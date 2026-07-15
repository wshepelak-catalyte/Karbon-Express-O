from decimal import Decimal

import pytest

from models.baked_good import BakedGood
from repositories.baked_good_repository import BakedGoodRepository
from services.baked_good_service import BakedGoodService


def make_baked_good(id_value: int, name: str, vendor_name: str) -> BakedGood:
    return BakedGood(
        id=id_value,
        name=name,
        vendor_name=vendor_name,
        allergens=["gluten"],
        purchasing_cost=Decimal("2.50"),
        markup_percentage=Decimal("0.20"),
    )


def test_name_duplicate_validation_detects_existing_name_for_vendor():
    repository = BakedGoodRepository()
    service = BakedGoodService(repository)
    repository.add(make_baked_good(1, "Croissant", "Bakery A"))

    assert service.is_name_taken("Croissant", "Bakery A") is True
    assert service.is_name_taken("croissant", "bakery a") is True


def test_name_duplicate_validation_ignores_same_item_when_updating():
    repository = BakedGoodRepository()
    service = BakedGoodService(repository)
    repository.add(make_baked_good(1, "Croissant", "Bakery A"))

    assert service.is_name_taken("Croissant", "Bakery A", exclude_id=1) is False
    assert service.is_name_taken("Muffin", "Bakery A") is False


def test_name_duplicate_validation_treats_whitespace_and_case_as_equal():
    repository = BakedGoodRepository()
    service = BakedGoodService(repository)
    repository.add(make_baked_good(1, "Croissant", "Bakery A"))

    assert service.is_name_taken("  CROISSANT  ", "  bakery a  ") is True


def test_add_baked_good_raises_for_duplicate_name_and_vendor():
    repository = BakedGoodRepository()
    service = BakedGoodService(repository)
    service.add_baked_good(make_baked_good(1, "Croissant", "Bakery A"))

    with pytest.raises(ValueError):
        service.add_baked_good(make_baked_good(2, "Croissant", "Bakery A"))


def test_update_baked_good_raises_for_conflicting_name_and_vendor():
    repository = BakedGoodRepository()
    service = BakedGoodService(repository)
    existing = make_baked_good(1, "Croissant", "Bakery A")
    repository.add(existing)

    with pytest.raises(ValueError):
        service.update_baked_good(make_baked_good(2, "Croissant", "Bakery A"))


def test_update_baked_good_raises_when_target_does_not_exist():
    repository = BakedGoodRepository()
    service = BakedGoodService(repository)

    with pytest.raises(ValueError):
        service.update_baked_good(make_baked_good(1, "Croissant", "Bakery A"))


def test_baked_good_defaults_to_available_and_can_be_toggled():
    repository = BakedGoodRepository()
    service = BakedGoodService(repository)
    good = make_baked_good(1, "Croissant", "Bakery A")
    repository.add(good)

    assert good.available is True
    assert service.is_available("Croissant", "Bakery A") is True

    service.mark_unavailable("Croissant", "Bakery A")
    assert good.available is False
    assert service.is_available("Croissant", "Bakery A") is False

    service.mark_available("Croissant", "Bakery A")
    assert good.available is True
    assert service.is_available("Croissant", "Bakery A") is True
