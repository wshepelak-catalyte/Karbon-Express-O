from models.purchase import Purchase
from collections import OrderedDict


class PurchaseRepository:
    """A repository for managing in-memory storage of Purchase records.

    Attributes:
        _purchases (OrderedDict[int, Purchase]): The internal ordered dictionary storing all purchase transactions.
    """

    def __init__(self):
        """Initializes an empty purchase repository."""
        self._purchases = OrderedDict()

    def get_all(self) -> list[Purchase]:
        """Retrieves all purchase transactions currently stored in the repository.

        Returns:
            list[Purchase]: A list containing all managed Purchase objects.
        """
        return list(self._purchases.values())

    def get_by_id(self, id: int) -> Purchase | None:
        """Finds a specific purchase record by its unique numerical identifier.

        Args:
            id (int): The numeric ID of the purchase transaction to look up.

        Returns:
            Purchase | None: The matching Purchase object if found; otherwise, None.
        """
        return self._purchases.get(id)

    def add(self, purchase: Purchase) -> Purchase:
        """Adds a new purchase transaction record to the repository.

        Args:
            purchase (Purchase): The Purchase instance to be recorded.

        Returns:
            Purchase: The Purchase instance that was successfully added.
        """
        self._purchases[purchase.id] = purchase
        return purchase

    def update(self, id: int, purchase: Purchase) -> Purchase | None:
        """Replaces an existing purchase transaction with updated information.

        Args:
            id (int): The numeric ID of the purchase record to update.
            purchase (Purchase): The new Purchase instance to replace the old record.

        Returns:
            Purchase | None: The updated Purchase instance if the target ID was found
                and replaced; otherwise, None.
        """
        if self._purchases.get(id) is None:
            return None
        self._purchases[id] = purchase
        return purchase
    
    def delete(self, id) -> bool:
        """
        Delete a Purchase by id.

        Args:
            id (int): The purchase id number.

        Returns:
            bool: True if deletion occurred, False otherwise.
        """
        if self._purchases.get(id) is None:
            return False
        del self._purchases[id]
        return True