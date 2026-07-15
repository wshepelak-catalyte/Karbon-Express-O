from numbers import Number
from models.drink import Drink
from collections import OrderedDict

class DrinkRepository:
    """A repository for managing in-memory storage of Drink instances.

    Attributes:
        _drinks (list[Drink]): The internal list storing all drink records.
    """

    def __init__(self):
        """Initializes an empty drink repository."""
        self._drinks: list[OrderedDict[str, Drink]] = []

    def get_all(self) -> list[Drink]:
        """Retrieves all drinks currently stored in the repository.

        Returns:
            list[Drink]: A list containing all managed Drink objects.
        """
        return [drink for drink_dict in self._drinks for drink in drink_dict.values()]

    def get_by_id(self, id: Number) -> Drink | None:
        """Finds a specific drink by its unique numerical identifier.

        Args:
            id (Number): The numeric ID of the drink to look up.

        Returns:
            Drink | None: The matching Drink object if found; otherwise, None.
        """
        return next((d for drink_dict in self._drinks for d in drink_dict.values() if d.id == id), None)

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
        return next((d for drink_dict in self._drinks for d in drink_dict.values() if isinstance(d.name, str) and d.name.strip().lower() == lookup), None)

    def add(self, drink: Drink) -> Drink:
        """Adds a new drink record to the repository.

        Args:
            drink (Drink): The Drink instance to be added.

        Returns:
            Drink: The Drink instance that was successfully added.
        """
        self._drinks.append(OrderedDict([(drink.id, drink)]))
        return drink

    def update(self, id: Number, drink: Drink) -> Drink | None:
        """Replaces an existing drink record with updated information.

        Args:
            id (Number): The numeric ID of the drink to update.
            drink (Drink): The new Drink instance to replace the old record.

        Returns:
            Drink | None: The updated Drink instance if the target ID was found
                and replaced; otherwise, None.
        """
        existing_drink = self.get_by_id(id)
        if existing_drink:
            self._drinks.remove(OrderedDict([(existing_drink.id, existing_drink)]))
            self._drinks.append(OrderedDict([(drink.id, drink)]))

            return drink
        return None

    def delete(self, id: Number) -> bool:
        """Removes a drink record from the repository by its ID.

        Args:
            id (Number): The numeric ID of the drink to remove.

        Returns:
            bool: True if the drink was found and successfully deleted; False
                if no matching record was found.
        """
        drink = self.get_by_id(id)
        if drink:
            self._drinks.remove(OrderedDict([(drink.id, drink)]))
            
            return True
        return False