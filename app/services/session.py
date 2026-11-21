import contextlib
import datetime
import secrets

from ulid import ULID

from app.exceptions import AuthenticationError, MissingValueError
from app.models import Session
from app.repositories import sessions
from app.repositories.repo import UniqueError
from app.services import user as user_service

SESSION_DURATION = datetime.timedelta(hours=1)
SESSION_TOKEN_BYTES = 128


def _current_timestamp_utc() -> int:

    return (datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()


def find_session(session_token: str) -> Session:
    try:
        return sessions.unique(token=session_token)
    except UniqueError:
        raise MissingValueError(
            "The given session does not exist. Please try logging in again"
        )


def log_in(credential: str, password_plaintext: str) -> Session:
    try:
        user = user_service.find_user_by_credential(credential)
    except MissingValueError:
        raise AuthenticationError("Unknown user")

    if not user.is_active:
        raise AuthenticationError("Cannot log into a deactivated account")

    if user_service.validate_credentials(credential, password_plaintext):
        session_token = secrets.token_hex(SESSION_TOKEN_BYTES)
        sessions.create(
            user_id=user.id,
            token=session_token,
            expiry_timestamp_utc=int(
                (datetime.datetime.now(datetime.UTC) + SESSION_DURATION).timestamp()
            ),
        )

        return sessions.unique(token=session_token)
    else:
        raise AuthenticationError("Please verify your credentials and try again")


def log_out(session_token: str) -> None:
    session = find_session(session_token)
    sessions.delete(id=session.id)


def session_is_valid(session_token: str) -> bool:
    """Determine if a session is valid. A session is valid if:
    - It exists
    - It hasn't expired
    - It is owned by a user who isn't deactivated.
    """
    session = None
    with contextlib.suppress(MissingValueError):
        session = find_session(session_token)

    if session is None:
        return False

    user = user_service.find_user_by_id(session.user_id)
    if not user.is_active:
        return False

    current_timestamp_utc = int(datetime.datetime.now(datetime.UTC).timestamp())

    return session.expiry_timestamp_utc > current_timestamp_utc
