"""
Tests for the BakedGoodRepository class.
"""

from decimal import Decimal

import pytest

from models.baked_good import BakedGood
from repositories.baked_good_repository import BakedGoodRepository


def make_baked_good(id_value: int, name: str, vendor_name: str, allergens: list[str]) -> BakedGood:
    return BakedGood(
        id=id_value,
        name=name,
        vendor_name=vendor_name,
        allergens=allergens,
        purchasing_cost=2.50,
        markup_percentage=0.20,
    )


def test_add_and_all_returns_added_items():
    """Ensure baked goods are stored and returned from the repository."""
    repo = BakedGoodRepository()
    croissant = make_baked_good(1, "Croissant", "Bakery A", ["gluten"])
    muffin = make_baked_good(2, "Muffin", "Bakery A", ["milk", "eggs"])

    repo.add(croissant)
    repo.add(muffin)

    all_goods = repo.all()

    assert len(all_goods) == 2
    assert all_goods[0].name == "Croissant"
    assert all_goods[1].name == "Muffin"


def test_find_by_name_and_vendor_filters_correctly():
    """Ensure name lookup can be scoped to a vendor."""
    repo = BakedGoodRepository()
    croissant_a = make_baked_good(1, "Croissant", "Bakery A", ["gluten"])
    croissant_b = make_baked_good(2, "Croissant", "Bakery B", ["gluten"])

    repo.add(croissant_a)
    repo.add(croissant_b)

    assert repo.find_by_name("Croissant", "Bakery A") is croissant_a
    assert repo.find_by_name("Croissant", "Bakery B") is croissant_b
    assert repo.find_by_name("Croissant") is croissant_a


def test_find_by_vendor_and_allergen_returns_matching_items():
    """Ensure repository filtering works for vendor and allergen queries."""
    repo = BakedGoodRepository()
    croissant = make_baked_good(1, "Croissant", "Bakery A", ["gluten"])
    muffin = make_baked_good(2, "Muffin", "Bakery A", ["milk", "eggs"])
    cookie = make_baked_good(3, "Cookie", "Bakery B", ["gluten", "nuts"])

    repo.add(croissant)
    repo.add(muffin)
    repo.add(cookie)

    assert repo.find_by_vendor("Bakery A") == [croissant, muffin]
    assert repo.find_by_allergen("gluten") == [croissant, cookie]


def test_update_and_remove_change_repository_state():
    """Ensure updates and removals affect the stored baked goods."""
    repo = BakedGoodRepository()
    croissant = make_baked_good(1, "Croissant", "Bakery A", ["gluten"])
    repo.add(croissant)

    updated = BakedGood(
        id=10,
        name="Croissant",
        vendor_name="Bakery A",
        allergens=["gluten", "milk"],
        purchasing_cost=3.00,
        markup_percentage=0.25,
    )

    repo.update(updated)
    assert repo.find_by_name("Croissant", "Bakery A") is updated
    assert repo.find_by_name("Croissant", "Bakery A").allergens == ["gluten", "milk"]

    repo.remove("Croissant", "Bakery A")
    assert repo.all() == []


def test_duplicate_add_raises_value_error():
    """Ensure duplicate baked goods cannot be added twice for the same vendor."""
    repo = BakedGoodRepository()
    croissant = make_baked_good(1, "Croissant", "Bakery A", ["gluten"])

    repo.add(croissant)

    with pytest.raises(ValueError):
        repo.add(croissant)
