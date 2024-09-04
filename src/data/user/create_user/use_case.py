from typing import NamedTuple
from src.domain.use_cases import CreateUserUseCaseInterface
from src.infra.repo import UserRepository

class CreateUserParameter(NamedTuple):
    name: str
    email: str
    last_name: str
    cpf: str

 

class CreateUserUseCase(CreateUserUseCaseInterface):
    """
    Use case gateway for create a new User entity
    """

    repository = UserRepository()

    def proceed(self, parameter: CreateUserParameter) -> dict:
        """
        Proceed the execution of use case by calling database to create a new single entity with parameters
        :param  - parameter: An Interfaced object with required data
        :return - A Dictionary with formated response of the request having 'success' and 'data' objects
        """

        try:
            record = self.repository.create_user(
                name=parameter.name,
                email=parameter.email,
                cpf=parameter.cpf,
                last_name=parameter.last_name,
            )

            serialized_record = record._asdict()
            return self._render_response(True, serialized_record)
        except:
            self._print_exception()
            return self._render_response(False, None)
