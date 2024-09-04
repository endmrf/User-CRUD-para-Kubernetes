from datetime import datetime, UTC
from abc import ABC, abstractmethod
from typing import List
from src.domain.models import User


class UserRepositoryInterface(ABC):
    """Interface to User Repository"""

    @abstractmethod
    def create_user(
        cls,
        id: str,
        name: str,
        email: str,
        last_name: str,
        cpf: str,
        created_at: datetime = datetime.now(UTC),
    ) -> User:
        """abstractmethod"""

        raise Exception("Method not implemented")

    @abstractmethod
    def get_user(self, id: str) -> User:
        """abstractmethod"""

        raise Exception("Method not implemented")

    @abstractmethod
    def update_user(
        cls,
        id: str,
        name: str,
        email: str,
        last_name: str,
        cpf: str
    ) -> User:
        """abstractmethod"""

        raise Exception("Method not implemented")

    @abstractmethod
    def delete_user(self, id: str) -> bool:
        """abstractmethod"""

        raise Exception("Method not implemented")

    @abstractmethod
    def select_users(
        cls, name: str = "", email: str = "", last_name: str = "", cpf: str = ""
    ) -> List[User]:
        """abstractmethod"""

        raise Exception("Method not implemented")
