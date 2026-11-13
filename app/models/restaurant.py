class Restaurant:
    def __init__(
            self,
            *,
            id: str,
            owner_id: str,
            name: str,
            description: str,
            address: str,
            phone_number: str,
            is_active: bool,
        ) -> None:
        self._id = id
        self._owner_id = owner_id
        self._name = name
        self._description = description
        self._address = address
        self._phone_number = phone_number
        self._is_active = is_active

    def is_owned_by(self, user_id: str) -> bool:
        has_same_user_id = self._owner_id == user_id

        if has_same_user_id:
            return True

        return False
