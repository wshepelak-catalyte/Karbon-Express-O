"""
Repository for managing Customer objects in memory.
"""

from models.customer import Customer

class CustomerRepository:
    """
    Provides CRUD operations for Customer objects stored in memory.

    Attributes:
        _customers (list[Customer]): Interal list storing Customer instances.
    """
    def __init__(self):
        """
        Initialize an empty CustomerRepository
        """
        self._customers: list[Customer] = []

    def get_all(self) -> list[Customer]:
        """
        Retrieve all Customer objects in the repository.

        Returns:
            list[Customer]: A list of all stored ingredients.
        """
        return self._customers
    
    def get_by_name(self, name : str) -> Customer | None:
        """
        Retrieve a Customer by its legal name (case-insensitive).

        Args:
            name (str): The name of the customer to search for.

        Returns:
            Customer | None: The matching Customer, or None if no customer is found.
        """
        if name is None:
            return None
        lookup = name.strip().lower()
        return next((c for c in self._customers if isinstance(c.name, str) and c.name.strip().lower() == lookup), None)

    def get_by_username(self, username : str) -> Customer | None:
        """
        Retrieve a Customer by username (case-insensitive).

        Args:
            username (str): The username of the customer to search for.

        Returns:
            Customer | None: The matching Customer, or None if no customer is found.
        """
        if username is None:
            return None
        lookup = username.strip().lower()
        return next((c for c in self._customers if isinstance(c.username, str) and c.username.strip().lower() == lookup), None)

    def get_by_email(self, email : str) -> Customer | None:
        """
        Retrieve a Customer by its email (case-insensitive).

        Args:
            email (str): The email of the customer to search for.

        Returns:
            Customer | None: The matching Customer, or None if no customer is found.
        """
        if email is None:
            return None
        lookup = email.strip().lower()
        return next((c for c in self._customers if isinstance(c.email, str) and c.email.strip().lower() == lookup), None)
    
    def add(self, customer : Customer) -> Customer:
        """
        Add a new Customer to the repository.

        Args:
            customer (Customer): the customer to add.

        Returns:
            Customer: The added customer.
        """
        self._customers.append(customer)
        return customer
    
    def update(self, name : str, customer : Customer) -> Customer | None:
        """
        Update an existing Customer by name.

        Args:
            name (str): The name of the customer to update.
            customer (Customer): The new customer data.

        Returns:
            Customer | None: The updated customer, or non if no customer is found.
        """
        for iterator, _customer in enumerate(self._customers):
            if _customer.name == name:
                self._customers[iterator] = customer
                return customer
        
        return None
    
    def delete(self, name : str) -> bool:
        """
        Delete a Customer by name.

        Args:
            name (str): The name of the customer to delete.

        Returns:
            bool: True if deletion occurred, False otherwise.
        """
        delete_occured = False
        for iterator, _customer in enumerate(self._customers):
            if _customer.name == name:
                del self._customers[iterator]
                delete_occured = True
        return delete_occured