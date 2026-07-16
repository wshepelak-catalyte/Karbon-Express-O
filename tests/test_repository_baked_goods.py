"""
Tests for the BakedGoodRepository class.
"""

from decimal import Decimal

import pytest

from models.baked_good import BakedGood
from repositories.baked_good_repository import BakedGoodRepository


def make_baked_good(
    id_value: int,
    name: str,
    vendor_name: str,
    allergens: list[str],
    purchasing_cost: Decimal | float = Decimal("2.50"),
    markup_percentage: Decimal | float = Decimal("0.20"),
) -> BakedGood:
    return BakedGood(
        id=id_value,
        name=name,
        vendor_name=vendor_name,
        allergens=allergens,
        purchasing_cost=purchasing_cost,
        markup_percentage=markup_percentage,
    )


def test_add_and_get_all_returns_added_items():
    """Ensure baked goods are stored and returned from the repository."""
    repo = BakedGoodRepository()
    croissant = make_baked_good(1, "Croissant", "Bakery A", ["gluten"])
    muffin = make_baked_good(2, "Muffin", "Bakery A", ["milk", "eggs"])

    repo.add(croissant)
    repo.add(muffin)

    all_goods = repo.get_all()

    assert len(all_goods) == 2
    assert all_goods[0].name == "Croissant"
    assert all_goods[1].name == "Muffin"


def test_get_by_name_and_vendor_filters_correctly():
    """Ensure name lookup can be scoped to a vendor."""
    repo = BakedGoodRepository()
    croissant_a = make_baked_good(1, "Croissant", "Bakery A", ["gluten"])
    croissant_b = make_baked_good(2, "Croissant", "Bakery B", ["gluten"])

    repo.add(croissant_a)
    repo.add(croissant_b)

    assert repo.get_by_name("Croissant", "Bakery A") is croissant_a
    assert repo.get_by_name("Croissant", "Bakery B") is croissant_b
    assert repo.get_by_name("Croissant") is croissant_a


def test_get_by_vendor_and_allergen_returns_matching_items():
    """Ensure repository filtering works for vendor and allergen queries."""
    repo = BakedGoodRepository()
    croissant = make_baked_good(1, "Croissant", "Bakery A", ["gluten"])
    muffin = make_baked_good(2, "Muffin", "Bakery A", ["milk", "eggs"])
    cookie = make_baked_good(3, "Cookie", "Bakery B", ["gluten", "nuts"])

    repo.add(croissant)
    repo.add(muffin)
    repo.add(cookie)

    assert repo.get_by_vendor("Bakery A") == [croissant, muffin]
    assert repo.get_by_allergen("gluten") == [croissant, cookie]


def test_update_and_delete_change_repository_state():
    """Ensure updates and deletions affect the stored baked goods."""
    repo = BakedGoodRepository()
    croissant = make_baked_good(1, "Croissant", "Bakery A", ["gluten"])
    repo.add(croissant)

    updated = BakedGood(
        id=10,
        name="Croissant",
        vendor_name="Bakery A",
        allergens=["gluten", "milk"],
        purchasing_cost=Decimal("3.00"),
        markup_percentage=Decimal("0.25"),
    )

    repo.update("Croissant", "Bakery A", updated)
    assert repo.get_by_name("Croissant", "Bakery A") is updated
    assert repo.get_by_name("Croissant", "Bakery A").allergens == ["gluten", "milk"]

    repo.delete("Croissant", "Bakery A")
    assert repo.get_all() == []


def test_duplicate_add_raises_value_error():
    """Ensure duplicate baked goods cannot be added twice for the same vendor."""
    repo = BakedGoodRepository()
    croissant = make_baked_good(1, "Croissant", "Bakery A", ["gluten"])

    repo.add(croissant)

    with pytest.raises(ValueError):
        repo.add(croissant)


def test_find_by_name_and_remove_aliases_work():
    """Ensure compatibility aliases route to the underlying repository behavior."""
    repo = BakedGoodRepository()
    croissant = make_baked_good(1, "Croissant", "Bakery A", ["gluten"])
    repo.add(croissant)

    assert repo.find_by_name("Croissant", "Bakery A") is croissant
    assert repo.remove("Croissant", "Bakery A") is True
    assert repo.get_all() == []


def test_update_missing_item_returns_none():
    """Ensure updates on missing entries return None instead of mutating state."""
    repo = BakedGoodRepository()
    updated = make_baked_good(99, "Croissant", "Bakery A", ["gluten"])

    assert repo.update("Croissant", "Bakery A", updated) is None
    assert repo.get_all() == []
