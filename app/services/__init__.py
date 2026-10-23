from ulid import ULID

def maybe_ulid(value: str | ULID) -> ULID:
    if isinstance(value, str):
        return ULID.from_str(value)
    else:
        return value
