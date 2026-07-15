from models.baked_good import BakedGood
from repositories.baked_good_repository import BakedGoodRepository


class BakedGoodService:
    """Service layer for baked good operations."""

    def __init__(self, repository: BakedGoodRepository) -> None:
        self.repository = repository

    def is_available(self, name: str, vendor_name: str) -> bool:
        """Return whether a baked good is currently available for sale."""
        good = self.repository.get_by_name(name, vendor_name)
        return good is not None and good.available

    def mark_unavailable(self, name: str, vendor_name: str) -> BakedGood:
        """Mark a baked good as unavailable."""
        good = self.repository.get_by_name(name, vendor_name)
        if good is None:
            raise ValueError(f"Baked good '{name}' for vendor '{vendor_name}' not found.")
        good.available = False
        return good

    def mark_available(self, name: str, vendor_name: str) -> BakedGood:
        """Mark a baked good as available."""
        good = self.repository.get_by_name(name, vendor_name)
        if good is None:
            raise ValueError(f"Baked good '{name}' for vendor '{vendor_name}' not found.")
        good.available = True
        return good

    def is_name_taken(self, name: str, vendor_name: str, exclude_id: int | None = None) -> bool:
        """Return True when another baked good already uses the same name for that vendor."""
        normalized_name = name.strip().lower()
        normalized_vendor = vendor_name.strip().lower()
        for good in self.repository.all():
            if good.name.lower() != normalized_name:
                continue
            if good.vendor_name.lower() != normalized_vendor:
                continue
            if exclude_id is not None and good.id == exclude_id:
                continue
            return True
        return False

    def add_baked_good(self, baked_good: BakedGood) -> BakedGood:
        """Add a baked good after validating that the name/vendor combination is unique."""
        if self.is_name_taken(baked_good.name, baked_good.vendor_name):
            raise ValueError(
                f"Baked good '{baked_good.name}' for vendor '{baked_good.vendor_name}' already exists."
            )
        return self.repository.add(baked_good)

    def update_baked_good(self, baked_good: BakedGood) -> BakedGood:
        """Update a baked good after validating that the name/vendor combination is still unique."""
        existing = self.repository.get_by_name(baked_good.name, baked_good.vendor_name)
        if existing is not None and existing.id != baked_good.id:
            raise ValueError(
                f"Baked good '{baked_good.name}' for vendor '{baked_good.vendor_name}' already exists."
            )
        updated = self.repository.update(baked_good.name, baked_good.vendor_name, baked_good)
        if updated is None:
            raise ValueError(
                f"Baked good '{baked_good.name}' for vendor '{baked_good.vendor_name}' not found."
            )
        return updated

    def delete_baked_good(self, name: str, vendor_name: str) -> bool:
        """Delete a baked good by name and vendor."""
        return self.repository.delete(name, vendor_name)
