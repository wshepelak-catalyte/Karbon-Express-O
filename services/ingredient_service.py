from repositories.ingredient_repository import IngredientRepository
from repositories.ingredient_availability_repository import IngredientAvailabilityRepository
from repositories.drink_repository import DrinkRepository
from models.ingredient import Ingredient


class IngredientService:
    """Service layer for ingredient availability and drink availability rules."""

    def __init__(
        self,
        repository: IngredientRepository,
        availability_repository: IngredientAvailabilityRepository,
        drink_repository: DrinkRepository,
    ):
        self._repository = repository
        self._availability_repository = availability_repository
        self._drink_repository = drink_repository

    def new_ingredient(self, ingredient: Ingredient) -> Ingredient:
        if self._repository.get_by_name(ingredient.name) is not None:
            return self._repository.get_by_name(ingredient.name)
        self._repository.add(ingredient)
        self._availability_repository.mark_available(ingredient.name)
        return ingredient

    def add_ingredient(self, ingredient: Ingredient) -> Ingredient:
        return self.new_ingredient(ingredient)

    def mark_unavailable(self, ingredient_name: str) -> None:
        self._availability_repository.mark_unavailable(ingredient_name)
        self._update_drink_availability()

    def mark_available(self, ingredient_name: str) -> None:
        self._availability_repository.mark_available(ingredient_name)
        self._update_drink_availability()

    def _update_drink_availability(self) -> None:
        for drink in self._drink_repository.get_all():
            drink.is_available = all(
                self._availability_repository.is_available(ingredient.name)
                for ingredient in drink.ingredients
            )

    def is_drink_available(self, drink_id: int) -> bool:
        drink = self._drink_repository.get_by_id(drink_id)
        if drink is None:
            return False
        return getattr(drink, "is_available", True)
