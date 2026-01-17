from core.User import User
from decimal import Decimal
from core.Operations import Operation

id_counter = 0

class BankAccount:
    """Расчётный счёт.

    Attributes:
        id (str): Уникальный идентификатор счета. (readonly)
        user (User): Объект пользователя, владеющего счетом. (readonly)
        balance (Decimal): Текущий баланс счета. (readonly)
        operations_history (list): История проведенных операций. (readonly)
    """
    def __init__(self, user: User):
        """
        Args:
            user (User): Объект пользователя, владеющего счетом.

        Raises:
            ValueError: Если user не является экземпляром класса User.
        """
        if not isinstance(user, User):
            raise ValueError("user must be instance of user class")

        id_counter += 1 # уникальный id
        self.__id = id_counter
        self.__user = user
        # Баланс делается через Decimal для точности в расчётах.
        # balance и history через safe вместо private, чтобы изменять через класс операций
        self._balance = Decimal('0')
        self._operations_history = []

    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def user(self) -> User:
        return self.__user

    @property
    def balance(self) -> Decimal:
        return self._balance
    
    @property
    def operations_history(self) -> list[Operation]:
        # клон списка, чтобы нельзя было изменить вручную
        result = []
        for operation in self._operations_history:
            result.append(str(operation))
        return result

    def __str__(self):
        """Строковое представление банковского счета.

        Returns:
            str: Строка, содержащая id счета, текущий баланс и владельца счёта.
        """
        return f'Id: {self.id}, Balance: {self.balance}, Owner: \"{str(User)}\"'