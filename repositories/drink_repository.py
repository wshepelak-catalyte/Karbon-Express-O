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
        self._drinks = OrderedDict()

    def get_all(self) -> list[Drink]:
        """Retrieves all drinks currently stored in the repository.

        Returns:
            list[Drink]: A list containing all managed Drink objects.
        """
        return list(self._drinks.values())

   

    def get_by_name(self, name: str) -> Drink | None:
        """Finds a drink by its name (case-insensitive, trimmed).

        Args:
            name (str): The name of the drink to look up.

        Returns:
            Drink | None: The matching Drink object if found; otherwise, None.
        """
       
        return self._drinks.get(name)

    def add(self, drink: Drink) -> Drink:
        """Adds a new drink record to the repository.

        Args:
            drink (Drink): The Drink instance to be added.

        Returns:
            Drink: The Drink instance that was successfully added.
        """
        self._drinks[drink.name] = drink
        return drink

    def update(self, name: str, drink: Drink) -> Drink | None:
        """Replaces an existing drink record with updated information.

        Args:
            id (Number): The numeric ID of the drink to update.
            drink (Drink): The new Drink instance to replace the old record.

        Returns:
            Drink | None: The updated Drink instance if the target ID was found
                and replaced; otherwise, None.
        """
        
        if self._drinks.get[name] is None:
            return None
        
        self._drinks[name] = drink
        return drink

    def delete(self, name: str) -> bool:
        """Removes a drink record from the repository by its ID.

        Args:
            id (Number): The numeric ID of the drink to remove.

        Returns:
            bool: True if the drink was found and successfully deleted; False
                if no matching record was found.
        """
        drink = self.get_by_name(name)
        if drink is None:
            return False
        del self._drinks[name]
        return True