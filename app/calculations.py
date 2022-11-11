def add(a: int, b: int):
    return a+b


def substract(a: int, b: int):
    return a-b


def multiply(a: int, b: int):
    return a*b


def divide(a: int, b: int):
    try:
        return a/b
    except ZeroDivisionError:
        return None


class InsufficientFunds(Exception):
    pass


class BankAccount():
    def __init__(self, balance: int = 0):
        self.balance = balance

    def deposit(self, amount: int):
        self.balance += amount

    def withdraw(self, amount: int):
        if amount > self.balance:
            raise InsufficientFunds('Insufficient funds')
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
