from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.repositories.repo import Repo

carts = Repo('carts', Cart, indexed_fields=['user_id','restaurant_id'])
