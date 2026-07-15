from repositories.ingredient_repository import IngredientRepository
from models.ingredient import Ingredient


class IngredientService:

    def __init__(self, repository : IngredientRepository):
        self._repository = repository

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
    
    