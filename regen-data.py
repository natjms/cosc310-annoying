from dotenv import load_dotenv
load_dotenv(".env")


from app.exceptions import ResourceConflictException
from app.models.role import RoleName
from app.services import menu as menu_service
from app.services import menu_item as menu_item_service
from app.services import restaurant as restaurant_service
from app.services import role as role_service
from app.services import user as user_service

def run_regen():
    print("starting database (re)generation...")

    # users/roles
    print("\n" + "creating users...")
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
            # password is always "password" to keep things simple
            user = user_service.register_user(u["username"], u["email"], "password")
            print(f"[+] created user: {u['username']}")
        except ResourceConflictException:
            # fetch pre-existing users
            user = user_service.find_user_by_username(u["username"])
            print(f"[-] user already exists: {u['username']}")

        # role-assignment
        for role in u["roles"]:
            role_service.assign_role(user.id, role)

        if u["username"] == "owner":
            owners.append(user)

    owner_user = owners[0]

    # restaurants/menus
    print("\n" + "creating restaurants, menus, and items...\n")

    # array structure: Restaurant -> Menus -> Items (Name, Price)
    mock_data = {
        "Spaghetti Farm": {
            "Lunch Menu": [("Small Spaghetti", 2.00), ("Large Spaghetti", 5.00)],
            "Dinner Menu": [("Meatballs", 3.00), ("Garlic Bread", 4.00)],
        },
        "Pizza Shack": {
            "Classic Pizzas": [("Cheese Pizza", 10.00), ("Pepperoni Pizza", 12.00)],
            "Sides": [("Chicken Wings", 8.00), ("Caesar Salad", 6.00)],
        },
        "Burger Queen": {
            "Burgers": [("Whopper", 3.00), ("Double Whopper", 5.50)],
            "Sides": [("Fries", 2.00), ("Onion Rings", 3.00)],
        },
        "Taco Shell": {
            "Tacos": [("Beef Taco", 3.00), ("Chicken Taco", 3.00)],
            "Drinks": [("Soda", 1.00), ("Bottled Water", 1.00)],
        },
        "Western Sushi": {
            "Rolls": [("California Roll", 6.00), ("Spicy Tuna Roll", 8.00)],
            "Appetizers": [("Edamame", 4.00), ("Miso Soup", 2.00)],
        },
    }

    for rest_name, menus in mock_data.items():
        # create restaurants
        restaurant = restaurant_service.create_restaurant(owner_user.id, rest_name)
        print(f"[+] created restaurant: {rest_name}")

        for menu_name, items in menus.items():
            # create menus
            menu = menu_service.create_menu(restaurant.id, menu_name)
            print(f"[+] created menu: {menu_name}")

            for item_name, price in items:
                # create menu items (Note: service expects a string for menu_id)
                # this is the case because of ULID                
                menu_item_service.create_menu_item(str(menu.id), item_name, price)
                print(f"[+] created item: {item_name} (${price})")

    print("\n\n" +"seeding complete!")
    print("login as 'customer' or 'owner' with password.")


if __name__ == "__main__":
    run_regen()
