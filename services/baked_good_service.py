from repositories.baked_good_repository import BakedGoodRepository


class BakedGoodService:
    """Service layer for baked good operations."""

    def __init__(self, repository: BakedGoodRepository) -> None:
        self.repository = repository

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
