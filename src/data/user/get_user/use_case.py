from typing import NamedTuple
from src.domain.use_cases import GetUserUseCaseInterface
from src.infra.repo import UserRepository

class GetUserParameter(NamedTuple):
    id: str


class GetUserUseCase(GetUserUseCaseInterface):
    """
    Use case gateway for get single User entity
    """

    repository = UserRepository()

    def proceed(self, parameter: GetUserParameter) -> dict:
        """
        Proceed the execution of use case by calling database to retrieve single entity by ID
        :param  - parameter: An Interfaced object with required data
        :return - A Dictionary with formated response of the request having 'success' and 'data' objects
        """

        try:
            record = self.repository.get_user(
                id=parameter.id
            )

            serialized_record = record._asdict()
            return self._render_response(True, serialized_record)
        except:
            self._print_exception()
            return self._render_response(False, None)
