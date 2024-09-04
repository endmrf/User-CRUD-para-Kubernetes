import os
from typing import NamedTuple
from src.domain.use_cases import DeleteUserUseCaseInterface
from src.infra.repo import UserRepository

class DeleteUserParameter(NamedTuple):
    id: str


class DeleteUserUseCase(DeleteUserUseCaseInterface):
    """
    Use case gateway for delete and existing User entity
    """

    repository = UserRepository()

    def proceed(self, parameter: DeleteUserParameter) -> dict:
        """
        Proceed the execution of use case by calling database to delete an existing entity by ID
        :param  - parameter: An Interfaced object with required data
        :return - A Dictionary with formated response of the request having 'success' and 'data' objects
        """

        try:

            record = self.repository.get_user(
                id=parameter.id
            )

            success = self.repository.delete_user(
                id=parameter.id
            )
            serialized_record = record._asdict()
            return self._render_response(success, serialized_record)
        except:
            self._print_exception()
            return self._render_response(False, None)
