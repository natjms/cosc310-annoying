from app.schemas.restaurant import RestaurantResponse
from app.repositories.repo import Repo

restaurants = Repo('restaurants', RestaurantResponse, indexed_fields=['owner_id', 'cuisine_ids', 'name'])
