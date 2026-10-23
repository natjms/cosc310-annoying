from app.models.restaurant import Restaurant
from app.repositories.repo import Repo

restaurants = Repo("restaurants", Restaurant, indexed_fields=["owner_id", "cuisine_ids", "name"])
