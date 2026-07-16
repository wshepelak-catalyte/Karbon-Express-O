from decimal import Decimal
import time

from models.baked_good import BakedGood
from repositories.baked_good_repository import BakedGoodRepository
from services.baked_good_service import BakedGoodService


def print_menu() -> None:
    print("\n=== Baked Good Demo Console ===")
    print("1. Add sample baked good")
    print("2. Mark baked good unavailable")
    print("3. Mark baked good available")
    print("4. Delete baked good")
    print("5. Show all baked goods")
    print("6. Look up baked good by name or ID")
    print("7. Run full demo sequence")
    print("0. Exit")


def build_sample_good(name: str, vendor: str, id_value: int | None = None) -> BakedGood:
    return BakedGood(
        id=id_value,
        name=name,
        vendor_name=vendor,
        allergens=["gluten"] if name == "Croissant" else ["milk", "eggs"],
        purchasing_cost=Decimal("2.50") if name == "Croissant" else Decimal("3.00"),
        markup_percentage=Decimal("0.20") if name == "Croissant" else Decimal("0.25"),
    )


def show_step(message: str) -> None:
    print(f"\n>> {message}")
    time.sleep(0.5)


def main() -> None:
    repository = BakedGoodRepository()
    service = BakedGoodService(repository)

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        if choice == "1":
            name = input("Baked good name (Croissant or Muffin): ").strip()
            vendor = input("Vendor name: ").strip() or "Bakery A"
            good = build_sample_good(name, vendor)
            service.add_baked_good(good)
            show_step(f"Added {good.name} with ID {good.id}")

        elif choice == "2":
            name = input("Baked good name: ").strip()
            vendor = input("Vendor name: ").strip() or "Bakery A"
            try:
                service.mark_unavailable(name, vendor)
                show_step(f"{name} is now unavailable")
            except ValueError as exc:
                print(exc)

        elif choice == "3":
            name = input("Baked good name: ").strip()
            vendor = input("Vendor name: ").strip() or "Bakery A"
            try:
                service.mark_available(name, vendor)
                show_step(f"{name} is now available")
            except ValueError as exc:
                print(exc)

        elif choice == "4":
            name = input("Baked good name: ").strip()
            vendor = input("Vendor name: ").strip() or "Bakery A"
            deleted = service.delete_baked_good(name, vendor)
            show_step(f"Deleted: {deleted}")

        elif choice == "5":
            goods = repository.get_all()
            if not goods:
                show_step("No baked goods in the repository.")
            else:
                show_step("Current baked goods in the repository:")
                for good in goods:
                    print(f"- {good.name} | ID: {good.id} | Vendor: {good.vendor_name} | Available: {good.available}")

        elif choice == "6":
            show_step("Lookup a baked good by typing either its name or its numeric ID.")
            lookup = input("Enter baked good name or ID number: ").strip()
            if lookup.isdigit():
                target_id = int(lookup)
                found = next((good for good in repository.get_all() if good.id == target_id), None)
            else:
                found = next((good for good in repository.get_all() if good.name.lower() == lookup.lower()), None)

            if found is None:
                show_step("No baked good found.")
            else:
                show_step(
                    f"Found: {found.name} | ID: {found.id} | Vendor: {found.vendor_name} | Available: {found.available}"
                )

        elif choice == "7":
            croissant = build_sample_good("Croissant", "Bakery A", 1)
            service.add_baked_good(croissant)
            show_step(f"Added {croissant.name} with ID {croissant.id}")
            service.mark_unavailable("Croissant", "Bakery A")
            show_step(f"Availability after mark_unavailable: {service.is_available('Croissant', 'Bakery A')}")
            service.mark_available("Croissant", "Bakery A")
            show_step(f"Availability after mark_available: {service.is_available('Croissant', 'Bakery A')}")
            service.delete_baked_good("Croissant", "Bakery A")
            show_step("Deleted Croissant from the repository")

            muffin = build_sample_good("Muffin", "Bakery A")
            service.add_baked_good(muffin)
            show_step(f"Added replacement item with reused ID: {muffin.id}")

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
