# services/drink_service.py
from decimal import Decimal
from repositories.drink_repository import DrinkRepository
from models.ingredient import Ingredient
from models.drink import Drink
from exceptions import DuplicateDrinkError, DrinkNotFoundError

class DrinkService:
    """Service layer for drink operations."""

    def __init__(self) -> None:
        """Initialize the DrinkService with an internal repository and ID management."""
        self._repository = DrinkRepository()
        self._empty_ids = []
        self._next_id = 0

    def create_drink(self,
                     name: str,
                     ingredients: list[Ingredient],
                     cost_to_produce: Decimal,
                     markup_percentage: Decimal,
                     sale_price: Decimal,
                     is_available: bool = False) -> None:
        """
        Create a new drink and store it in the repository.
        """

        if self._repository.get_by_name(name) is not None:
            raise DuplicateDrinkError(f"Drink '{name}' already exists.")
       
        created_drink_id = None
       
        if len(self._empty_ids) == 0:
            created_drink_id = self._next_id
            self._next_id += 1
        else:
            created_drink_id = self._empty_ids.pop()
        
        created_drink = Drink(
                id=created_drink_id,
                name=name,
                cost_to_produce=cost_to_produce,
                markup_percentage=markup_percentage,
                sale_price=sale_price,
                is_available=is_available,
                ingredients=ingredients
            )
        self._repository.add(created_drink)

    def get_all_drinks(self) -> list[Drink]:
        """
        Retrieve all drinks
        """
        return self._repository.get_all()
    
    def get_available_drinks(self) -> list[Drink]:
        """
        Retrieve all drinks that are available.
        """
        return [drink for drink in self._repository.get_all() if drink.is_available]
    
    def get_drink_by_name(self, name: str) -> Drink:
        """
        Retrieve a single drink by its name.

        Parameters
        ----------
        name : str
            The name of the drink to retrieve.

        Returns
        -------
        Drink
            The drink matching the provided name.

        Raises
        ------
        DrinkNotFoundError
            If no drink with the given name exists.
        """
        drink = self._repository.get_by_name(name)
        if drink is None:
            raise DrinkNotFoundError(f"No drink found with name '{name}'")
        return drink
    
    def update_drink(self, name: str, ingredients: list[Ingredient], cost_to_produce: Decimal, markup_percentage: Decimal, sale_price: Decimal, is_available: bool) -> None:
        """
        Update an existing drink's details.

        Parameters
        ----------
        drink_id : int
            The ID of the drink to update.
        name : str
            The new name for the drink.
        ingredients : list[Ingredient]
            The new list of ingredients for the drink.
        cost_to_produce : Decimal
            The new cost to produce the drink.
        markup_percentage : Decimal
            The new markup percentage for the drink.
        sale_price : Decimal
            The new sale price for the drink.
        is_available : bool
            The new availability status for the drink.

        Raises
        ------
        DuplicateDrinkError
            If another drink with the same name already exists (case-insensitive).
        DrinkNotFoundError
            If no drink with the given ID exists.
        """
        existing_drink = self._repository.get_by_name(name)
        if existing_drink is None:
            raise DrinkNotFoundError(f"No drink found with Name '{name}'")
        
        if self.is_name_taken(name, exclude_id=existing_drink.id):
            raise DuplicateDrinkError(f"Drink '{name}' already exists.")
        
        updated_drink = Drink(
            id=existing_drink.id,
            name=name,
            ingredients=ingredients,
            cost_to_produce=cost_to_produce,
            markup_percentage=markup_percentage,
            sale_price=sale_price,
            is_available=is_available
        )
        
        self._repository.update(name, updated_drink)

    def delete_drink(self, name: str) -> None:
        """
        Delete a drink by its name.

        Parameters
        ----------
        name : str
            The name of the drink to delete.

        Raises
        ------
        DrinkNotFoundError
            If no drink with the given name exists.
        """
        deleted_drink = self._repository.get_by_name(name)
        if deleted_drink is None:
            raise DrinkNotFoundError(f"No drink found with name '{name}'")
        self._empty_ids.append(deleted_drink.id)
        self._repository.delete(name)

    def is_name_taken(self, name: str, exclude_id: int | None = None) -> bool:
        """Return True when another drink already uses the same name."""
        normalized_name = name.strip().lower()
        for drink in self._repository.get_all():
            if drink.name.lower() != normalized_name:
                continue
            if exclude_id is not None and drink.id == exclude_id:
                continue
            return True
        return False