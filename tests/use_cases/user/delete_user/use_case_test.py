import os
import uuid
import pytest
from faker import Faker
from unittest import mock
from tests.mock_util import MockUtil
from src.infra.config import DBConnectionHandler
from src.data.user.delete_user import DeleteUserUseCase, DeleteUserParameter

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
def test_delete_use_case(mock_entity, db_connection_handler):
    """
    Test the DeleteUserUseCase invocation
    :param - None
    :return - None
    """

    engine = db_connection_handler.get_engine()
    engine.execute(MockUtil.build_insert_sql("users", mock_entity))

    
    use_case = DeleteUserUseCase()
    parameter = DeleteUserParameter(id=mock_entity["id"])
    response = use_case.proceed(parameter)

    assert response["success"] is True
    assert response["data"] is not None
    data = response["data"]

    assert data["id"] == mock_entity["id"]

    parameter = DeleteUserParameter(id="<NOT_EXISTING_ID>")
    response = use_case.proceed(parameter)

    assert response["success"] is False
    assert response["data"] is None

    query_entity = engine.execute(
        "SELECT * FROM users WHERE id='{}'".format(mock_entity["id"])
    ).fetchone()

    assert query_entity is None

