from typing import NamedTuple
from src.domain.use_cases import UpdateUserUseCaseInterface
from src.infra.repo import UserRepository

class UpdateUserParameter(NamedTuple):
    id: str
    name: str
    cpf: str
    email: str
    last_name: str


class UpdateUserUseCase(UpdateUserUseCaseInterface):
    """
    Use case gateway for create a new User entity
    """

    repository = UserRepository()

    def proceed(self, parameter: UpdateUserParameter) -> dict:
        """
        Proceed the execution of update use case by calling database to update a existing entity with parameters
        :param  - parameter: An Interfaced object with required data
        :return - A Dictionary with formated response of the request having 'success' and 'data' objects
        """

        try:

            record = self.repository.update_user(
                id=parameter.id,
                name=parameter.name,
                cpf=parameter.cpf,
                email=parameter.email,
                last_name=parameter.last_name,
            )
            serialized_record = record._asdict()
            return self._render_response(True, serialized_record)
        except:
            self._print_exception()
            return self._render_response(False, None)
