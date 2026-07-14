from numbers import Number
from models.drink import Drink

class DrinkRepository:
    """A repository for managing in-memory storage of Drink instances.

    Attributes:
        _drinks (list[Drink]): The internal list storing all drink records.
    """

    def __init__(self):
        """Initializes an empty drink repository."""
        self._drinks: list[Drink] = []

    def get_all(self) -> list[Drink]:
        """Retrieves all drinks currently stored in the repository.

        Returns:
            list[Drink]: A list containing all managed Drink objects.
        """
        return self._drinks

    def get_by_id(self, id: Number) -> Drink | None:
        """Finds a specific drink by its unique numerical identifier.

        Args:
            id (Number): The numeric ID of the drink to look up.

        Returns:
            Drink | None: The matching Drink object if found; otherwise, None.
        """
        return next((d for d in self._drinks if d.id == id), None)

    def add(self, drink: Drink) -> Drink:
        """Adds a new drink record to the repository.

        Args:
            drink (Drink): The Drink instance to be added.

        Returns:
            Drink: The Drink instance that was successfully added.
        """
        self._drinks.append(drink)
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
            self._drinks.remove(existing_drink)
            self._drinks.append(drink)
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
            self._drinks.remove(drink)
            return True
        return False