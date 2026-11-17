from app.models import Role
from app.repositories.repo import Repo

roles = Repo('roles', Role, indexed_fields=['user_id', 'role'])
