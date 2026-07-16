from models.drink import Drink
from collections import OrderedDict

class DrinkRepository:
    """A repository for managing in-memory storage of Drink instances.

    Attributes:
        _drinks (list[Drink]): The internal list storing all drink records.
    """

    def __init__(self):
        """Initializes an empty drink repository."""
        self._drinks: OrderedDict[int, Drink] = OrderedDict()

    def get_all(self) -> list[Drink]:
        """Retrieves all drinks currently stored in the repository.

        Returns:
            list[Drink]: A list containing all managed Drink objects.
        """
        return list(self._drinks.values())

   

    def get_by_id(self, id: int) -> Drink | None:
        """Find a drink by ID."""
        return self._drinks.get(id)

    def get_by_name(self, name: str) -> Drink | None:
        """Finds a drink by its name (case-insensitive, trimmed).

        Args:
            name (str): The name of the drink to look up.

        Returns:
            Drink | None: The matching Drink object if found; otherwise, None.
        """
        if name is None:
            return None
        lookup = name.strip().lower()
        for drink in self._drinks.values():
            if drink.name.strip().lower() == lookup:
                return drink
        return None

    def add(self, drink: Drink) -> Drink:
        """Adds a new drink record to the repository.

        Args:
            drink (Drink): The Drink instance to be added.

        Returns:
            Drink: The Drink instance that was successfully added.
        """
        self._drinks[drink.id] = drink
        return drink

    def update(self, key: int | str, drink: Drink) -> Drink | None:
        """Replaces an existing drink record with updated information.

        Args:
            id (Number): The numeric ID of the drink to update.
            drink (Drink): The new Drink instance to replace the old record.

        Returns:
            Drink | None: The updated Drink instance if the target ID was found
                and replaced; otherwise, None.
        """
        
        existing: Drink | None
        if isinstance(key, int):
            existing = self.get_by_id(key)
        else:
            existing = self.get_by_name(key)

        if existing is None:
            return None

        del self._drinks[existing.id]
        self._drinks[drink.id] = drink
        return drink

    def delete(self, key: int | str) -> bool:
        """Removes a drink record from the repository by its ID.

        Args:
            id (Number): The numeric ID of the drink to remove.

        Returns:
            bool: True if the drink was found and successfully deleted; False
                if no matching record was found.
        """
        if isinstance(key, int):
            drink = self.get_by_id(key)
        else:
            drink = self.get_by_name(key)

        if drink is None:
            return False
        del self._drinks[drink.id]
        return True