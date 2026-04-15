"""Interactive command-line interface for Shoponize."""

from __future__ import annotations

from typing import Callable, Iterable, Optional, Union

from .config import DatabaseConfig
from .db import Database, DatabaseError
from .schema import initialize_sqlite
from .services import AdminService, AuthService, CartService, CatalogService, NotFoundError, ValidationError


def main() -> int:
    try:
        config = DatabaseConfig.from_env()
        db = Database(config)
        if config.backend == "sqlite":
            with db.connect() as connection:
                initialize_sqlite(connection)
        run_app(db)
        return 0
    except (DatabaseError, ValueError) as exc:
        print(f"Startup failed: {exc}")
        return 1


def run_app(db: Database) -> None:
    auth = AuthService(db)
    catalog = CatalogService(db)
    cart = CartService(db)
    admin = AdminService(db)

    print("Shoponize Initialized")
    while True:
        choice = choose(
            "Main Menu",
            [
                "Enter as a customer",
                "Enter as an admin",
                "Exit",
            ],
        )
        if choice == 1:
            username = prompt("Username")
            password = prompt("Password")
            result = auth.login("customer", username, password)
            print(result.message)
            if result.success:
                customer_page(username, catalog, cart)
        elif choice == 2:
            username = prompt("Username")
            password = prompt("Password")
            result = auth.login("admin", username, password)
            print(result.message)
            if result.success:
                admin_page(admin, auth)
        elif choice == 3:
            print("Thanks for visiting Shoponize.")
            return


def customer_page(username: str, catalog: CatalogService, cart: CartService) -> None:
    customer_id = cart.customer_id_for_username(username)
    while True:
        choice = choose(
            "Customer Menu",
            [
                "Search products",
                "View product categories",
                "View cart",
                "Checkout",
                "Logout",
            ],
        )
        try:
            if choice == 1:
                products = catalog.search_products(prompt("Product name or keyword"))
                print_rows(products, ("ID", "Name", "Price", "Available", "Description"))
                customer_product_actions(customer_id, catalog, cart)
            elif choice == 2:
                print_rows(catalog.categories(), ("ID", "Name", "Description"))
                category_id = prompt_int("Category ID to view, or 0 to go back", minimum=0)
                if category_id:
                    print_rows(
                        catalog.products_in_category(category_id),
                        ("ID", "Name", "Price", "Available"),
                    )
                    customer_product_actions(customer_id, catalog, cart)
            elif choice == 3:
                show_cart(cart, customer_id)
            elif choice == 4:
                result = cart.checkout(customer_id)
                print(f"Order {result.order_number} placed for {money(result.amount)}.")
            elif choice == 5:
                print("Logging out...")
                return
        except (ValidationError, NotFoundError) as exc:
            print(exc)


def customer_product_actions(customer_id: int, catalog: CatalogService, cart: CartService) -> None:
    while True:
        choice = choose("Product Actions", ["Add to cart", "View product details", "Go back"])
        try:
            if choice == 1:
                cart.add_to_cart(
                    customer_id,
                    prompt_int("Product ID"),
                    prompt_int("Quantity", minimum=1),
                )
                print("Added to cart.")
            elif choice == 2:
                product = catalog.product_details(prompt_int("Product ID"))
                print_rows([product], ("ID", "Name", "Price", "Available", "Description", "Review"))
            elif choice == 3:
                return
        except (ValidationError, NotFoundError) as exc:
            print(exc)


def show_cart(cart: CartService, customer_id: int) -> None:
    lines = cart.view_cart(customer_id)
    if not lines:
        print("Cart is empty.")
        return
    print_rows(
        [(line.product_id, line.name, line.unit_price, line.quantity, line.total) for line in lines],
        ("ID", "Name", "Unit Price", "Quantity", "Total"),
    )
    choice = choose("Cart Actions", ["Remove item", "Checkout", "Go back"])
    if choice == 1:
        cart.remove_from_cart(customer_id, prompt_int("Product ID"))
        print("Removed from cart.")
    elif choice == 2:
        result = cart.checkout(customer_id)
        print(f"Order {result.order_number} placed for {money(result.amount)}.")


def admin_page(admin: AdminService, auth: AuthService) -> None:
    while True:
        choice = choose(
            "Admin Menu",
            [
                "View orders",
                "Update order status",
                "Delete order",
                "View low stock products",
                "Update product price",
                "Unlock customer account",
                "Logout",
            ],
        )
        try:
            if choice == 1:
                print_rows(admin.orders(), ("Order", "Customer", "Date", "Amount", "Status"))
            elif choice == 2:
                admin.update_order_status(prompt_int("Order number"), prompt("New status"))
                print("Order status updated.")
            elif choice == 3:
                admin.delete_order(prompt_int("Order number"))
                print("Order deleted.")
            elif choice == 4:
                print_rows(admin.low_stock_products(), ("ID", "Name", "Price", "Available"))
            elif choice == 5:
                admin.update_product_price(
                    prompt_int("Product ID"),
                    prompt_float("New price", minimum=0),
                )
                print("Product price updated.")
            elif choice == 6:
                auth.unlock_account("customer", prompt_int("Customer ID"))
                print("Customer account unlocked.")
            elif choice == 7:
                print("Logging out...")
                return
        except (ValidationError, NotFoundError) as exc:
            print(exc)


def choose(title: str, options: list[str]) -> int:
    while True:
        print("-" * 20)
        print(title)
        for index, label in enumerate(options, start=1):
            print(f"{index}. {label}")
        print("-" * 20)
        value = prompt_int("Choose an option", minimum=1)
        if value <= len(options):
            return value
        print("Invalid option. Please try again.")


def prompt(label: str) -> str:
    return input(f"{label}: ").strip()


def prompt_int(label: str, minimum: Optional[int] = None) -> int:
    return _prompt_number(label, int, minimum)


def prompt_float(label: str, minimum: Optional[float] = None) -> float:
    return _prompt_number(label, float, minimum)


def _prompt_number(
    label: str,
    parser: Callable[[str], Union[int, float]],
    minimum: Optional[Union[int, float]],
):
    while True:
        raw = prompt(label)
        try:
            value = parser(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if minimum is not None and value < minimum:
            print(f"Please enter a value greater than or equal to {minimum}.")
            continue
        return value


def print_rows(rows: Iterable[object], headers: tuple[str, ...]) -> None:
    rows = [tuple(row) for row in rows]
    if not rows:
        print("No records found.")
        return

    widths = [len(header) for header in headers]
    rendered_rows = []
    for row in rows:
        rendered = [money(value) if isinstance(value, float) else str(value) for value in row]
        rendered_rows.append(rendered)
        widths = [max(width, len(value)) for width, value in zip(widths, rendered)]

    header_line = " | ".join(header.ljust(width) for header, width in zip(headers, widths))
    print(header_line)
    print("-+-".join("-" * width for width in widths))
    for row in rendered_rows:
        print(" | ".join(value.ljust(width) for value, width in zip(row, widths)))


def money(value: float) -> str:
    return f"${value:,.2f}"
