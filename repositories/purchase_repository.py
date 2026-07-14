from models.purchase import Purchase
from numbers import Number

class PurchaseRepository:
    """A repository for managing in-memory storage of Purchase records.

    Attributes:
        _purchases (list[Purchase]): The internal list storing all purchase transactions.
    """

    def __init__(self):
        """Initializes an empty purchase repository."""
        self._purchases: list[Purchase] = []

    def get_all(self) -> list[Purchase]:
        """Retrieves all purchase transactions currently stored in the repository.

        Returns:
            list[Purchase]: A list containing all managed Purchase objects.
        """
        return self._purchases

    def get_by_id(self, id: Number) -> Purchase | None:
        """Finds a specific purchase record by its unique numerical identifier.

        Args:
            id (Number): The numeric ID of the purchase transaction to look up.

        Returns:
            Purchase | None: The matching Purchase object if found; otherwise, None.
        """
        return next((p for p in self._purchases if p.id == id), None)

    def get_by_customer_username(self, username: str) -> list[Purchase]:
        """Retrieve all purchases associated with a given customer username."""
        if username is None:
            return []
        lookup = username.strip().lower()
        return [
            p
            for p in self._purchases
            if isinstance(p.customer.username, str)
            and p.customer.username.strip().lower() == lookup
        ]

    def add(self, purchase: Purchase) -> Purchase:
        """Adds a new purchase transaction record to the repository.

        Args:
            purchase (Purchase): The Purchase instance to be recorded.

        Returns:
            Purchase: The Purchase instance that was successfully added.
        """
        self._purchases.append(purchase)
        return purchase

    def update(self, id: Number, purchase: Purchase) -> Purchase | None:
        """Replaces an existing purchase transaction with updated information.

        Args:
            id (Number): The numeric ID of the purchase record to update.
            purchase (Purchase): The new Purchase instance to replace the old record.

        Returns:
            Purchase | None: The updated Purchase instance if the target ID was found
                and replaced; otherwise, None.
        """
        existing_purchase = self.get_by_id(id)
        if existing_purchase:
            self._purchases.remove(existing_purchase)
            self._purchases.append(purchase)
            return purchase
        return None