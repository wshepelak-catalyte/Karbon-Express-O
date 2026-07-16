import sys
from datetime import datetime, timezone, timedelta
from decimal import Decimal

# Import Models
from models.customer import Customer
from models.drink import Drink
from models.baked_good import BakedGood
from models.ingredient import Ingredient
from models.purchase import Purchase

# Import Repositories
from repositories.customer_repository import CustomerRepository
from repositories.drink_repository import DrinkRepository
from repositories.baked_good_repository import BakedGoodRepository
from repositories.purchase_repository import PurchaseRepository
from repositories.ingredient_repository import IngredientRepository

# Import Services
from services.customer_service import CustomerService
from services.drink_service import DrinkService
from services.baked_good_service import BakedGoodService
from services.purchase_service import PurchaseService
from services.ingredient_service import IngredientService


class PurchaseDemoApp:
    def __init__(self):
        # 1. Initialize Repositories
        self.cust_repo = CustomerRepository()
        self.drink_repo = DrinkRepository()
        self.bg_repo = BakedGoodRepository()
        self.purch_repo = PurchaseRepository()
        self.ing_repo = IngredientRepository()

        # 2. Initialize Services
        self.customer_service = CustomerService(self.cust_repo)
        self.purchase_service = PurchaseService(self.purch_repo)
        
        # Syncing repository instances
        self.drink_service = DrinkService()
        self.drink_service._repository = self.drink_repo
        
        self.bg_service = BakedGoodService(self.bg_repo)
        self.ing_service = IngredientService()
        self.ing_service._repository = self.ing_repo

        # 3. Seed Demo Data
        self._seed_data()

    def _seed_data(self):
        # Create some ingredients
        self.ing_service.create_ingredient("Espresso Beans", Decimal("0.50"), 1.0, "oz", True)
        self.ing_service.create_ingredient("Whole Milk", Decimal("0.25"), 8.0, "oz", True)
        espresso = self.ing_service.get_ingredient_by_name("Espresso Beans")
        milk = self.ing_service.get_ingredient_by_name("Whole Milk")

        # Create a Drink (Latté)
        self.drink_service.create_drink(
            name="Vanilla Latte",
            ingredients=[espresso, milk],
            cost_to_produce=Decimal("1.20"),
            markup_percentage=Decimal("2.5"),
            sale_price=Decimal("4.20"),
            is_available=True
        )
        latte = self.drink_service.get_drink_by_name("Vanilla Latte")

        # Create a Baked Good (Croissant)
        croissant = BakedGood(
            id=1,
            name="Butter Croissant",
            vendor_name="Le Parisian Bakery",
            allergens=["wheat", "dairy"],
            purchasing_cost=Decimal("1.50"),
            markup_percentage=Decimal("1.0")
        )
        self.bg_service.add_baked_good(croissant)

        # 1. Create Alice (Starts as a clean $0.00 prospect for your live demo) #[cite: 12]
        self.customer_service.create_customer(
            name="Alice Smith",
            email="alice@example.com",
            phone="555-0199",
            username="alice_adventures",
            lifetime_spend=Decimal("0.00"),
            purchases=[]
        )

        # 2. Create Bob (An existing repeat customer) #[cite: 12]
        bob = self.customer_service.create_customer(
            name="Bob Miller",
            email="bob@example.com",
            phone="555-0244",
            username="bob_brews",
            lifetime_spend=Decimal("0.00"),  # Will accumulate dynamically below #[cite: 2]
            purchases=[]
        )

        # 3. Create Charlie (A high-value VIP regular) #[cite: 12]
        charlie = self.customer_service.create_customer(
            name="Charlie Green",
            email="charlie@example.com",
            phone="555-0877",
            username="charlie_croissant",
            lifetime_spend=Decimal("0.00"),  # Will accumulate dynamically below #[cite: 2]
            purchases=[]
        )

        # --- Seeding Historical Ledger ---
        now = datetime.now(timezone.utc)
        thirty_days_ago = now - timedelta(days=30)
        seven_days_ago = now - timedelta(days=7)

        # Bob's History (1 order last month, 1 order last week) #[cite: 15]
        self.purchase_service.create_purchase(
            timestamp=thirty_days_ago,
            items=[latte],
            total_cost=Decimal("4.20"),
            customer=bob
        )
        bob.add_purchase(self.purchase_service.get_all_purchases()[-1]) #[cite: 2]

        self.purchase_service.create_purchase(
            timestamp=seven_days_ago,
            items=[latte, croissant],
            total_cost=Decimal("7.20"),
            customer=bob
        )
        bob.add_purchase(self.purchase_service.get_all_purchases()[-1]) #[cite: 2]

        # Charlie's VIP History (Multiple orders) #[cite: 15]
        self.purchase_service.create_purchase(
            timestamp=thirty_days_ago,
            items=[latte, croissant],
            total_cost=Decimal("7.20"),
            customer=charlie
        )
        charlie.add_purchase(self.purchase_service.get_all_purchases()[-1]) #[cite: 2]

        self.purchase_service.create_purchase(
            timestamp=thirty_days_ago + timedelta(days=5),
            items=[croissant, croissant, croissant],
            total_cost=Decimal("9.00"),
            customer=charlie
        )
        charlie.add_purchase(self.purchase_service.get_all_purchases()[-1]) #[cite: 2]

        self.purchase_service.create_purchase(
            timestamp=seven_days_ago + timedelta(days=2),
            items=[latte, latte, croissant],
            total_cost=Decimal("11.40"),
            customer=charlie
        )
        charlie.add_purchase(self.purchase_service.get_all_purchases()[-1]) #[cite: 2]

    def run(self):
        try:
            while True:
                print("\n" + "="*50)
                print("      ☕ COFFEE SHOP SYSTEM - MAIN MENU ☕      ")
                print("="*50)
                print("1. Run Guided Purchase Simulation 🛒")
                print("2. Purchase CRUD System (Admin Mode) ⚙️")
                print("3. View Customer Profile (Loyalty & History)")
                print("4. View Shop Analytics (Total Revenue Tracker)")
                print("5. Exit Demo (or press Ctrl+C)")
                print("="*50)
                
                choice = input("Select an option (1-5): ").strip()
                
                if choice == "1":
                    self.simulate_purchase()
                elif choice == "2":
                    self.run_crud_submenu()
                elif choice == "3":
                    self.show_customer_profile()
                elif choice == "4":
                    self.show_analytics()
                elif choice == "5":
                    self.exit_gracefully()
                else:
                    print("\n❌ Invalid option. Please select 1-5.")
        except KeyboardInterrupt:
            # Intercepts Ctrl+C cleanly
            self.exit_gracefully()

    def exit_gracefully(self):
        print("\n\nThank you for exploring the purchase demo! Goodbye. 👋")
        sys.exit(0)

    # ==========================================
    #            GUIDED PO DEMO
    # ==========================================
    def simulate_purchase(self):
        print("\n--- 🛒 PO DEMO: SIMULATING PURCHASE FLOW ---")
        try:
            customer = self.customer_service.get_customer_by_name("Alice Smith") #[cite: 12]
        except Exception:
            print("Customer 'Alice Smith' not found!")
            return

        print(f"Current Buyer: {customer.name} (Current Lifetime Spend: ${customer.lifetime_spend:.2f})")
        print("\nWhat would Alice like to buy?")
        print("1. Vanilla Latte ($4.20)")
        print("2. Butter Croissant ($3.00)")
        print("3. Both! (Combo - $7.20)")
        
        choice = input("Select items to purchase (1-3): ").strip()
        
        items_to_buy = []
        if choice == "1":
            items_to_buy.append(self.drink_service.get_drink_by_name("Vanilla Latte"))
        elif choice == "2":
            items_to_buy.append(self.bg_repo.get_by_name("Butter Croissant", "Le Parisian Bakery"))
        elif choice == "3":
            items_to_buy.append(self.drink_service.get_drink_by_name("Vanilla Latte"))
            items_to_buy.append(self.bg_repo.get_by_name("Butter Croissant", "Le Parisian Bakery"))
        else:
            print("❌ Invalid choice. Cancelling purchase.")
            return

        total_cost = sum(item.sale_price for item in items_to_buy)
        purchase_timestamp = datetime.now(timezone.utc)
        
        # 1. Create the Purchase #[cite: 15]
        self.purchase_service.create_purchase(
            timestamp=purchase_timestamp,
            items=items_to_buy,
            total_cost=total_cost,
            customer=customer
        )
        
        # Retrieve purchase & link to customer history to update lifetime spending #[cite: 2]
        latest_purchase = self.purchase_service.get_all_purchases()[-1]
        customer.add_purchase(latest_purchase) #[cite: 2]

        print("\n✅ TRANSACTION SUCCESSFUL!")
        print("-" * 35)
        print(f"Receipt ID:   TXN-{latest_purchase.id}")
        print(f"Customer:     {customer.name}")
        print(f"Items:        {', '.join([item.name for item in items_to_buy])}")
        print(f"Amount Paid:  ${total_cost:.2f}")
        print("-" * 35)
        print(f"📈 Alice's New Lifetime Spend: ${customer.lifetime_spend:.2f}")


    # ==========================================
    #         DELIVERABLE: CRUD SUBMENU
    # ==========================================
    def run_crud_submenu(self):
        try:
            while True:
                print("\n" + "-"*40)
                print("   🛠️  PURCHASE CRUD MANAGEMENT SUBMENU  ")
                print("-"*40)
                print("1. CREATE - New Purchase Record")
                print("2. READ - View All Purchases")
                print("3. READ - Find Purchase by ID")
                print("4. UPDATE - Edit Existing Purchase")
                print("5. DELETE - Remove Purchase")
                print("6. Back to Main Menu")
                print("-"*40)
                
                choice = input("Select an admin option (1-6): ").strip()
                
                if choice == "1":
                    self.crud_create()
                elif choice == "2":
                    self.crud_read_all()
                elif choice == "3":
                    self.crud_read_by_id()
                elif choice == "4":
                    self.crud_update()
                elif choice == "5":
                    self.crud_delete()
                elif choice == "6":
                    break
                else:
                    print("❌ Invalid option.")
        except KeyboardInterrupt:
            self.exit_gracefully()

    def crud_create(self):
        print("\n--- [CREATE] NEW PURCHASE ---")
        # Let administrator choose the customer #[cite: 12]
        customers = self.customer_service.get_all_customers() #[cite: 12]
        if not customers:
            print("No customers available. Please add a customer first.")
            return
        
        print("Select Customer:")
        for idx, c in enumerate(customers, 1):
            print(f"  {idx}. {c.name} (@{c.username})")
        
        cust_choice = input("Select customer number: ").strip()
        try:
            customer = customers[int(cust_choice) - 1]
        except (ValueError, IndexError):
            print("❌ Invalid customer choice.")
            return

        # Select items
        items = []
        # Combine drinks and goods for easy listing
        all_items = []
        for d in self.drink_service.get_all_drinks():
            all_items.append(d)
        for g in self.bg_repo.get_all():
            all_items.append(g)

        print("\nSelect Items to add (Enter numbers separated by commas, e.g., '1,2'):")
        for idx, item in enumerate(all_items, 1):
            print(f"  {idx}. {item.name} (${item.sale_price:.2f})")
        
        item_choices = input("Items choice: ").strip()
        try:
            selected_indices = [int(i.strip()) - 1 for i in item_choices.split(",") if i.strip()]
            selected_items = [all_items[idx] for idx in selected_indices if 0 <= idx < len(all_items)]
        except (ValueError, IndexError):
            print("❌ Invalid item selection.")
            return

        if not selected_items:
            print("❌ No valid items selected. Aborting.")
            return

        total_cost = sum(item.sale_price for item in selected_items)
        
        # Save #[cite: 15]
        self.purchase_service.create_purchase(
            timestamp=datetime.now(timezone.utc),
            items=selected_items,
            total_cost=total_cost,
            customer=customer
        )
        
        # Link to customer profiles to keep spends uniform #[cite: 2]
        latest = self.purchase_service.get_all_purchases()[-1]
        customer.add_purchase(latest) #[cite: 2]
        
        print(f"✅ Created Purchase ID #{latest.id} successfully!")

    def crud_read_all(self):
        print("\n--- [READ] ALL PURCHASES ---")
        purchases = self.purchase_service.get_all_purchases()
        if not purchases:
            print("No purchases recorded yet.")
            return
        
        for p in purchases:
            items_str = ", ".join([item.name for item in p.items])
            print(f"ID: {p.id} | Customer: {p.customer.name} | Items: [{items_str}] | Total Cost: ${p.total_cost:.2f}")

    def crud_read_by_id(self):
        print("\n--- [READ] PURCHASE BY ID ---")
        id_str = input("Enter Purchase ID to view: ").strip()
        if not id_str.isdigit():
            print("❌ ID must be a numeric integer.")
            return
        
        try:
            p = self.purchase_service.get_purchase_by_id(int(id_str)) #[cite: 15]
            items_str = ", ".join([item.name for item in p.items])
            print(f"\n📍 Purchase Record Details:")
            print(f"  ID:         {p.id}")
            print(f"  Timestamp:  {p.timestamp}")
            print(f"  Customer:   {p.customer.name} (@{p.customer.username})")
            print(f"  Items:      {items_str}")
            print(f"  Total Cost: ${p.total_cost:.2f}")
        except Exception as e:
            print(f"❌ {e}")

    def crud_update(self):
        print("\n--- [UPDATE] EXISTING PURCHASE ---")
        id_str = input("Enter Purchase ID to modify: ").strip()
        if not id_str.isdigit():
            print("❌ ID must be numeric.")
            return
        
        p_id = int(id_str)
        try:
            old_purchase = self.purchase_service.get_purchase_by_id(p_id) #[cite: 15]
        except Exception as e:
            print(f"❌ {e}")
            return

        print(f"Currently modifying Purchase #{old_purchase.id} (Owner: {old_purchase.customer.name})")
        cost_input = input(f"Enter new Total Cost (Current: ${old_purchase.total_cost:.2f}): $").strip()
        try:
            new_cost = Decimal(cost_input) if cost_input else old_purchase.total_cost
        except ValueError:
            print("❌ Invalid currency format.")
            return

        # Keep original timestamp and items for simplicity of update, or customize #[cite: 15]
        self.purchase_service.update_purchase(
            id=p_id,
            timestamp=old_purchase.timestamp,
            items=old_purchase.items,
            total_cost=new_cost,
            customer=old_purchase.customer
        )
        print(f"✅ Purchase ID #{p_id} updated successfully!")

    def crud_delete(self):
        print("\n--- [DELETE] REMOVE PURCHASE ---")
        id_str = input("Enter Purchase ID to delete: ").strip()
        if not id_str.isdigit():
            print("❌ ID must be numeric.")
            return
        
        p_id = int(id_str)
        try:
            self.purchase_service.delete_purchase(p_id) #[cite: 15]
            print(f"🗑️ Purchase ID #{p_id} deleted successfully.")
        except Exception as e:
            print(f"❌ {e}")


    # ==========================================
    #               UTILITIES
    # ==========================================
    def show_customer_profile(self):
        print("\n--- 👤 CUSTOMER DIRECTORY & LOYALTY HISTORY ---")
        customers = self.customer_service.get_all_customers() #[cite: 12]
        if not customers:
            print("No customers found in the system.")
            return

        print("Select a customer to view their detailed profile:")
        for idx, c in enumerate(customers, 1):
            print(f"  {idx}. {c.name} (@{c.username}) — Lifetime Spend: ${c.lifetime_spend:.2f}")

        choice = input("\nEnter customer number (or press Enter to return): ").strip()
        if not choice:
            return

        try:
            selected_customer = customers[int(choice) - 1]
            print(f"\nProfile Details for {selected_customer.name}:")
            print(f"  • Email:          {selected_customer.email}")
            print(f"  • Phone:          {selected_customer.phone}")
            print(f"  • Username:       {selected_customer.username}")
            print(f"  • Lifetime Spend: ${selected_customer.lifetime_spend:.2f}")
            print(f"  • Total Orders:   {len(selected_customer.purchases)}")
            
            if selected_customer.purchases:
                print("\n  Receipt History:")
                for i, p in enumerate(selected_customer.purchases, 1):
                    item_names = ", ".join([item.name for item in p.items])
                    print(f"    {i}. {p.timestamp.strftime('%Y-%m-%d %H:%M:%S')} UTC | {item_names} | Total: ${p.total_cost:.2f}")
            else:
                print("\n  Receipt History: No transactions logged yet.")
        except (ValueError, IndexError):
            print("❌ Invalid selection.")

    def show_analytics(self):
        print("\n--- 📈 SHOP REVENUE ANALYTICS ---")
        
        # 1. Fetch total statistics using the purchase service #[cite: 15]
        total_revenue = self.purchase_service.get_total_spending() #[cite: 15]
        purchases = self.purchase_service.get_all_purchases() #[cite: 15]
        total_transactions = len(purchases)

        # 2. Extract boundaries for the current calendar month
        now = datetime.now(timezone.utc)
        current_year = now.year
        current_month = now.month

        # 3. Calculate this month's subtotal dynamically
        this_month_revenue = Decimal("0.00")
        for p in purchases:
            if p.timestamp.year == current_year and p.timestamp.month == current_month:
                this_month_revenue += p.total_cost

        # 4. Display the formatted stats
        print(f"💰 All-Time Total Revenue:  ${total_revenue:.2f}")
        print(f"📅 Current Month Revenue:   ${this_month_revenue:.2f}")
        print(f"🧾 Total Transactions:      {total_transactions}")


if __name__ == "__main__":
    app = PurchaseDemoApp()
    app.run()