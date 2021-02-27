import pytest


@pytest.fixture
def test_ok():
    print("ok")


def test_example():
    assert 1 == 1


def capital_case(x):
    return x.capitalize()


def test_fail():
    assert 1 == 2


def test_capital_case():
    assert capital_case('semaphore') == 'Semaphore'