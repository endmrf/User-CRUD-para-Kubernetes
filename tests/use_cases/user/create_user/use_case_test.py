import os
import uuid
import pytest
from faker import Faker
from unittest import mock
from src.infra.config import DBConnectionHandler
from src.data.user.create_user import CreateUserUseCase, CreateUserParameter

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


@mock.patch.dict(
    os.environ,
    {
        "TEST_DATABASE_CONNECTION": MOCK_DB_PATH,
    },
)
def test_create_use_case(mock_entity, db_connection_handler):
    """
    Test the CreateUserUseCase invocation
    :param - None
    :return - None
    """

    use_case = CreateUserUseCase()

    parameter = CreateUserParameter(
        name=mock_entity["name"],
        email=mock_entity["email"],
        last_name=mock_entity["last_name"],
        cpf=mock_entity["cpf"],
    )
    response = use_case.proceed(parameter)
    assert response["success"] is True
    assert response["data"] is not None

    data = use_case.serialize(response)["data"]

    engine = db_connection_handler.get_engine()
    query_entity = engine.execute(
        "SELECT * FROM users WHERE id='{}'".format(response["data"]["id"])
    ).fetchone()

    assert data["id"] == "1"
    assert data["name"] == query_entity.name
    assert data["email"] == query_entity.email
    assert data["last_name"] == query_entity.last_name

    engine.execute("DELETE FROM users WHERE id ='{}'".format(data["id"]))

