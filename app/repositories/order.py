from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.repo import Repo

orders = Repo("orders", Order, indexed_fields=["user_id", "restaurant_id"])
