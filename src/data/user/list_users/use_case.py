from typing import NamedTuple
from src.domain.use_cases import ListUsersUseCaseInterface
from src.infra.repo import UserRepository

class ListUsersParameter(NamedTuple):
    name: str = ""
    email: str = ""
    last_name: str = ""
    cpf: str = ""
    column: str = "name"
    order: str = "asc"
    page: int = 0
    limit: int = 10

class ListUsersUseCase(ListUsersUseCaseInterface):
    """
    Use case gateway for list User entity
    """

    repository = UserRepository()

    def proceed(self, parameter: ListUsersParameter) -> dict:
        """
        Proceed the execution of use case by calling database to retrieve entities
        :param  - parameter: An Interfaced object with required data
        :return - A Dictionary with formated response of the request having 'success' and 'data' objects
        """

        try:
            
            records = self.repository.select_users(
                name=parameter.name,
                email=parameter.email,
                cpf=parameter.cpf,
                last_name=parameter.last_name,
                column=parameter.column,
                order=parameter.order,
                page=parameter.page,
                limit=parameter.limit,
            )
            
            total_count = self.repository.count_users(
                name=parameter.name,
                email=parameter.email,
                cpf=parameter.cpf,
                last_name=parameter.last_name,
            )
            serialized_records = list(map(lambda item: item._asdict(), records))
            return self._render_response(True, serialized_records, total=total_count)
        except:
            self._print_exception()
            return self._render_response(False, [])
