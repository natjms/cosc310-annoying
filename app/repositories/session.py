from app.models.session import Session
from app.repositories.repo import Repo

sessions = Repo('sessions', Session, indexed_fields=['user_id', 'token'])
