import re
from decimal import Decimal

from models.customer import Customer
from models.purchase import Purchase
from repositories.customer_repository import CustomerRepository
from exceptions import (
    CustomerNotFoundError,
    DuplicateCustomerError,
    InvalidEmailFormat,
)

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]{1,30}@[A-Za-z0-9.-]{1,30}\.[A-Za-z]{2,15}$")


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self._repository = repository
        self._empty_ids = []
        self._next_id = 0

    def validate_email_format(self, email: str) -> bool:
        """Validates that customer email follows a proper format."""
        if not isinstance(email, str) or not email:
            return False
        return re.fullmatch(EMAIL_PATTERN, email) is not None

    def is_unique_email(self, email: str) -> bool:
        lookup = email.strip().lower()
        return not any(customer.email.strip().lower() == lookup for customer in self._repository.get_all())

    def is_unique_username(self, username: str) -> bool:
        lookup = username.strip().lower()
        return not any(customer.username.strip().lower() == lookup for customer in self._repository.get_all())

    def _normalize_lifetime_spend(self, lifetime_spend: float | Decimal | None) -> Decimal:
        if lifetime_spend is None:
            return Decimal("0")
        if isinstance(lifetime_spend, Decimal):
            return lifetime_spend
        return Decimal(str(lifetime_spend))

    def _coerce_customer_inputs(
        self,
        name_or_customer: str | Customer,
        email: str | None = None,
        phone: str | None = None,
        username: str | None = None,
        lifetime_spend: float | Decimal | None = None,
        purchases: list[Purchase] | None = None,
    ) -> tuple[str, str, str, str, Decimal, list[Purchase]]:
        if isinstance(name_or_customer, Customer):
            customer = name_or_customer
            return (
                customer.name,
                customer.email,
                customer.phone,
                customer.username,
                self._normalize_lifetime_spend(customer.lifetime_spend),
                list(customer.purchases),
            )

        if not isinstance(name_or_customer, str):
            raise TypeError("name_or_customer must be a customer name or Customer instance")

        return (
            name_or_customer,
            email or "",
            phone or "",
            username or "",
            self._normalize_lifetime_spend(lifetime_spend),
            list(purchases or []),
        )

    def _find_customer_by_name(self, name: str) -> Customer | None:
        lookup = name.strip().lower()
        for customer in self._repository.get_all():
            if customer.name.strip().lower() == lookup:
                return customer
        return None

    def _find_customer_by_email(self, email: str) -> Customer | None:
        lookup = email.strip().lower()
        for customer in self._repository.get_all():
            if customer.email.strip().lower() == lookup:
                return customer
        return None

    def _find_customer_by_username(self, username: str) -> Customer | None:
        lookup = username.strip().lower()
        for customer in self._repository.get_all():
            if customer.username.strip().lower() == lookup:
                return customer
        return None

    def create_customer(
        self,
        name_or_customer: str | Customer,
        email: str | None = None,
        phone: str | None = None,
        username: str | None = None,
        lifetime_spend: float | Decimal | None = None,
        purchases: list[Purchase] | None = None,
    ) -> Customer:
        name, email, phone, username, lifetime_spend, purchases = self._coerce_customer_inputs(
            name_or_customer,
            email,
            phone,
            username,
            lifetime_spend,
            purchases,
        )

        if self._find_customer_by_name(name) is not None:
            raise DuplicateCustomerError("A customer with the same name is already in the repository")
        if not self.validate_email_format(email):
            raise InvalidEmailFormat("Invalid email format. Please use user@example.com")
        if not self.is_unique_email(email):
            raise DuplicateCustomerError("That email is already registered. Please use a different email address.")
        if not self.is_unique_username(username):
            raise DuplicateCustomerError("That username is already taken. Please choose a different username.")

        if isinstance(name_or_customer, Customer):
            self._repository.add(name_or_customer)
            return name_or_customer

        created_customer_id = self._empty_ids.pop() if self._empty_ids else self._next_id
        if not self._empty_ids and created_customer_id == self._next_id:
            self._next_id += 1

        created_customer = Customer(
            id=created_customer_id,
            name=name,
            email=email,
            phone=phone,
            username=username,
            lifetime_spend=lifetime_spend,
            purchases=purchases,
        )
        self._repository.add(created_customer)
        return created_customer

    def get_all_customers(self) -> list[Customer]:
        return self._repository.get_all()

    def get_customer_by_name(self, name: str) -> Customer:
        returned_customer = self._find_customer_by_name(name)
        if returned_customer is None:
            raise CustomerNotFoundError(f"No Customer with name {name} was found in the repository")
        return returned_customer

    def get_customer_by_email(self, email: str) -> Customer:
        returned_customer = self._find_customer_by_email(email)
        if returned_customer is None:
            raise CustomerNotFoundError(f"No Customer with the email {email} was found in the repository")
        return returned_customer

    def get_customer_by_username(self, username: str) -> Customer:
        returned_customer = self._find_customer_by_username(username)
        if returned_customer is None:
            raise CustomerNotFoundError(f"No Customer with the username {username} was found in the repository")
        return returned_customer

    def update_customer(
        self,
        name_or_customer: str | Customer,
        email: str | None = None,
        phone: str | None = None,
        username: str | None = None,
        lifetime_spend: float | Decimal | None = None,
        purchases: list[Purchase] | None = None,
    ) -> Customer:
        name, email, phone, username, lifetime_spend, purchases = self._coerce_customer_inputs(
            name_or_customer,
            email,
            phone,
            username,
            lifetime_spend,
            purchases,
        )

        old_customer = self._find_customer_by_name(name)
        if old_customer is None:
            raise CustomerNotFoundError(f"No Customer with name {name} was found in the repository")

        for customer in self._repository.get_all():
            if customer.id == old_customer.id:
                continue
            if customer.username.strip().lower() == username.strip().lower():
                raise DuplicateCustomerError("That username is already taken. Please choose a different username.")
            if customer.email.strip().lower() == email.strip().lower():
                raise DuplicateCustomerError("That email is already registered. Please use a different email address.")

        if not self.validate_email_format(email):
            raise InvalidEmailFormat("Invalid email format. Please use user@example.com")

        updated_customer = Customer(
            id=old_customer.id,
            name=name,
            email=email,
            phone=phone,
            username=username,
            lifetime_spend=lifetime_spend,
            purchases=purchases,
        )

        self._repository.update(name, updated_customer)
        return updated_customer

    def delete_customer(self, name: str):
        deleted_customer = self._find_customer_by_name(name)
        if deleted_customer is None:
            raise CustomerNotFoundError(f"No customer with name {name} was found in the repository")
        self._empty_ids.append(deleted_customer.id)
        self._repository.delete(name)