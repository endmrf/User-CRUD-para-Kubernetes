import os
import uuid
import pytest
from faker import Faker
from unittest import mock
from tests.mock_util import MockUtil
from src.infra.config import DBConnectionHandler
from src.data.user.list_users import ListUsersUseCase, ListUsersParameter

fake = Faker()
MOCK_DB_PATH = "sqlite:///mock_data.db"


@pytest.fixture(scope="session")
def mock_entity():

    return {
        "id": str(uuid.uuid4()),
        "cpf": fake.pystr(min_chars=11, max_chars=11),
        "name": fake.name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
    }


@pytest.fixture(scope="session")
@mock.patch.dict(os.environ, {"TEST_DATABASE_CONNECTION": MOCK_DB_PATH})
def db_connection_handler():
    return DBConnectionHandler()


@mock.patch.dict(os.environ, {"TEST_DATABASE_CONNECTION": MOCK_DB_PATH})
def test_list_use_case(mock_entity, db_connection_handler):
    """
    Test the ListUsersUseCase invocation
    :param - None
    :return - None
    """

    engine = db_connection_handler.get_engine()
    engine.execute(MockUtil.build_insert_sql("users", mock_entity))

    use_case = ListUsersUseCase()
    parameter = ListUsersParameter(
        name=mock_entity["name"],
        email=mock_entity["email"],
        last_name=mock_entity["last_name"],
        cpf=mock_entity["cpf"],
        column="name",
        order="asc",
        page=0,
        limit=10,
    )
    response = use_case.proceed(parameter)

    assert response["success"] is True
    assert response["data"] is not None

    data = response["data"][0]
    assert data["id"] == mock_entity["id"]
    assert data["name"] == mock_entity["name"]
    assert data["email"] == mock_entity["email"]
    assert data["last_name"] == mock_entity["last_name"]
    assert data["cpf"] == mock_entity["cpf"]

    engine.execute("DELETE FROM users WHERE id='{}'".format(data["id"]))
