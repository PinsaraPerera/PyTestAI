# PyTestAI/tests/test_generator.py
from PyTestAI import include_in_test

@include_in_test
def add_two_integers(a: int, b: int) -> int:
    return a + b

result = add_two_integers(3,4)
print(result)