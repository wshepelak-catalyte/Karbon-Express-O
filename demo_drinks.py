from decimal import Decimal
from decimal import Decimal
import time
from models.ingredient import Ingredient
from services.drink_service import DrinkService
from exceptions import DuplicateDrinkError, DrinkNotFoundError


def print_menu() -> None:
    print("\n=== Drink Demo Console ===")
    print("1. Add sample drink")
    print("2. Show all drinks")
    print("3. Look up drink by name")
    print("4. Update drink")
    print("5. Delete drink by name")
    print("6. Get available drinks")
    print("7. Run full demo sequence")
    print("0. Exit")


def show_step(message: str) -> None:
    print(f"\n>> {message}")
    time.sleep(0.5)


def _parse_ingredients(raw: str) -> list[Ingredient]:
    items = [s.strip() for s in raw.split(",") if s.strip()]
    # Provide minimal valid fields for Ingredient dataclass
    return [Ingredient(id=0, name=name, purchasing_cost=0.0, unit_amount=1.0, unit_of_measure="", available=True) for name in items]


def main() -> None:
    service = DrinkService()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        if choice == "1":
            name = input("Drink name: ").strip()
            ingredients_input = input("Ingredients (comma-separated): ").strip()
            ingredients_list = _parse_ingredients(ingredients_input)
            try:
                service.create_drink(
                    name=name,
                    ingredients=ingredients_list,
                    cost_to_produce=Decimal("2.50"),
                    markup_percentage=Decimal("0.20"),
                    sale_price=Decimal("3.00"),
                    is_available=True,
                )
                show_step(f"Added {name}")
            except DuplicateDrinkError as exc:
                print(exc)

        elif choice == "2":
            drinks = service.get_all_drinks()
            for drink in drinks:
                print(f"ID: {drink.id}, Name: {drink.name}, Ingredients: {[ing.name for ing in drink.ingredients]}")

        elif choice == "3":
            name = input("Drink name to look up: ").strip()
            try:
                drink = service.get_drink_by_name(name)
                print(f"Found Drink - ID: {drink.id}, Name: {drink.name}, Ingredients: {[ing.name for ing in drink.ingredients]}")
            except DrinkNotFoundError as exc:
                print(exc)

        elif choice == "4":
            name = input("Drink name to update: ").strip()
            new_ingredients_input = input("New ingredients (comma-separated): ").strip()
            new_ingredients_list = _parse_ingredients(new_ingredients_input)
            new_cost = Decimal(input("New cost to produce (e.g. 2.50): ").strip() or "0")
            new_markup = Decimal(input("New markup percentage (e.g. 0.20): ").strip() or "0")
            new_sale = Decimal(input("New sale price (e.g. 3.00): ").strip() or "0")
            is_avail_raw = input("Is available? (y/n): ").strip().lower()
            is_avail = is_avail_raw.startswith("y")
            try:
                service.update_drink(name, new_ingredients_list, new_cost, new_markup, new_sale, is_avail)
                show_step(f"Updated {name}")
            except DrinkNotFoundError as exc:
                print(exc)
            except DuplicateDrinkError as exc:
                print(exc)

        elif choice == "5":
            name = input("Drink name to delete: ").strip()
            try:
                service.delete_drink(name)
                show_step(f"Deleted {name} from the repository")
            except DrinkNotFoundError as exc:
                print(exc)

        elif choice == "6":
            available_drinks = service.get_available_drinks()
            for drink in available_drinks:
                print(f"Available Drink - ID: {drink.id}, Name: {drink.name}, Ingredients: {[ing.name for ing in drink.ingredients]}")

        elif choice == "7":
            # Simple demo sequence
            try:
                service.create_drink(
                    name="Demo Coffee",
                    ingredients=[Ingredient(id=0, name="Water", purchasing_cost=0.0, unit_amount=1.0, unit_of_measure="", available=True)],
                    cost_to_produce=Decimal("1.00"),
                    markup_percentage=Decimal("0.50"),
                    sale_price=Decimal("1.50"),
                    is_available=True,
                )
                show_step("Added Demo Coffee")
            except DuplicateDrinkError:
                show_step("Demo Coffee already exists")


if __name__ == "__main__":
    main()