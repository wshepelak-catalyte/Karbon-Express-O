from collections import OrderedDict

from models.baked_good import BakedGood


class BakedGoodRepository:
    """In-memory repository for BakedGood domain objects."""

    def __init__(self) -> None:
        self._goods = OrderedDict()

    def all(self) -> list[BakedGood]:
        """Return all baked goods."""
        return self.get_all()

    def get_all(self) -> list[BakedGood]:
        """Return all baked goods."""
        return_list = []
        for key, val in self._goods.items():
            return_list.append(val)
        return return_list

    def find_by_name(self, name: str, vendor_name: str | None = None) -> BakedGood | None:
        """Find a baked good by name, optionally filtering by vendor."""
        if vendor_name is None:
            return next((good for good in self._goods.values() if good.name == name), None)
        return self.get_by_name(name, vendor_name)

    def get_by_name(self, name: str, vendor_name: str | None = None) -> BakedGood | None:
        """Find a baked good by name, optionally filtering by vendor."""
        if vendor_name is None:
            return self.find_by_name(name)
        key = self._make_key(name, vendor_name)
        return self._goods.get(key)

    def find_by_vendor(self, vendor_name: str) -> list[BakedGood]:
        """Return all baked goods for a given vendor."""
        return self.get_by_vendor(vendor_name)

    def get_by_vendor(self, vendor_name: str) -> list[BakedGood]:
        """Return all baked goods for a given vendor."""
        return [good for good in self._goods.values() if good.vendor_name == vendor_name]

    def find_by_allergen(self, allergen: str) -> list[BakedGood]:
        """Return baked goods that contain a given allergen."""
        return self.get_by_allergen(allergen)

    def get_by_allergen(self, allergen: str) -> list[BakedGood]:
        """Return baked goods that contain a given allergen."""
        return [good for good in self._goods.values() if allergen in good.allergens]

    def add(self, baked_good: BakedGood) -> BakedGood:
        """Add a baked good to the repository."""
        if self.get_by_name(baked_good.name, baked_good.vendor_name) is not None:
            raise ValueError(
                f"Baked good '{baked_good.name}' for vendor '{baked_good.vendor_name}' already exists."
            )
        key = self._make_key(baked_good.name, baked_good.vendor_name)
        self._goods[key] = baked_good
        return baked_good

    def update(self, name: str | BakedGood, vendor_name: str | None = None, baked_good: BakedGood | None = None) -> BakedGood | None:
        """Replace an existing baked good with an updated instance."""
        if isinstance(name, BakedGood):
            baked_good = name
            name = baked_good.name
            vendor_name = baked_good.vendor_name
        elif baked_good is None:
            raise TypeError("update() missing required argument: baked_good")

        key = self._make_key(name, vendor_name)
        if key not in self._goods:
            return None
        self._goods[key] = baked_good
        return baked_good

    def delete(self, name: str, vendor_name: str | None = None) -> bool:
        """Remove a baked good from the repository."""
        key = self._make_key(name, vendor_name)
        if key not in self._goods:
            return False
        del self._goods[key]
        return True

    def remove(self, name: str, vendor_name: str | None = None) -> bool:
        """Backward-compatible alias for delete."""
        return self.delete(name, vendor_name)

    def _make_key(self, name: str, vendor_name: str | None = None) -> str:
        return f"{name.lower()}::{(vendor_name or '').lower()}"