from decimal import Decimal
import time 
from models.drink import Drink
from models.ingredient import Ingredient
from repositories.drink_repository import DrinkRepository
from services.drink_service import DrinkService




def print_menu() -> None:
    print("\n=== Drink Demo Console ===")
    print("1. Add sample drink")  #create_drink
    print("2. Show all drinks")  #get_all_drinks
    print("3. Look up drink by name")  #get_drink_by_name
    print("4. Update drink name/ingredient")  #update_drink
    print("5. Delete drink by name")  #delete_drink 
    print("6. Get available drinks")  #get_available_drinks
    print("7. Run full demo sequence")
    print("0. Exit")


def build_sample_drink(name: str, ingredients: list[Ingredient], id_value: int | None = None) -> Drink:
    return Drink(
        id=id_value,
        name=name,
        ingredients=ingredients,
        cost_to_produce=Decimal("2.50"),    
        markup_percentage=Decimal("0.20"),
        sale_price=Decimal("3.00"),
        is_available=True
    )


def show_step(message: str) -> None:
    print(f"\n>> {message}")
    time.sleep(0.5)


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
            ingredients_list = [Ingredient(name=ing.strip()) for ing in ingredients_input.split(",")]
            drink = build_sample_drink(name, ingredients_list)
            service.add_drink(drink)
            show_step(f"Added {drink.name} with ID {drink.id}")

        elif choice == "2":
            drinks = service.get_all_drinks()
            for drink in drinks:
                print(f"ID: {drink.id}, Name: {drink.name}, Ingredients: {[ing.name for ing in drink.ingredients]}")

        elif choice == "3":
            name = input("Drink name to look up: ").strip()
            drink = service.get_drink_by_name(name)
            if drink:
                print(f"Found Drink - ID: {drink.id}, Name: {drink.name}, Ingredients: {[ing.name for ing in drink.ingredients]}")
            else:
                print("Drink not found.")

        elif choice == "4":
            name = input("Drink name to update: ").strip()
            new_name = input("New drink name: ").strip()
            new_ingredients_input = input("New ingredients (comma-separated): ").strip()
            new_ingredients_list = [Ingredient(name=ing.strip()) for ing in new_ingredients_input.split(",")]
            updated_drink = build_sample_drink(new_name, new_ingredients_list)
            result = service.update_drink(name, updated_drink)
            if result:
                show_step(f"Updated {name} to {updated_drink.name}")
            else:
                print("Drink not found for update.")

        elif choice == "5":
            name = input("Drink name to delete: ").strip()
            success = service.delete_drink(name)
            if success:
                show_step(f"Deleted {name} from the repository")
            else:
                print("Drink not found for deletion.")

        elif choice == "6":
            available_drinks = [drink for drink in service.get_all_drinks() if drink.is_available]
            for drink in available_drinks:
                print(f"Available Drink - ID: {drink.id}, Name: {drink.name}, Ingredients: {[ing.name for ing in drink.ingredients]}")

        elif choice == "7":
            # Full demo sequence can be added later if needed
            print("Full demo sequence not implemented yet.")

if __name__ == "__main__":
    main()             