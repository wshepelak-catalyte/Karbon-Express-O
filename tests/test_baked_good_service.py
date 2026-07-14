from decimal import Decimal

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
