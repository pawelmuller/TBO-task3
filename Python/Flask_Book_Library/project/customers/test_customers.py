import secrets
import string
import unittest

from project import db, app
from project.customers.models import Customer
from sqlalchemy.exc import IntegrityError


class TestCustomerModel(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_valid_customer_creation(self):
        customer = Customer(
            name='John Doe',
            city='City',
            age=40,
            pesel='99999999999',
            street='Marszalkowska',
            appNo='123'
        )
        db.session.add(customer)
        db.session.commit()
        self.assertIsNotNone(customer.id)

    def test_invalid_age(self):
        customer = Customer(
            name='John Doe',
            city='City',
            age=-40,
            pesel='99999999999',
            street='Street St',
            appNo='456'
        )
        db.session.add(customer)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_sql_injection(self):
        customer = Customer(
            name="John Doe'); DROP TABLE customers;--",
            city='City',
            age=25,
            pesel='99999999999',
            street='Street St',
            appNo='789'
        )
        db.session.add(customer)
        db.session.commit()
        self.assertNotIn("DROP TABLE", customer.name)

    def test_javascript_injection(self):
        customer = Customer(
            name='<script>alert("is anyone there?")</script>',
            city='City',
            age=22,
            pesel='99999999999',
            street='Street St',
            appNo='135'
        )
        db.session.add(customer)
        db.session.commit()
        self.assertNotIn('<script>', customer.name)
        self.assertNotIn('</script>', customer.name)

    def test_extreme_string_length(self):
        customer = Customer(
            name=''.join(secrets.choice(string.ascii_letters) for _ in range(300)),
            city='City',
            age=40,
            pesel='99999999999',
            street='Street St',
            appNo='246'
        )
        db.session.add(customer)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_empty_fields(self):
        test_cases = [
            {'name': None, 'city': None, 'age': None, 'pesel': None, 'street': None, 'appNo': None},
            {'name': '', 'city': '', 'age': 0, 'pesel': '', 'street': '', 'appNo': ''},
        ]

        for test_case in test_cases:
            with self.subTest(case=test_case):
                new_customer = Customer(
                    name=test_case.get('name'),
                    city=test_case.get('city'),
                    age=test_case.get('age'),
                    pesel=test_case.get('pesel'),
                    street=test_case.get('street'),
                    appNo=test_case.get('appNo')
                )
                db.session.add(new_customer)
                with self.assertRaises(IntegrityError):
                    db.session.commit()

    def test_unique_pesel(self):
        customer1 = Customer(name='John Doe', city='Paris', age=15, pesel='1111111111', street='Test St', appNo='C001')
        customer2 = Customer(name='Jane Doe', city='London', age=90, pesel='1111111111', street='Test St', appNo='C002')
        db.session.add(customer1)
        db.session.commit()
        db.session.add(customer2)
        with self.assertRaises(IntegrityError):
            db.session.commit()


if __name__ == '__main__':
    unittest.main()