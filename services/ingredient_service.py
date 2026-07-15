from repositories.ingredient_repository import IngredientRepository
from models.ingredient import Ingredient
from decimal import Decimal


class IngredientService:
    """Service layer for ingredient availability and drink availability rules."""

    def __init__(self):
        self._repository = IngredientRepository()
        self._empty_ids = []
        self._next_id = 0

    def create_ingredient(self, name : str, purchasing_cost : float | Decimal, unit_amount : float, unit_of_measure : str):
        """
        Validation
        """
        created_ingredient_id = None
        if len(self._empty_ids) == 0:
            created_ingredient_id = self._next_id
            self._next_id += 1
        else:
            created_ingredient_id = self._empty_ids.pop()
        
        created_ingredient = Ingredient(
                id=created_ingredient_id,
                name=name,
                purchasing_cost=purchasing_cost,
                unit_amount=unit_amount,
                unit_of_measure=unit_of_measure
            )
        self._repository.add(created_ingredient)

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
    