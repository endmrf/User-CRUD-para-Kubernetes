from datetime import datetime, timedelta, timezone
from sqlalchemy import Column, String, DateTime, cast
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import JSON, BigInteger, Boolean
from src.infra.config import Base

class User(Base):
    """Users Entity"""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    cpf = Column(String(), nullable=False, unique=True)
    email = Column(String(), nullable=False, unique=True)
    created_at = Column(
        DateTime, default=datetime.now(timezone(timedelta(hours=-3))), nullable=True
    )
    

    def __str__(self) -> str:
        """
        Returns a string representation of the User object.

        :return: A string representation of the User object.
        :rtype: str
        """
        return f"User [id={self.id}, email={self.email}, name={self.name}]"