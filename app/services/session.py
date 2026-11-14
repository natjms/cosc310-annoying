from fastapi import HTTPException, Request
from ulid import ULID
import datetime
import secrets

from app.models import Session
from app.repositories import sessions
from app.repositories.repo import UniqueError
from app.services import user as user_service
from app.exceptions import AuthenticationException, MissingValueException

SESSION_DURATION = datetime.timedelta(hours=1)
SESSION_TOKEN_BYTES = 128

def _current_timestamp_utc() -> int:

    return (datetime.utcnow() - datetime(1970,1,1)).total_seconds()

def find_session(session_token: str) -> Session:
    try:
        return sessions.unique(token=session_token)
    except UniqueError:
        raise MissingValueException('The given session does not exist. Please try logging in again')

def log_in(credential: str, password_plaintext: str) -> Session:
    user = user_service.find_user_by_credential(credential)

    if user_service.validate_credentials(credential, password_plaintext):
        session_token = secrets.token_hex(SESSION_TOKEN_BYTES)
        sessions.create(user_id=user.id, token=session_token,
            expiry_timestamp_utc=int((datetime.datetime.now(datetime.UTC) + SESSION_DURATION).timestamp()))

        return sessions.unique(token=session_token)
    else:
        raise AuthenticationException("Please verify your credentials and try again")

def log_out(session_token: str) -> None:
    session = find_session(session_token)
    sessions.delete(id=session.id)

def session_is_valid(session_token: str) -> bool:
    session = None
    try:
        session = find_session(session_token)
    except MissingValueException:
        pass

    if session is None:
        return False

    current_timestamp_utc = int(datetime.datetime.now(datetime.UTC).timestamp())

    return session.expiry_timestamp_utc > current_timestamp_utc

def guard_authentication(request: Request):
    if "authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Session token not provided")

    # e.g. Authorization: Bearer 056b322f90557e6796d4d76de5227d90...
    try:
        auth_scheme, session_token = request.headers["authorization"].split(" ")
    except ValueError:
        # Will occur if the header looks like "Authorization: 056b322f90557e6796d4d76de5227d90..."
        # which is an incorrect use of the Authorization header
        raise HTTPException(status_code=422, detail="Invalid Authorization header")

    if auth_scheme != "Bearer":
        raise HTTPException(status_code=422, detail="Only the Bearer authentication scheme is supported")

    try:
        session = find_session(session_token)
    except MissingValueException:
        raise HTTPException(status_code=401, detail="Session not found. Please try logging in again")

    if not session_is_valid(session.token):
        log_out(session.token)
        raise HTTPException(status_code=401, detail="Your session has expired. Please try logging in again")

    user = user_service.find_user_by_id(session.user_id)

    return (user, session)
