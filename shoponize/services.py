"""Business services for authentication, catalog, cart, and administration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Iterable, Optional

from .db import Database
from .security import verify_password


MAX_LOGIN_ATTEMPTS = 3
LOW_STOCK_THRESHOLD = 3
VALID_ORDER_STATUSES = {"Pending", "In Progress", "Delivered", "Cancelled"}
ROLE_TABLES = {"customer": "customer", "admin": "admin", "supplier": "supplier"}
ORDER_STATUS_LOOKUP = {status.lower(): status for status in VALID_ORDER_STATUSES}


@dataclass(frozen=True)
class AuthResult:
    success: bool
    message: str
    role: Optional[str] = None
    username: Optional[str] = None


@dataclass(frozen=True)
class CartLine:
    product_id: int
    name: str
    unit_price: float
    quantity: int

    @property
    def total(self) -> float:
        return self.unit_price * self.quantity


@dataclass(frozen=True)
class CheckoutResult:
    order_number: int
    amount: float
    items: tuple[CartLine, ...]


class ValidationError(ValueError):
    """Raised when user input cannot be accepted."""


class NotFoundError(LookupError):
    """Raised when a requested entity does not exist."""


class AuthService:
    def __init__(self, db: Database):
        self.db = db

    def login(self, role: str, username: str, password: str) -> AuthResult:
        role = role.strip().lower()
        table = ROLE_TABLES.get(role)
        if table is None:
            raise ValidationError(f"Unsupported role: {role}")

        username = username.strip()
        if not username or not password:
            return AuthResult(False, "Username and password are required", role, username)

        with self.db.connect() as connection:
            row = self.db.row(
                connection,
                f"""
                SELECT password, loginAttempts, isLocked
                FROM {table}
                WHERE username = ?
                """,
                (username,),
            )
            if row is None:
                return AuthResult(False, "Username not found", role, username)

            stored_password, attempts, is_locked = row
            if bool(is_locked):
                return AuthResult(False, "Account is locked", role, username)

            if verify_password(password, stored_password):
                self.db.execute(
                    connection,
                    f"UPDATE {table} SET loginAttempts = 0 WHERE username = ?",
                    (username,),
                )
                return AuthResult(True, "Login successful", role, username)

            attempts = int(attempts or 0) + 1
            should_lock = attempts >= MAX_LOGIN_ATTEMPTS
            self.db.execute(
                connection,
                f"UPDATE {table} SET loginAttempts = ?, isLocked = ? WHERE username = ?",
                (attempts, int(should_lock), username),
            )
            if should_lock:
                return AuthResult(False, "Maximum attempts reached; account locked", role, username)
            return AuthResult(False, "Wrong password", role, username)

    def unlock_account(self, role: str, account_id: int) -> None:
        role = role.strip().lower()
        table = ROLE_TABLES.get(role)
        if table is None:
            raise ValidationError(f"Unsupported role: {role}")
        if account_id <= 0:
            raise ValidationError("Account ID must be a positive integer")

        id_column = f"{table}ID"
        with self.db.connect() as connection:
            updated = self.db.execute(
                connection,
                f"UPDATE {table} SET isLocked = 0, loginAttempts = 0 WHERE {id_column} = ?",
                (account_id,),
            ).rowcount
            if updated == 0:
                raise NotFoundError(f"{role.title()} account not found")


class CatalogService:
    def __init__(self, db: Database):
        self.db = db

    def categories(self) -> Iterable[Any]:
        with self.db.connect() as connection:
            return self.db.rows(
                connection,
                "SELECT categoryID, name, description FROM productCategory ORDER BY name",
            )

    def search_products(self, term: str) -> Iterable[Any]:
        term = term.strip()
        if not term:
            raise ValidationError("Search term is required")

        search = f"%{term}%"
        with self.db.connect() as connection:
            return self.db.rows(
                connection,
                """
                SELECT productID, name, price, quantityAvailable, description
                FROM product
                WHERE name LIKE ? OR description LIKE ?
                ORDER BY name
                """,
                (search, search),
            )

    def product_details(self, product_id: int) -> Any:
        with self.db.connect() as connection:
            row = self.db.row(
                connection,
                """
                SELECT productID, name, price, quantityAvailable, description, review
                FROM product
                WHERE productID = ?
                """,
                (product_id,),
            )
            if row is None:
                raise NotFoundError("Product not found")
            return row

    def products_in_category(self, category_id: int) -> Iterable[Any]:
        with self.db.connect() as connection:
            return self.db.rows(
                connection,
                """
                SELECT productID, name, price, quantityAvailable
                FROM product
                WHERE categoryID = ?
                ORDER BY name
                """,
                (category_id,),
            )


class CartService:
    def __init__(self, db: Database):
        self.db = db

    def customer_id_for_username(self, username: str) -> int:
        with self.db.connect() as connection:
            customer_id = self.db.scalar(
                connection,
                "SELECT customerID FROM customer WHERE username = ?",
                (username,),
            )
            if customer_id is None:
                raise NotFoundError("Customer not found")
            return int(customer_id)

    def add_to_cart(self, customer_id: int, product_id: int, quantity: int) -> None:
        self._validate_id("Customer ID", customer_id)
        self._validate_id("Product ID", product_id)
        self._validate_quantity(quantity)

        with self.db.connect() as connection:
            self._ensure_customer_exists(connection, customer_id)
            product = self.db.row(
                connection,
                "SELECT quantityAvailable FROM product WHERE productID = ?",
                (product_id,),
            )
            if product is None:
                raise NotFoundError("Product not found")

            available = int(product[0])
            existing_quantity = self.db.scalar(
                connection,
                "SELECT quantity FROM cart WHERE customerID = ? AND productID = ?",
                (customer_id, product_id),
            )
            new_quantity = int(existing_quantity or 0) + quantity
            if new_quantity > available:
                raise ValidationError("Requested quantity exceeds available stock")

            if existing_quantity is None:
                self.db.execute(
                    connection,
                    "INSERT INTO cart (customerID, productID, quantity) VALUES (?, ?, ?)",
                    (customer_id, product_id, new_quantity),
                )
            else:
                self.db.execute(
                    connection,
                    "UPDATE cart SET quantity = ? WHERE customerID = ? AND productID = ?",
                    (new_quantity, customer_id, product_id),
                )

    def remove_from_cart(self, customer_id: int, product_id: int) -> None:
        self._validate_id("Customer ID", customer_id)
        self._validate_id("Product ID", product_id)

        with self.db.connect() as connection:
            deleted = self.db.execute(
                connection,
                "DELETE FROM cart WHERE customerID = ? AND productID = ?",
                (customer_id, product_id),
            ).rowcount
            if deleted == 0:
                raise NotFoundError("Product not found in cart")

    def view_cart(self, customer_id: int) -> tuple[CartLine, ...]:
        self._validate_id("Customer ID", customer_id)

        with self.db.connect() as connection:
            self._ensure_customer_exists(connection, customer_id)
            rows = self.db.rows(
                connection,
                """
                SELECT p.productID, p.name, p.price, c.quantity
                FROM cart c
                JOIN product p ON p.productID = c.productID
                WHERE c.customerID = ?
                ORDER BY p.name
                """,
                (customer_id,),
            )
            return tuple(CartLine(int(row[0]), row[1], float(row[2]), int(row[3])) for row in rows)

    def checkout(self, customer_id: int) -> CheckoutResult:
        self._validate_id("Customer ID", customer_id)

        with self.db.connect() as connection:
            self._ensure_customer_exists(connection, customer_id)
            rows = self.db.rows(
                connection,
                """
                SELECT p.productID, p.name, p.price, p.quantityAvailable, c.quantity
                FROM cart c
                JOIN product p ON p.productID = c.productID
                WHERE c.customerID = ?
                ORDER BY p.productID
                """,
                (customer_id,),
            )
            if not rows:
                raise ValidationError("Cart is empty")

            items: list[CartLine] = []
            for row in rows:
                product_id, name, price, available, quantity = row
                if int(quantity) > int(available):
                    raise ValidationError(f"Insufficient stock for product {product_id}")
                items.append(CartLine(int(product_id), name, float(price), int(quantity)))

            amount = self._calculate_total(items)
            order_number = self._next_order_number(connection)
            self.db.execute(
                connection,
                """
                INSERT INTO orders (orderNumber, customerID, orderDate, amount, orderStatus)
                VALUES (?, ?, ?, ?, ?)
                """,
                (order_number, customer_id, date.today().isoformat(), float(amount), "Pending"),
            )
            for item in items:
                self.db.execute(
                    connection,
                    """
                    INSERT INTO contains (orderNumber, productID, quantity, unitPrice)
                    VALUES (?, ?, ?, ?)
                    """,
                    (order_number, item.product_id, item.quantity, item.unit_price),
                )
                updated = self.db.execute(
                    connection,
                    """
                    UPDATE product
                    SET quantityAvailable = quantityAvailable - ?,
                        isLowStock = CASE
                            WHEN quantityAvailable - ? < ? THEN 1
                            ELSE 0
                        END
                    WHERE productID = ? AND quantityAvailable >= ?
                    """,
                    (
                        item.quantity,
                        item.quantity,
                        LOW_STOCK_THRESHOLD,
                        item.product_id,
                        item.quantity,
                    ),
                ).rowcount
                if updated == 0:
                    raise ValidationError(f"Insufficient stock for product {item.product_id}")
            self.db.execute(connection, "DELETE FROM cart WHERE customerID = ?", (customer_id,))
            return CheckoutResult(order_number, float(amount), tuple(items))

    def _next_order_number(self, connection: Any) -> int:
        current = self.db.scalar(connection, "SELECT COALESCE(MAX(orderNumber), 1000) FROM orders")
        return int(current) + 1

    def _validate_quantity(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero")

    def _validate_id(self, label: str, value: int) -> None:
        if value <= 0:
            raise ValidationError(f"{label} must be a positive integer")

    def _ensure_customer_exists(self, connection: Any, customer_id: int) -> None:
        exists = self.db.scalar(
            connection,
            "SELECT 1 FROM customer WHERE customerID = ?",
            (customer_id,),
        )
        if exists is None:
            raise NotFoundError("Customer not found")

    def _calculate_total(self, items: Iterable[CartLine]) -> Decimal:
        total = sum(
            (Decimal(str(item.unit_price)) * Decimal(item.quantity) for item in items),
            Decimal("0"),
        )
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class AdminService:
    def __init__(self, db: Database):
        self.db = db

    def orders(self) -> Iterable[Any]:
        with self.db.connect() as connection:
            return self.db.rows(
                connection,
                """
                SELECT orderNumber, customerID, orderDate, amount, orderStatus
                FROM orders
                ORDER BY orderNumber DESC
                """,
            )

    def update_order_status(self, order_number: int, status: str) -> None:
        normalized_status = ORDER_STATUS_LOOKUP.get(status.strip().lower())
        if normalized_status is None:
            raise ValidationError(
                f"Order status must be one of: {', '.join(sorted(VALID_ORDER_STATUSES))}"
            )
        with self.db.connect() as connection:
            updated = self.db.execute(
                connection,
                "UPDATE orders SET orderStatus = ? WHERE orderNumber = ?",
                (normalized_status, order_number),
            ).rowcount
            if updated == 0:
                raise NotFoundError("Order not found")

    def delete_order(self, order_number: int) -> None:
        with self.db.connect() as connection:
            deleted = self.db.execute(
                connection,
                "DELETE FROM orders WHERE orderNumber = ?",
                (order_number,),
            ).rowcount
            if deleted == 0:
                raise NotFoundError("Order not found")

    def low_stock_products(self) -> Iterable[Any]:
        with self.db.connect() as connection:
            return self.db.rows(
                connection,
                """
                SELECT productID, name, price, quantityAvailable
                FROM product
                WHERE quantityAvailable < ?
                ORDER BY quantityAvailable ASC, name
                """,
                (LOW_STOCK_THRESHOLD,),
            )

    def update_product_price(self, product_id: int, price: float) -> None:
        if price < 0:
            raise ValidationError("Price cannot be negative")
        with self.db.connect() as connection:
            updated = self.db.execute(
                connection,
                "UPDATE product SET price = ? WHERE productID = ?",
                (price, product_id),
            ).rowcount
            if updated == 0:
                raise NotFoundError("Product not found")
