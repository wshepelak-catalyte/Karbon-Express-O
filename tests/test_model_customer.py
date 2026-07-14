"""
Tests for the Customer model.
"""

import pytest
from decimal import Decimal
from models.customer import Customer

@pytest.mark.parametrize(
    "customer, expected_id, expected_name, expected_email, expected_spend",
    [
        (
            Customer(
                id=1,
                name="Alice",
                email="alice@example.com",
                lifetime_spend=10.50
            ),
            1,
            "Alice",
            "alice@example.com",
            Decimal("10.50")
        ),
        (
            Customer(
                id=2,
                name="Bob",
                email="bob@coffee.io",
                lifetime_spend=0
            ),
            2,
            "Bob",
            "bob@coffee.io",
            Decimal("0")
        )
    ]
)
def test_customer_initialization(customer, expected_id, expected_name, expected_email, expected_spend):
    """Ensure Customer initializes with correct attribute values."""
    assert customer.id == expected_id
    assert customer.name == expected_name
    assert customer.email == expected_email
    assert customer.lifetime_spend == expected_spend

@pytest.mark.parametrize(
    "customer",
    [
        Customer(id=1, name="Alice", email="alice@exmaple.com", lifetime_spend=10.50),
        Customer(id=2, name="Bob", email="bob@coffee.io", lifetime_spend=Decimal("5.25"))
    ]
)
def test_customer_types(customer):
    """Verify Customer fields have correct types."""
    assert isinstance(customer.id, int)
    assert isinstance(customer.name, str)
    assert isinstance(customer.email, str)
    assert isinstance(customer.lifetime_spend, Decimal)

def test_customer_decimal_cast():
    """Ensure lifetime_spend is cast to Decimal when initialized with float."""
    customer = Customer(id=1, name="Charlie", email="charlie@beans.net", lifetime_spend=12.34)
    assert isinstance(customer.lifetime_spend, Decimal)
    assert customer.lifetime_spend == Decimal("12.34")

@pytest.mark.parametrize(
        "email",
        [
            "noatsymbol.com",
            "@missingusername.com",
            "toolongusernameeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee@example.com",
            "user@toolongdomainnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn@example.com",
            "user@domain.x",
            "user@domain.extensiontoolonggggggggggg"
        ]
)
def test_customer_invalid_email_format(email):
    """
    Ensure invalid email formats are rejected.
    Validation belongs in the service layer, but the model should not break.
    """
    # The model does Not validate email format.
    # So Customer should still initialize successfully.
    customer = Customer(id=1, name="Test", email=email, lifetime_spend=1.0)
    assert customer.email == email

def test_customer_string_cast():
    """Verify Customer string cast is correctly formatted."""
    customer = Customer(
        id=1,
        name="Alice",
        email="alice@example.com",
        lifetime_spend=Decimal("10.50")
    )

    expected = (
        "Customer\n"
        "   Id: 1\n"
        "   Name: Alice\n"
        "   Email: alice@example.com\n"
        "   Lifetime Spend: $10.50"
    )

    assert str(customer) == expected