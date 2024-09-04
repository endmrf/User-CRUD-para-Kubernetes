import os
import uuid
import pytest
from unittest import mock
from faker import Faker
from src.infra.repo import UserRepository
from src.infra.config import DBConnectionHandler
from tests.mock_util import MockUtil

fake = Faker()
MOCK_DB_PATH = "sqlite:///mock_data.db"


def generate_uuid():
    return str(uuid.uuid4())


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
def test_user_repository_create(mock_entity, db_connection_handler):
    """
    Test the create action into Repository
    :param - None
    :return - None
    """

    user_repository = UserRepository()

    data = user_repository.create_user(
        name=mock_entity["name"],
        email=mock_entity["email"],
        last_name=mock_entity["last_name"],
        cpf=mock_entity["cpf"],
    )

    engine = db_connection_handler.get_engine()
    query_entity = engine.execute(
        "SELECT * FROM users WHERE id='{}'".format(data.id)
    ).fetchone()

    assert data.name == query_entity.name
    assert data.email == query_entity.email
    assert data.last_name == query_entity.last_name
    assert data.cpf == query_entity.cpf

    engine.execute("DELETE FROM users WHERE id='{}'".format(data.id))

@mock.patch.dict(os.environ, {"TEST_DATABASE_CONNECTION": MOCK_DB_PATH})
def test_user_repository_get(mock_entity, db_connection_handler):
    """
    Test get single INSTANCE action into Repository
    :param - None
    :return - None
    """

    engine = db_connection_handler.get_engine()
    engine.execute(MockUtil.build_insert_sql("users", mock_entity))

    user_repository = UserRepository()
    data = user_repository.get_user(
        id=mock_entity["id"]
    )

    assert data.id == mock_entity["id"]
    assert data.name == mock_entity["name"]
    assert data.email == mock_entity["email"]
    assert data.last_name == mock_entity["last_name"]
    assert data.cpf == mock_entity["cpf"]

    engine.execute(
        "DELETE FROM users WHERE id='{}'".format(mock_entity["id"])
    )

@mock.patch.dict(os.environ, {"TEST_DATABASE_CONNECTION": MOCK_DB_PATH})
def test_user_repository_list(mock_entity, db_connection_handler):
    """
    Test list query action into Repository
    :param - None
    :return - None
    """

    engine = db_connection_handler.get_engine()
    engine.execute(MockUtil.build_insert_sql("users", mock_entity))
    user_repository = UserRepository()

    data = user_repository.select_users(
        name=mock_entity["name"]
    )
    assert len(data) > 0

    assert data[0].id == mock_entity["id"]
    assert data[0].name == mock_entity["name"]
    assert data[0].last_name == mock_entity["last_name"]
    assert data[0].cpf == mock_entity["cpf"]

    engine.execute(
        "DELETE FROM users WHERE id='{}'".format(mock_entity["id"])
    )

@mock.patch.dict(os.environ, {"TEST_DATABASE_CONNECTION": MOCK_DB_PATH})
def test_user_repository_update(mock_entity, db_connection_handler):
    """
    Test update single INSTANCE action into Repository
    :param - None
    :return - None
    """

    engine = db_connection_handler.get_engine()
    engine.execute(MockUtil.build_insert_sql("users", mock_entity))

    email = fake.email()

    user_repository = UserRepository()
    data = user_repository.update_user(
        id=mock_entity["id"],
        name=mock_entity["name"],
        email=email,
        last_name=mock_entity["last_name"],
        cpf=mock_entity["cpf"],
    )

    query_entity = engine.execute(
        "SELECT * FROM users WHERE id='{}'".format(data.id)
    ).fetchone()

    assert data.id == query_entity.id
    assert data.id == mock_entity["id"]
    assert data.name == query_entity.name
    assert data.email == query_entity.email
    assert data.last_name == query_entity.last_name
    assert data.cpf == query_entity.cpf

    assert mock_entity["email"] != query_entity.email

    engine.execute(
        "DELETE FROM users WHERE id='{}'".format(mock_entity["id"])
    )


@mock.patch.dict(os.environ, {"TEST_DATABASE_CONNECTION": MOCK_DB_PATH})
def test_user_repository_delete(mock_entity, db_connection_handler):
    """
    Test delete single INSTANCE action into Repository
    :param - None
    :return - None
    """

    engine = db_connection_handler.get_engine()
    engine.execute(MockUtil.build_insert_sql("users", mock_entity))

    user_repository = UserRepository()
    deleted = user_repository.delete_user(
        id=mock_entity["id"]
    )

    assert deleted is True

    query_entity = engine.execute(
        "SELECT * FROM users WHERE id='{}'".format(mock_entity["id"])
    ).fetchone()

    assert query_entity is None

    try:
        user_repository.delete_user(
            id="nonexists", company_id=mock_entity["company_id"]
        )
        assert False
    except:
        assert True