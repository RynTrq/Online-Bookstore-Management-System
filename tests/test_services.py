import tempfile
import unittest
from pathlib import Path

from shoponize.config import DatabaseConfig
from shoponize.db import Database
from shoponize.schema import initialize_sqlite
from shoponize.security import hash_password, verify_password
from shoponize.services import (
    AdminService,
    AuthService,
    CartService,
    NotFoundError,
    ValidationError,
    MAX_LOGIN_ATTEMPTS,
)


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        db_path = Path(self.tempdir.name) / "shoponize-test.db"
        self.db = Database(DatabaseConfig(sqlite_path=db_path))
        with self.db.connect() as connection:
            initialize_sqlite(connection)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_customer_login_resets_failed_attempts(self):
        auth = AuthService(self.db)

        failed = auth.login("customer", "john_doe", "bad-password")
        self.assertFalse(failed.success)

        success = auth.login("customer", "john_doe", "password123")
        self.assertTrue(success.success)

        with self.db.connect() as connection:
            attempts = self.db.scalar(
                connection,
                "SELECT loginAttempts FROM customer WHERE username = ?",
                ("john_doe",),
            )
        self.assertEqual(attempts, 0)

    def test_customer_account_locks_after_max_failed_attempts(self):
        auth = AuthService(self.db)

        for _ in range(MAX_LOGIN_ATTEMPTS):
            result = auth.login("customer", "john_doe", "wrong")

        self.assertFalse(result.success)
        self.assertIn("locked", result.message)
        self.assertFalse(auth.login("customer", "john_doe", "password123").success)

    def test_hashed_passwords_are_supported(self):
        hashed = hash_password("correct horse battery staple", salt="fixed")
        self.assertTrue(verify_password("correct horse battery staple", hashed))
        self.assertFalse(verify_password("wrong", hashed))

    def test_add_to_cart_accumulates_quantity_without_exceeding_stock(self):
        cart = CartService(self.db)
        customer_id = cart.customer_id_for_username("john_doe")

        cart.add_to_cart(customer_id, 101, 2)
        cart.add_to_cart(customer_id, 101, 3)

        lines = cart.view_cart(customer_id)
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0].quantity, 5)

        with self.assertRaises(ValidationError):
            cart.add_to_cart(customer_id, 101, 2)

    def test_checkout_creates_order_updates_stock_and_clears_cart(self):
        cart = CartService(self.db)
        customer_id = cart.customer_id_for_username("john_doe")
        cart.add_to_cart(customer_id, 101, 2)
        cart.add_to_cart(customer_id, 102, 1)

        result = cart.checkout(customer_id)

        self.assertEqual(result.order_number, 1001)
        self.assertEqual(result.amount, 68)
        self.assertEqual(cart.view_cart(customer_id), ())

        with self.db.connect() as connection:
            stock = self.db.scalar(
                connection,
                "SELECT quantityAvailable FROM product WHERE productID = ?",
                (101,),
            )
            item_count = self.db.scalar(
                connection,
                "SELECT COUNT(*) FROM contains WHERE orderNumber = ?",
                (result.order_number,),
            )
        self.assertEqual(stock, 4)
        self.assertEqual(item_count, 2)

    def test_checkout_rejects_empty_cart(self):
        cart = CartService(self.db)
        customer_id = cart.customer_id_for_username("john_doe")

        with self.assertRaises(ValidationError):
            cart.checkout(customer_id)

    def test_checkout_rolls_back_on_stock_conflict(self):
        cart = CartService(self.db)
        customer_id = cart.customer_id_for_username("john_doe")
        cart.add_to_cart(customer_id, 101, 2)

        # Simulate concurrent stock depletion after cart add.
        with self.db.connect() as connection:
            self.db.execute(
                connection,
                "UPDATE product SET quantityAvailable = ? WHERE productID = ?",
                (1, 101),
            )

        with self.assertRaises(ValidationError):
            cart.checkout(customer_id)

        with self.db.connect() as connection:
            order_count = self.db.scalar(connection, "SELECT COUNT(*) FROM orders")
            cart_quantity = self.db.scalar(
                connection,
                "SELECT quantity FROM cart WHERE customerID = ? AND productID = ?",
                (customer_id, 101),
            )
        self.assertEqual(order_count, 0)
        self.assertEqual(cart_quantity, 2)

    def test_admin_status_update_is_case_insensitive(self):
        admin = AdminService(self.db)
        with self.db.connect() as connection:
            self.db.execute(
                connection,
                "INSERT INTO orders (orderNumber, customerID, orderDate, amount, orderStatus) VALUES (?, ?, ?, ?, ?)",
                (1005, 1, "2024-03-15", 15.0, "Pending"),
            )

        admin.update_order_status(1005, "delivered")

        with self.db.connect() as connection:
            status = self.db.scalar(
                connection,
                "SELECT orderStatus FROM orders WHERE orderNumber = ?",
                (1005,),
            )
        self.assertEqual(status, "Delivered")

    def test_admin_update_order_status_rejects_invalid_value(self):
        admin = AdminService(self.db)
        with self.assertRaises(ValidationError):
            admin.update_order_status(1000, "Shipped")

    def test_add_to_cart_requires_existing_customer(self):
        cart = CartService(self.db)
        with self.assertRaises(NotFoundError):
            cart.add_to_cart(999, 101, 1)

    def test_sqlite_schema_contains_contact_and_management_tables(self):
        required_tables = {
            "contactNumber_customer",
            "contactNumber_admin",
            "contactNumber_supplier",
            "manages",
        }
        with self.db.connect() as connection:
            rows = self.db.rows(
                connection,
                "SELECT name FROM sqlite_master WHERE type = 'table'",
            )
        available = {row[0] for row in rows}
        self.assertTrue(required_tables.issubset(available))


if __name__ == "__main__":
    unittest.main()
