from abc import ABC, abstractmethod
from core.BankAccount import BankAccount
from decimal import Decimal

operation_id_counter = 0

class Operation(ABC):
    """Абстрактный класс для всех финансовых операций с банковскими счетами.
    
    Attributes:
        id (int): уникальный идентефикатор (readonly)
        status (str): I - инициализирован, E - ошибка в выполнении, D - выполнен, U - выполнен и отменён (readonly)
        content (str): комментарий к операции (readonly)
    """

    __content = ''

    def __init__(self, content=''):
        operation_id_counter += 1
        self.__id = operation_id_counter

        self.__status = 'I'
        self.__content = content

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Абстрактный метод для выполнения операции.
        
        Принимает переменное количество аргументов, зависящих от типа операции.
        """
        pass

    @abstractmethod
    def undo(self, *args, **kwargs):
        """Абстрактный метод для отмены операции.

        Принимает переменное количество аргументов, зависящих от типа операции.
        """
        pass

    @abstractmethod
    def __str__(self):
        pass

    @property
    def id(self) -> int:
        return self.__id

    @property
    def status(self) -> str:
        # чтобы нельзя было изменять вручную
        return self.__status
    
    @property
    def content(self) -> str:
        '''комментарий к операции'''
        return self.__content


class DepositOperation(Operation):
    """Операция пополнения счёта.
    
    Attributes:
        bank_account (BankAccount): Аккаунт, на который производится депозит. (readonly)
        value (Decimal): сколько денег (readonly)
    """

    def __init__(self, bank_account: BankAccount, value: Decimal, content=''):
        """
        Args:
            bank_account (BankAccount): Объект счёта, который будет пополняться.

        Raises:
            ValueError: Если bank_account не является экземпляром класса BankAccount.
            ValueError: Если value не является экземпляром класса Decimal.
        """
        if not isinstance(bank_account, BankAccount):
            raise ValueError("bank_account must be instance of BankAccount class")
        if not isinstance(value, Decimal):
            raise ValueError("value must be instance of Decimal class")
        
        super().__init__(content=content)

        self.__bank_account = bank_account
        self.__value = value

    def execute(self):
        """Выполняет пополнение счета.
        Увеличивает баланс указанного счета на заданную сумму и записывает операцию.

        Returns:
            bool: True, если операция выполнена успешно.
        """
        if self.status != 'I': # операция уже выполнена
            return False
        self.bank_account._balance += self.value
        self.bank_account._operation_history.append(self)
        self.__status = 'D'
        return True

    def undo(self):
        """Отменяет операцию пополнения счета.
        Уменьшает баланс счета на ранее внесенную сумму. Уведомляет, если операция приводит к отрицательному счёту.

        Returns:
            bool: True, если операция выполнена успешно.
        """
        if self.status != 'D': # операция не выполнена или отменена
            return False
        self.bank_account._balance -= self.value
        self.__status = 'U'

        if self.bank_account._balance < 0:
            print(f"WARNING: После отмены <{str(self)}> счёт стал отрицательным")
        
        return True
    
    def __str__(self) -> str:
        return f"{self.id}: DepositOperation"
    
    @property
    def bank_account(self) -> BankAccount:
        return self.__bank_account
    
    @property
    def value(self) -> int:
        return self.__value


class WithdrawalOperation(Operation):
    """Операция снятия средств со счёта.
    
    Attributes:
        bank_account (BankAccount): Аккаунт, с которого снимают деньги. (readonly)
        value (Decimal): сколько денег (readonly)
    """

    def __init__(self, bank_account: BankAccount, value: Decimal, content=''):
        """
        Args:
            bank_account (BankAccount): Объект счёта, с которого будет списание.

        Raises:
            ValueError: Если bank_account не является экземпляром класса BankAccount.
            ValueError: Если value не является экземпляром класса Decimal.
        """
        if not isinstance(bank_account, BankAccount):
            raise ValueError("bank_account must be instance of BankAccount class")
        if not isinstance(value, Decimal):
            raise ValueError("value must be instance of Decimal class")
        
        super().__init__()

        self.__bank_account = bank_account
        self.__value = value

    def execute(self):
        """Выполняет снятие со счёта.

        Returns:
            bool: True, если операция выполнена успешно.
        """
        if self.status != 'I': # операция уже выполнена
            return False
        
        if self.bank_account._balance - self.value < 0:
            self.__status = 'E'
            return False
        self.bank_account._balance -= self.value
        self.bank_account._operation_history.append(self)
        self.__status = 'D'
        return True

    def undo(self):
        """Отменяет операцию пополнения счета.
        Уменьшает баланс счета на ранее внесенную сумму. Уведомляет, если операция приводит к отрицательному счёту.

        Returns:
            bool: True, если операция выполнена успешно.
        """
        if self.status != 'D': # операция не выполнена или отменена
            return False

        self.bank_account._balance += self.value
        self.__status = 'U'
        
        return True
    
    def __str__(self) -> str:
        return f"{self.id}: WithdrawalOperation"
    
    @property
    def bank_account(self) -> BankAccount:
        return self.__bank_account
    
    @property
    def value(self) -> int:
        return self.__value


class InterestAccrualOperation(DepositOperation):
    """Представляет операцию начисления процентов на банковский счет.
    """

    def __init__(self, bank_account: BankAccount, rate: Decimal):
        """
        Args:
            bank_account (BankAccount): Объект счёта, который будет пополняться.

        Raises:
            ValueError: Если bank_account не является экземпляром класса BankAccount.
            ValueError: Если rate не является экземпляром класса Decimal.
        """
        if not isinstance(bank_account, BankAccount):
            raise ValueError("bank_account must be instance of BankAccount class")
        if not isinstance(rate, Decimal):
            raise ValueError("rate must be instance of Decimal class")
        
        super().__init__(bank_account=bank_account, value=rate * bank_account.balance)