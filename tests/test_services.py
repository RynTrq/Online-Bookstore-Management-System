import tempfile
import unittest
from pathlib import Path

from shoponize.config import DatabaseConfig
from shoponize.db import Database
from shoponize.schema import initialize_sqlite
from shoponize.security import hash_password, verify_password
from shoponize.services import (
    AuthService,
    CartService,
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


if __name__ == "__main__":
    unittest.main()
