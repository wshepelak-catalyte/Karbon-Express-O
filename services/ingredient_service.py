from repositories.ingredient_repository import IngredientRepository
from models.ingredient import Ingredient
from decimal import Decimal


class IngredientService:
    """
    Service layer responsible for managing ingredient data and enforcing validation
    rules for ingredients used in drink preparation.

    This class provides creation, retrieval, updating, and deletion operations
    while maintaining internal ID allocation logic for ingredients.
    """

    def __init__(self):
        """
        Initialize the IngredientService.

        Creates an internal repository instance, a list for tracking reusable
        ingredient IDs, and a counter for assigning new unique IDs.
        """
        self._repository = IngredientRepository()
        self._empty_ids = []
        self._next_id = 0

    def create_ingredient(
                self, 
                name : str,
                purchasing_cost : float | Decimal,
                unit_amount : float,
                unit_of_measure : str
            ):
        """
        Create a new ingredientand store it in the repository.

        Parameters
        ----------
        name : str
            The name of the ingredient.
        purchasing_cost : float | Decimal
            The cost to purchase the ingredient.
        unit_amount : float
            The amount of the ingredient per unit.
        unit_of_measure : str
            The unit of measurement (e.g., 'grams', 'onces').

        Notes
        -----
        - If previously deleted ingredient IDs exist, the lowest available ID
          is reused.
        - Otherwise, a new sequential ID is assigned.
        """

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
        """
        Retrieve all ingredients as structured tuples.

        Returns
        -------
        list[Ingredient]
            A list of Ingredient objects.
        """
        return self._repository.get_all()
    
    def get_ingredient_by_name(self, name : str) -> Ingredient:
        """
        Retrieve a single ingredient by its name.

        Parameters
        ----------
        name : str
            The name of the ingredient to retrieve.

        Returns
        -------
        Ingredient
            The ingredient matching the provided name.

        Raises
        ------
        LookupError
            If no ingredient with the given name exists.
        """
        returned_ingredient = self._repository.get_by_name(name)
        if returned_ingredient is None:
            raise #ingredient not found
        return returned_ingredient
    
    def update_ingredient(
                self, 
                name : str,
                purchasing_cost : float | Decimal,
                unit_amount : float,
                unit_of_measure : str
            ):
        """
        Update an existing ingredient's stored attributes.

        Parameters
        ----------
        name : str
            The name of the ingredient to update.
        purchasing_cost : float | Decimal
            The updated purchasing cost.
        unit_amount : float
            The updated unit amount.
        unit_of_measure : str
            The updated unit of measurement.

        Raises
        ------
        LookupError
            If the ingredient does not exist in the repository.
        """
        """
        validation
        """
        old_ingredient_id = self._repository.get_by_name(name).id
        updated_ingredient = Ingredient(
            id=old_ingredient_id,
            name=name,
            purchasing_cost=purchasing_cost,
            unit_amount=unit_amount,
            unit_of_measure=unit_of_measure
        )

        self._repository.update(name, updated_ingredient)

    def delete_ingredient(self, name : str):
        """
        Delete an ingredient from the repository.

        Parameters
        ----------
        name : str
            The name of the ingredient to delete.

        Raises
        ------
        LookupError
            If the ingredient does not exist.

        Notes
        -----
        The deleted ingredient's ID is stored for reuse in future creations.
        """
        """
        Validation
        """
        self._empty_ids.append(self._repository.get_by_name(name).id)
        self._repository.delete(name)
    