import re
from dataclasses import dataclass
from decimal import Decimal
from repositories.customer_repository import CustomerRepository
from models.purchase import Purchase
from models.customer import Customer
from exceptions import DuplicateCustomerError, CustomerNotFoundError, InvalidEmailFormat

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]{1,30}@[A-Za-z0-9.-]{1,30}\.[A-Za-z]{2,15}$")

class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self._repository = repository
        self._empty_ids = []
        self._next_id = 0

    def validate_email_format(self, email: str) -> bool:
        """Validates that customer email follows a proper format"""
        return re.fullmatch(EMAIL_PATTERN, email) is not None
    
    def is_unique_email(self, email : str):
        is_unique = True
        for customer in self._repository.get_all():
            if customer.email == email:
                is_unique = False
        return is_unique
    
    def is_unique_username(self, username: str) -> bool:
        is_unique = True
        for customer in self._repository.get_all():
            if customer.username == username:
                is_unique = False
        return is_unique

    def create_customer(
                self,
                name : str,
                email : str,
                phone : str,
                username : str,
                lifetime_spend : float | Decimal,
                purchases : list[Purchase]
            ):
        if self._repository.get_by_name(name) is not None:
            raise DuplicateCustomerError("A customer with the same name is already in the repository")
        if not self.validate_email_format(email):
            raise InvalidEmailFormat("The email provided is not formated correctly")
        if not self.is_unique_email(email):
            raise DuplicateCustomerError("A customer with the same email already exists")
        if not self.is_unique_username(username):
            raise DuplicateCustomerError("A customer with the same username already exists")
        
        created_customer_id = None
        if len(self._empty_ids) == 0:
            created_customer_id = self._next_id
            self._next_id += 1
        else:
            created_customer_id = self._empty_ids.pop()

        created_customer = Customer(
            id=created_customer_id,
            name=name,
            email=email,
            phone=phone,
            username=username,
            lifetime_spend=lifetime_spend,
            purchases=purchases
        )
        self._repository.add(created_customer)
        return created_customer

    def get_all_customers(self) -> list[Customer]:
        return self._repository.get_all()
        
    def get_customer_by_name(self, name : str) -> Customer:
        returned_customer = self._repository.get_by_name(name)
        if returned_customer is None:
            raise CustomerNotFoundError(f"No Customer with name {name} was found in the repository")
        return returned_customer
    
    def get_customer_by_email(self, email : str) -> Customer:
        for customer in self._repository.get_all():
            if customer.email == email:
                return customer
        raise CustomerNotFoundError(f"No Customer with the email {email} was found in the repository")

    def get_customer_by_username(self, username : str) -> Customer:
        for customer in self._repository.get_all():
            if customer.username == username:
                return customer
        raise CustomerNotFoundError(f"No Customer with the username {username} was found in the repository")

    def update_customer(
                self,
                name : str,
                email : str,
                phone : str,
                username : str,
                lifetime_spend : float | Decimal,
                purchases : list[Purchase]
            ):
        old_customer = self._repository.get_by_name(name)
        if old_customer is None:
            raise CustomerNotFoundError(f"No Customer with name {name} was found in the repository")
        
        for customer in self._repository.get_all():
            if customer.id != old_customer.id:
                if customer.username == username:
                    raise DuplicateCustomerError("A customer with the same username already exists")
                if customer.email == email: 
                    raise DuplicateCustomerError("A customer with the same email already exists")
        
        if not self.validate_email_format(email):
            raise InvalidEmailFormat("The email provided is not formated correctly")
        
        updated_customer = Customer(
            id=old_customer.id,
            name=name,
            email=email,
            phone=phone,
            username=username,
            lifetime_spend=lifetime_spend,
            purchases=purchases
        )

        self._repository.update(name, updated_customer)

    def delete_customer(self, name : str):
        deleted_customer = self._repository.get_by_name(name)
        if deleted_customer is None:
            raise CustomerNotFoundError(f"No customer with name {name} was found in the repository")
        self._empty_ids.append(deleted_customer.id)
        self._repository.delete(name)