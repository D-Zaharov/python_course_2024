import pytest
from factorial import factorial

def test_factorial_zero():
    assert factorial(0) == 1

def test_factorial_one():
    assert factorial(1) == 1

def test_factorial_positive():
    assert factorial(5) == 120
    assert factorial(3) == 6

def test_factorial_negative():
    with pytest.raises(ValueError):
        factorial(-1)