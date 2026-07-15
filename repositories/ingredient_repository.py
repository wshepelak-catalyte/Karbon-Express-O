"""
Repository for managing Ingredient objects in memory.
"""

from models.ingredient import Ingredient
from collections import OrderedDict


class IngredientRepository:
    """
    Provides CRUD operations for Ingredient objects stored in memory.

    Attributes:
        _ingredients (OrderedDict[str, Ingredient]): Internal dictionary storing Ingredient instances.
    """
    def __init__(self):
        """
        Initialize an empty IngredientRepository
        """
        self._ingredients = OrderedDict()

    def get_all(self)->list[Ingredient]:
        """
        Retrieve all Ingredient objects in the repository.

        Returns:
            list[Ingredient]: A list of all stored ingredients.
        """
        return list(self._ingredients.values())
    
    def get_by_name(self, name: str) -> Ingredient | None:
        """
        Retrieve an Ingredient by its name.

        Args:
            name (str): The name of the ingredient to search for.

        Returns:
            Ingredient | None: The matching Ingredient, or None if not found.
        """
        return self._ingredients.get(name)
    
    def add(self, ingredient : Ingredient) -> Ingredient:
        """
        Add a new Ingredient to the repository.

        Args:
            ingredient (Ingredient): The ingredient to add.

        Returns:
            Ingredient: The added ingredient.
        """
        self._ingredients[ingredient.name] = ingredient
        return ingredient

    def update(self, name : str, ingredient : Ingredient) -> Ingredient | None:
        """
        Update an existing Ingredient by name.

        Args:
            name (str): The name of the ingredient to update.
            ingredient (Ingredient): The new ingredient data.

        Returns:
            Ingredient | None: The updated ingredient, or None if not found.
        """
        if self._ingredients.get(name) is None:
            return None
        self._ingredients[name] = ingredient
        return ingredient

    def delete(self, name: str) -> bool:
        """
        Delete an Ingredient by name.

        Args:
            name (str): The name of the ingredient to delete.

        Returns:
            bool: True if deletion occurred, False otherwise.
        """
        if self._ingredients.get(name) is None:
            return False
        del self._ingredients[name]
        return True
