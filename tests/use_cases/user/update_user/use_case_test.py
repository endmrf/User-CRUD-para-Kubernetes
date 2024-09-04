import os
import uuid
import pytest
from faker import Faker
from unittest import mock
from tests.mock_util import MockUtil
from src.infra.config import DBConnectionHandler
from src.data.user.update_user import UpdateUserUseCase, UpdateUserParameter

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
def test_update_use_case(mock_entity, db_connection_handler):
    """
    Test the UpdateUserUseCase invocation
    :param - None
    :return - None
    """

    engine = db_connection_handler.get_engine()
    engine.execute(MockUtil.build_insert_sql("users", mock_entity))

    use_case = UpdateUserUseCase()

    name = fake.name()
    email = fake.email()

    parameter = UpdateUserParameter(
        id=mock_entity["id"],
        name=name,
        email=email,
        cpf=mock_entity["cpf"],
        last_name=mock_entity["last_name"],
    )
    response = use_case.proceed(parameter)
    assert response["success"] is True
    assert response["data"] is not None

    data = response["data"]

    query_entity = engine.execute(
        "SELECT * FROM users WHERE id='{}'".format(mock_entity["id"])
    ).fetchone()

    assert data["name"] == query_entity.name
    assert data["email"] == query_entity.email
    assert name == query_entity.name
    assert email == query_entity.email

    assert data["last_name"] == query_entity.last_name
    assert data["cpf"] == query_entity.cpf

    assert query_entity.name != mock_entity["name"]
    assert query_entity.email != mock_entity["email"]

    parameter = UpdateUserParameter(
        id="<NOT_EXISTING_ID>",
        name=name,
        email=email,
        cpf=mock_entity["cpf"],
        last_name=mock_entity["last_name"],
    )
    response = use_case.proceed(parameter)
    assert response["success"] is False
    assert response["data"] is None

    engine.execute("DELETE FROM users WHERE id='{}'".format(data["id"]))
