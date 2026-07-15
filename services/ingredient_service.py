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

<<<<<<< HEAD
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
=======
    def create_ingredient(self, ingredient : Ingredient):
        pass

    def get_all_ingredients(self) -> list[Ingredient]:
        return self._repository.get_all()
    
    def get_ingredient_by_name(self, name : str) -> Ingredient:
        returned_ingredient = self._repository.get_by_name(name)
        if returned_ingredient is None:
            raise #ingredient not found
        return returned_ingredient
    
    def update_ingredient(self, ):
        pass

    def delete_ingredient(self, name : str) -> Ingredient | None:
        deleted_ingredient = self._repository.get_by_name(name)
        if self._repository.delete(name):
            return deleted_ingredient
        else:
            return None
    
    
>>>>>>> b4081b64c9b18090a23187f51ad6173090490730
