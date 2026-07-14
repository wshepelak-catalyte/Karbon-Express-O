from repositories.ingredient_repository import IngredientRepository
from models.ingredient import Ingredient


class IngredientService:

    def __init__(self, repository : IngredientRepository):
        self._repository = repository

    def new_ingredient(self, ingredient : Ingredient) -> Ingredient:
        if self._repository.get_by_name(ingredient.name) is not None:
            raise DuplicateIngredientError(f"Ingredient \'{ingredient.name}\' already exists.")
        return self._repository.add(ingredient)
    