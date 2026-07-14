"""
Tests for the CustomerRepository class.
"""

import pytest
from decimal import Decimal
from models.customer import Customer
from repositories.customer_repository import CustomerRepository

def test_add_and_get_all():
    """Ensure customers are added and retrieved correctly."""
    repo = CustomerRepository()
    alice = Customer(id=1, name="Alice", email="alice@example.com", lifetime_spend=10.50)
    bob = Customer(id=2, name="Bob", email="bob@coffee.io", lifetime_spend=0)

    repo.add(alice)
    repo.add(bob)

    all_items = repo.get_all()

    assert len(all_items) == 2
    assert all_items[0].name == "Alice"
    assert all_items[1].name == "Bob"

def test_get_by_name_found():
    """Ensure get_by_name retrns the correct customer."""
    repo = CustomerRepository()
    customer = Customer(id=1, name="Charlie", email="charlie@beans.net", lifetime_spend=12.34)
    repo.add(customer)

    result = repo.get_by_name("Charlie")

    assert result is not None
    assert result.name == "Charlie"

def test_get_by_name_not_found():
    """Ensure get_by_name returns None wen customer does not exist."""
    repo = CustomerRepository()
    result = repo.get_by_name("NotReal")

    assert result is None

def test_update_success():
    """Ensure update replaces the correct customer."""
    repo = CustomerRepository()
    old = Customer(id=1, name="Alice", email="alice@example.com", lifetime_spend=10.50)
    new = Customer(id=1, name="Alice", email="alice@awesome.com", lifetime_spend=11.50)

    repo.add(old)
    updated = repo.update("Alice", new)

    assert updated is not None
    assert updated.email == "alice@awesome.com"
    assert updated.lifetime_spend == Decimal("11.50")

def test_update_not_found():
    """Ensure update returns None when customer does not exist."""
    repo = CustomerRepository()
    new = Customer(id=1, name="Alice", email="alice@example.com", lifetime_spend=10.50)

    result = repo.update("NotReal", new)

    assert result is None

def test_delete_success():
    """Ensure delete removes the customer and returns True."""
    repo = CustomerRepository()
    customer = Customer(id=1, name="Alice", email="alice@example.com", lifetime_spend=10.50)
    repo.add(customer)

    deleted = repo.delete("Alice")

    assert deleted is True
    assert repo.get_by_name("Alice") is None

def test_delete_not_found():
    """Ensure delete returns False when customer does not exist."""
    repo = CustomerRepository()

    deleted = repo.delete("NotReal")

    assert deleted is False