# pylint: disable=E1101

import uuid
from datetime import datetime, timezone, timedelta
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from src.data.interfaces import UserRepositoryInterface
from src.domain.models import User
from src.infra.config import DBConnectionHandler
from src.infra.entities import User as UserModel


class UserRepository(UserRepositoryInterface):
    """Class to manage User Repository"""

    def __build_entity_to_domain_interface(self, entity_instance: UserModel) -> User:
        """
        Transform infra Entity User into named tuple domain model User
        :param  - entity_instance: A UserModel
        :return - A domain User
        """

        domain_entity = User(
            id=entity_instance.id,
            name=entity_instance.name,
            last_name=entity_instance.last_name,
            email=entity_instance.email,
            cpf=entity_instance.cpf,
        )
        return domain_entity

    def create_user(
        self,
        name: str,
        email: str,
        last_name: str,
        cpf: str,
        created_at: datetime = datetime.now(timezone(timedelta(hours=-3))),
    ) -> User:
        """
        Create a new user in the database.

        :param name: The first name of the user.
        :param email: The email address of the user.
        :param last_name: The last name of the user.
        :param cpf: The CPF (Cadastro de Pessoas Físicas) of the user.
        :param created_at: The datetime when the user was created. Defaults to the current time.
        :return: The created User domain model.
        """

        with DBConnectionHandler() as db_connection:
            try:
                id = str(uuid.uuid4())
                entity_instance = UserModel(
                    id=id,
                    created_at=created_at,
                    cpf=cpf,
                    email=email,
                    last_name=last_name,
                    name=name
                )
                
                db_connection.session.add(entity_instance)
                db_connection.session.commit()

                return self.__build_entity_to_domain_interface(entity_instance)

            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()

        return None

    def update_user(
        self,
        id: str,
        name: str,
        email: str,
        last_name: str,
        cpf: str,
    ) -> User:
        """
        Update an existing user in the database.

        :param id: The unique identifier of the user to update.
        :param name: The new first name of the user.
        :param email: The new email address of the user.
        :param last_name: The new last name of the user.
        :param cpf: The new CPF of the user.
        :return: The updated User domain model.
        """

        with DBConnectionHandler() as db_connection:
            try:
                entity_instance = db_connection.session.get(UserModel, id)
                entity_instance.name = name
                entity_instance.cpf = cpf
                entity_instance.email = email
                entity_instance.last_name = last_name

                db_connection.session.merge(entity_instance)
                db_connection.session.commit()

                return self.__build_entity_to_domain_interface(entity_instance)
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()


    def delete_user(self, id: str) -> bool:
        """
        Delete a user from the database by their unique identifier.

        :param id: The unique identifier of the user to delete.
        :return: True if the deletion was successful, False otherwise.
        """

        with DBConnectionHandler() as db_connection:
            try:
                entity_instance = (
                    db_connection.session.query(UserModel)
                    .filter(UserModel.id == id)
                    .first()
                )
                db_connection.session.delete(entity_instance)
                db_connection.session.commit()
                return True
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()

    def select_users(
        self,
        name: str = "",
        email: str = "",
        last_name: str = "",
        cpf: str = "",
        column: str = "name",
        order: str = "desc",
        page: int = 0,
        limit: int = 10,
    ) -> List[User]:
        """
        Select users from the database based on search criteria.

        :param name: Filter by the user's first name. Defaults to empty string (no filter).
        :param email: Filter by the user's email. Defaults to empty string (no filter).
        :param last_name: Filter by the user's last name. Defaults to empty string (no filter).
        :param cpf: Filter by the user's CPF. Defaults to empty string (no filter).
        :param column: The column to sort the results by. Defaults to 'name'.
        :param order: The order of sorting ('asc' for ascending, 'desc' for descending). Defaults to 'desc'.
        :param page: The page number for pagination. Defaults to 0.
        :param limit: The number of results to return per page. Defaults to 10.
        :return: A list of User domain models that match the search criteria.
        """

        attribute = getattr(UserModel, column)
        order_by_attribute = attribute.desc() if order == "desc" else attribute.asc()
        query_data = None
        
        with DBConnectionHandler() as db_connection:
            try:
                query_data = (
                    (
                        db_connection.session.query(UserModel)
                        .filter(
                            UserModel.name.ilike("%" + name + "%"),
                            UserModel.email.ilike("%" + email + "%"),
                            UserModel.last_name.ilike("%" + last_name + "%"),
                            UserModel.cpf.ilike("%" + cpf + "%"),
                        )
                    )
                    .order_by(order_by_attribute)
                    .limit(limit)
                    .offset(page)
                )
                
                return list(
                    map(
                        lambda instance: self.__build_entity_to_domain_interface(
                            instance
                        ),
                        query_data,
                    )
                )
            except NoResultFound:
                return []
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()


    def count_users(
        self,
        name: str = "",
        email: str = "",
        last_name: str = "",
        cpf: str = "",
    ) -> List[User]:
        """
        Count the number of users in the database that match the given search criteria.

        :param name: Filter by the user's first name. Defaults to empty string (no filter).
        :param email: Filter by the user's email. Defaults to empty string (no filter).
        :param last_name: Filter by the user's last name. Defaults to empty string (no filter).
        :param cpf: Filter by the user's CPF. Defaults to empty string (no filter).
        :return: The count of users that match the search criteria.
        """

        with DBConnectionHandler() as db_connection:
            try:
                count = (
                    db_connection.session.query(UserModel)
                    .filter(
                        UserModel.name.ilike("%" + name + "%"),
                        UserModel.email.ilike("%" + email + "%"),
                        UserModel.last_name.ilike("%" + last_name + "%"),
                        UserModel.cpf.ilike("%" + cpf + "%"),
                    )
                    .count()
                )
                return count
            except NoResultFound:
                return []
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()


    def get_user(cls, id: str) -> User:
        """
        Retrieve a user from the database by their unique identifier.

        :param id: The unique identifier of the user to retrieve.
        :return: The User domain model if found, None otherwise.
        """

        query_data = None
        with DBConnectionHandler() as db_connection:
            try:
                query_data = db_connection.session.get(UserModel, id)
                if query_data is not None:
                    return cls.__build_entity_to_domain_interface(query_data)
            except NoResultFound:
                return []
            except:
                db_connection.session.rollback()
                raise
            finally:
                db_connection.session.close()

        return None
