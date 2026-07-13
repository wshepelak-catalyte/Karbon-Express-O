from models.baked_good import BakedGood


class BakedGoodRepository:
    """In-memory repository for BakedGood domain objects."""

    def __init__(self) -> None:
        self._goods: List[BakedGood] = []

    def add(self, baked_good: BakedGood) -> None:
        if self.find_by_name(baked_good.name, baked_good.vendor_name) is not None:
            raise ValueError(
                f"Baked good '{baked_good.name}' for vendor '{baked_good.vendor_name}' already exists."
            )
        self._goods.append(baked_good)

    def all(self) -> List[BakedGood]:
        return list(self._goods)

    def find_by_name(
        self, name: str, vendor_name: Optional[str] = None
    ) -> Optional[BakedGood]:
        for good in self._goods:
            if good.name == name and (vendor_name is None or good.vendor_name == vendor_name):
                return good
        return None

    def find_by_vendor(self, vendor_name: str) -> List[BakedGood]:
        return [good for good in self._goods if good.vendor_name == vendor_name]

    def find_by_allergen(self, allergen: str) -> List[BakedGood]:
        return [good for good in self._goods if allergen in good.allergens]

    def update(self, baked_good: BakedGood) -> None:
        for index, existing in enumerate(self._goods):
            if existing.name == baked_good.name and existing.vendor_name == baked_good.vendor_name:
                self._goods[index] = baked_good
                return
        raise ValueError(
            f"Baked good '{baked_good.name}' for vendor '{baked_good.vendor_name}' not found."
        )

    def remove(self, name: str, vendor_name: Optional[str] = None) -> None:
        original_length = len(self._goods)
        self._goods = [
            good
            for good in self._goods
            if not (good.name == name and (vendor_name is None or good.vendor_name == vendor_name))
        ]
        if len(self._goods) == original_length:
            raise ValueError(
                f"Baked good '{name}'"
                + (f" for vendor '{vendor_name}'" if vendor_name else "")
                + " not found."
            )