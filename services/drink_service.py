from repositories.drink_repository import DrinkRepository


class DrinkService:
    """Service layer for drink operations."""

    def __init__(self, repository: DrinkRepository) -> None:
        self.repository = repository

    def is_name_taken(self, name: str, exclude_id: int | None = None) -> bool:
        """Return True when another drink already uses the same name."""
        normalized_name = name.strip().lower()
        for drink in self.repository.get_all():
            if drink.name.lower() != normalized_name:
                continue
            if exclude_id is not None and drink.id == exclude_id:
                continue
            return True
        return False