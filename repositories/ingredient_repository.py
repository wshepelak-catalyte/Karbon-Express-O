"""
Repository for managing Ingredient objects in memory.
"""

from models.ingredient import Ingredient

class IngredientRepository:
    """
    Provides CRUD operations for Ingredient objects stored in memory.

    Attributes:
        _ingredients (list[Ingredient]): Internal list storing Ingredient instances.
    """
    def __init__(self):
        """
        Initialize an empty IngredientRepository
        """
        self._ingredients: list[Ingredient] = []

    def get_all(self)->list[Ingredient]:
        """
        Retrieve all Ingredient objects in the repository.

        Returns:
            list[Ingredient]: A list of all stored ingredients.
        """
        return self._ingredients
    
    def get_by_name(self, name: str) -> Ingredient | None:
        """
        Retrieve an Ingredient by its name.

        Args:
            name (str): The name of the ingredient to search for.

        Returns:
            Ingredient | None: The matching Ingredient, or None if not found.
        """
        return next((i for i in self._ingredients if i.name == name), None)
    
    def add(self, ingredient : Ingredient) -> Ingredient:
        """
        Add a new Ingredient to the repository.

        Args:
            ingredient (Ingredient): The ingredient to add.

        Returns:
            Ingredient: The added ingredient.
        """
        self._ingredients.append(ingredient)
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
        for iterator, _ingredient in enumerate(self._ingredients):
            if _ingredient.name == name:
                self._ingredients[iterator] = ingredient
                return ingredient
            else:
                return None

    def delete(self, name: str) -> bool:
        """
        Delete an Ingredient by name.

        Args:
            name (str): The name of the ingredient to delete.

        Returns:
            bool: True if deletion occurred, False otherwise.
        """
        delete_occured = False
        for iterator, _ingredient in enumerate(self._ingredients):
            if _ingredient.name == name:
                del self._ingredients[iterator]
                delete_occured = True
        return delete_occured
