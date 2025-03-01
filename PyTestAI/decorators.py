# PyTestAI/decorators.py
def include_in_test(func):
    """Decorator to mark functions/classes to be included in test cases."""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper