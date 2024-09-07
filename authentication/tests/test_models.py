from django.test import TestCase

from authentication.models import User


class CustomUserManagerTests(TestCase):

    def setUp(self) -> None:
        # Create users with different roles
        self.owner = User.objects.create_user(
            username="owner1",
            password="Test@1234",
            user_type="owner",
            phone_number="01700000001",
            address="Owner's Address",
            first_name="Owner",
            last_name="One",
        )
        self.employee = User.objects.create_user(
            username="employee1",
            password="Test@1234",
            user_type="employee",
            phone_number="01700000002",
            address="Employee's Address",
            first_name="Employee",
            last_name="One",
        )
        self.customer = User.objects.create_user(
            username="customer1",
            password="Test@1234",
            user_type="customer",
            phone_number="01700000003",
            address="Customer's Address",
            first_name="Customer",
            last_name="One",
        )

    def test_get_employees(self) -> None:
        # Test if get_employees() only returns users with 'employee' user_type
        employees = User.objects.get_employees()
        self.assertIn(self.employee, employees)
        self.assertNotIn(self.owner, employees)
        self.assertNotIn(self.customer, employees)
        self.assertEqual(employees.count(), 1)

    def test_get_customers(self) -> None:
        # Test if get_customers() only returns users with 'customer' user_type
        customers = User.objects.get_customers()
        self.assertIn(self.customer, customers)
        self.assertNotIn(self.owner, customers)
        self.assertNotIn(self.employee, customers)
        self.assertEqual(customers.count(), 1)

    def test_get_owners(self) -> None:
        # Test if get_owners() only returns users with 'owner' user_type
        owners = User.objects.get_owners()
        self.assertIn(self.owner, owners)
        self.assertNotIn(self.employee, owners)
        self.assertNotIn(self.customer, owners)
        self.assertEqual(owners.count(), 1)

    def test_user_str(self) -> None:
        # Test the __str__ method of the User model
        self.assertEqual(str(self.owner), self.owner.get_full_name())
        self.assertEqual(str(self.employee), self.employee.get_full_name())
        self.assertEqual(str(self.customer), self.customer.get_full_name())

    def test_automatic_profile_creation_on_create_user(self) -> None:
        # Test if a Profile instance is automatically created when a User is created
        self.assertIsNotNone(self.owner.owner)
        self.assertIsNotNone(self.employee.employee)
        self.assertIsNotNone(self.customer.customer)
