from app.exceptions import ResourceConflictException
from app.models.role import RoleName
from app.services import menu as menu_service
from app.services import menu_item as menu_item_service
from app.services import restaurant as restaurant_service
from app.services import role as role_service
from app.services import user as user_service


def run_seed():
    print("Starting database seed...")

    # --- 1. CREATE USERS & ROLES ---
    print("Creating users...")
    users_data = [
        {
            "username": "admin",
            "email": "admin@test.com",
            "roles": [RoleName.admin, RoleName.customer],
        },
        {
            "username": "customer",
            "email": "customer@test.com",
            "roles": [RoleName.customer],
        },
        {
            "username": "owner",
            "email": "owner@test.com",
            "roles": [RoleName.restaurateur, RoleName.customer],
        },
    ]

    owners = []
    for u in users_data:
        try:
            # Create user (password is always "password")
            user = user_service.register_user(u["username"], u["email"], "password")
            print(f"  [+] Created user: {u['username']}")
        except ResourceConflictException:
            # If they already exist, fetch them
            user = user_service.find_user_by_username(u["username"])
            print(f"  [-] User already exists: {u['username']}")

        # Assign roles
        for role in u["roles"]:
            role_service.assign_role(user.id, role)

        if u["username"] == "owner":
            owners.append(user)

    owner_user = owners[0]

    # --- 2. RESTAURANTS, MENUS, & ITEMS ---
    print("Creating restaurants, menus, and items...")

    # Data structure: Restaurant -> Menus -> Items (Name, Price)
    mock_data = {
        "Spaghetti Store": {
            "Lunch Menu": [("Small Spaghetti", 2.00), ("Large Spaghetti", 5.00)],
            "Dinner Menu": [("Meatballs", 3.00), ("Garlic Bread", 4.00)],
        },
        "Pizza Shack": {
            "Classic Pizzas": [("Cheese Pizza", 10.00), ("Pepperoni Pizza", 12.00)],
            "Sides": [("Chicken Wings", 8.00), ("Caesar Salad", 6.00)],
        },
        "Burger King": {
            "Burgers": [("Whopper", 6.00), ("Double Whopper", 8.00)],
            "Sides": [("Fries", 2.00), ("Onion Rings", 3.00)],
        },
        "Taco Truck": {
            "Tacos": [("Beef Taco", 3.00), ("Chicken Taco", 3.00)],
            "Drinks": [("Soda", 1.00), ("Bottled Water", 1.00)],
        },
        "Sushi Spot": {
            "Rolls": [("California Roll", 6.00), ("Spicy Tuna Roll", 8.00)],
            "Appetizers": [("Edamame", 4.00), ("Miso Soup", 2.00)],
        },
    }

    for rest_name, menus in mock_data.items():
        # Create Restaurant
        restaurant = restaurant_service.create_restaurant(owner_user.id, rest_name)
        print(f"  [+] Created Restaurant: {rest_name}")

        for menu_name, items in menus.items():
            # Create Menu
            menu = menu_service.create_menu(restaurant.id, menu_name)
            print(f"    [+] Created Menu: {menu_name}")

            for item_name, price in items:
                # Create Menu Item (Note: service expects a string for menu_id)
                menu_item_service.create_menu_item(str(menu.id), item_name, price)
                print(f"      [+] Created Item: {item_name} (${price})")

    print(
        "Seeding complete! You can now log in as 'customer' or 'owner' with password 'password'."
    )


if __name__ == "__main__":
    run_seed()
