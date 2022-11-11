from app.calculations import add, substract, multiply, divide, BankAccount, InsufficientFunds
import pytest

# create empty account


@pytest.fixture
def empty_account():
    return BankAccount()

# create account with 100


@pytest.fixture
def account_100():
    return BankAccount(100)


@pytest.mark.parametrize("a, b, result", [
    (1, 1, 2),
    (2, 1, 3),
    (3, 1, 4),
    (4, 2, 6)
])
def test_add(a, b, result):
    assert add(a, b) == result


@pytest.mark.parametrize("a, b, result", [
    (1, 1, 0),
    (1, 2, -1),
    (3, 1, 2),
    (4, 2, 2)
])
def test_substract(a, b, result):
    assert substract(a, b) == result


def test_multiply():
    assert multiply(7, 3) == 21


def test_divide():
    assert divide(9, 3) == 3
    assert divide(7, 0) is None


def test_bank_set_initial_amount(account_100):
    assert account_100.balance == 100


def test_bank_default_amount(empty_account):
    assert empty_account.balance == 0

# test deposit


def test_bank_deposit(account_100):
    assert account_100.balance == 100

# test withdraw


def test_bank_withdraw(account_100):
    account_100.withdraw(50)
    assert account_100.balance == 50

# test collect interest
def test_collect_interest(account_100):
    account_100.collect_interest()
    assert account_100.balance == 100*1.1


@pytest.mark.parametrize("a, b, result", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000),
])
def test_bank_transaction(empty_account, a, b, result):
    empty_account.deposit(a)
    empty_account.withdraw(b)
    assert empty_account.balance == result

def test_insufficient_funds(account_100):
    with pytest.raises(InsufficientFunds):
        account_100.withdraw(1000)
