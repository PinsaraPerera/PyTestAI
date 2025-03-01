# PyTestAI/utils.py
import os
import re
import ast
from pathlib import Path

def _get_api_key() -> str:
    """
    Retrieves the DeepSeek API key from environment variables.

    Returns:
        str: The API key.

    Raises:
        ValueError: If the API key is not set in the environment.
    """
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "DEEPSEEK_API_KEY is not set. Please set it using:\n"
            "export DEEPSEEK_API_KEY='your_api_key_here'  (Linux/macOS)\n"
            "set DEEPSEEK_API_KEY='your_api_key_here'  (Windows CMD)\n"
            "$env:DEEPSEEK_API_KEY='your_api_key_here'  (PowerShell)"
        )
    
    return api_key

def _payload_setup(file_path: str, source_code: str, model: str = "deepseek-chat", tempreture: int = 1.0) -> dict:
    """
    Prepare the API request payload.

    Returns:
        dict: The API request payload.
    """
    return {
        "model": "deepseek-chat",
        "model": model,
        "tempreture": tempreture,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that generates pytest-compatible test cases "
                    "for Python code. The test cases should import all necessary functions, "
                    "classes, and modules from the original file. Include proper assertions "
                    "and test coverage for all major functionalities. The test file should "
                    "be ready to run directly with `pytest` without any modifications. "
                    "Any explanations or comments should be formatted as Python comments "
                    "using the '#' symbol."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Generate pytest test cases for the following Python file:\n\n"
                    f"File Path: {file_path}\n\n"
                    f"Source Code:\n```python\n{source_code}\n```"
                ),
            },
        ],
        "stream": False,
    }

# source code extraction
def _extract_marked_definitions(file_path: Path) -> str:
    """Extracts imports and functions/classes marked with @include_in_test, keeping other decorators but removing @include_in_test."""

    # Example: source code with functions/classes marked for test generation
    """ 
    import json
    from .mega import include_in_test

    def read_json_file(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
        
    @include_in_test
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        return n * factorial(n - 1)

    # this is an test class
    @include_in_test
    class Student:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        # this is getting name
        def get_name(self):
            return self.name

        def get_age(self):
            return self.age

    if __name__ == "__main__":
        print(factorial(5))
        student = Student("Alice", 20)
        print(student.get_name())
        print(student.get_age())
        print(read_json_file("data.json"))
    """
        
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()
    
    # Parse the source code into an AST
    tree = ast.parse(source_code)

    extracted_definitions = []
    extracted_imports = []

    for node in tree.body:
        # Extract import statements
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            extracted_imports.append(ast.get_source_segment(source_code, node))
        
        # Extract functions and classes with @include_in_test
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):  
            if any(isinstance(decorator, ast.Name) and decorator.id == "include_in_test" for decorator in node.decorator_list):
                definition_code = ast.get_source_segment(source_code, node)
                
                # Capture all decorators except @include_in_test
                decorators_code = [
                    "@" + ast.get_source_segment(source_code, decorator)
                    for decorator in node.decorator_list
                    if not (isinstance(decorator, ast.Name) and decorator.id == "include_in_test")
                ]

                # Combine decorators (without @include_in_test) and function/class definition
                full_definition_code = "\n".join(decorators_code) + "\n" + definition_code if decorators_code else definition_code
                extracted_definitions.append(full_definition_code.strip())

    # Construct the final source code string
    extracted_code = "\n".join(extracted_imports) + "\n\n" + "\n\n".join(extracted_definitions)

    return extracted_code.strip()

def _clean_api_response(api_response: str) -> str:
    """
    Extracts Python code from the API response while converting non-code parts into comments.

    Args:
        api_response (str): The raw response from the API.

    Returns:
        str: A cleaned-up version of the test code with comments.
    """

    """api_response = 
        Here is a pytest-compatible test file for the provided Python code. The test file imports all necessary functions
        and classes from the original file and includes test cases for all major functionalities.

        ```python
        import pytest
        import os
        import json
        from deco import read_json_file, factorial, Student
        from abc import abstractmethod

        # Test cases for read_json_file function
        def test_read_json_file(tmpdir):
            # Create a temporary JSON file
            json_data = {"key": "value"}
            file_path = tmpdir.join("test.json")
            with open(file_path, "w") as f:
                json.dump(json_data, f)

            # Test reading the JSON file
            result = read_json_file(file_path)
            assert result == json_data

        @abstractmethod
        def test_read_json_file_nonexistent():
            # Test reading a non-existent file
            with pytest.raises(FileNotFoundError):
                read_json_file("nonexistent.json")

        # Test cases for factorial function
        def test_factorial_zero():
            assert factorial(0) == 1

        def test_factorial_one():
            assert factorial(1) == 1

        def test_factorial_positive():
            assert factorial(5) == 120

        def test_factorial_negative():
            with pytest.raises(RecursionError):
                factorial(-1)

        # Test cases for Student class
        def test_student_initialization():
            student = Student("John Doe", 20)
            assert student.name == "John Doe"
            assert student.age == 20

        def test_student_get_name():
            student = Student("Jane Doe", 22)
            assert student.get_name() == "Jane Doe"

        def test_student_get_age():
            student = Student("Alice", 25)
            assert student.get_age() == 25

        # Additional test cases for edge cases
        def test_factorial_large_number():
            assert factorial(10) == 3628800

        def test_student_with_empty_name():
            student = Student("", 30)
            assert student.get_name() == ""
            assert student.get_age() == 30

        def test_student_with_zero_age():
            student = Student("Bob", 0)
            assert student.get_name() == "Bob"
            assert student.get_age() == 0

        # Test case for invalid JSON file
        def test_read_invalid_json_file(tmpdir):
            # Create a temporary invalid JSON file
            invalid_json_data = "{invalid}"
            file_path = tmpdir.join("invalid.json")
            with open(file_path, "w") as f:
                f.write(invalid_json_data)

            # Test reading the invalid JSON file
            with pytest.raises(json.JSONDecodeError):
                read_json_file(file_path)
        ```

        ### Explanation:
        1. **`test_read_json_file(tmpdir)`**: Tests the `read_json_file` function by creating a temporary JSON file and verifying that the function correctly reads and returns the JSON data.
        2. **`test_read_json_file_nonexistent()`**: Tests the `read_json_file` function with a non-existent file path, expecting a `FileNotFoundError`.       
        3. **`test_factorial_zero()`**: Tests the `factorial` function with input `0`, which should return `1`.
        4. **`test_factorial_one()`**: Tests the `factorial` function with input `1`, which should return `1`.
        5. **`test_factorial_positive()`**: Tests the `factorial` function with a positive integer input (`5`), which should return `120`.
        6. **`test_factorial_negative()`**: Tests the `factorial` function with a negative integer input, expecting a `RecursionError`.
        7. **`test_student_initialization()`**: Tests the initialization of the `Student` class with valid name and age.
        8. **`test_student_get_name()`**: Tests the `get_name` method of the `Student` class.
        9. **`test_student_get_age()`**: Tests the `get_age` method of the `Student` class.
        10. **`test_factorial_large_number()`**: Tests the `factorial` function with a larger input (`10`), which should return `3628800`.
        11. **`test_student_with_empty_name()`**: Tests the `Student` class with an empty name.
        12. **`test_student_with_zero_age()`**: Tests the `Student` class with an age of `0`.
        13. **`test_read_invalid_json_file(tmpdir)`**: Tests the `read_json_file` function with an invalid JSON file, expecting a `json.JSONDecodeError`.     

        ### Running the Tests:
        To run the tests, save the test file (e.g., `test_deco.py`) and run the following command in the terminal:

        ```bash
        pytest test_deco.py
        ```

        This will execute all the test cases and report the results.
        """


    # Extract Python code from markdown blocks
    code_blocks = re.findall(r"```python(.*?)```", api_response, re.DOTALL)

    # Extract text outside of code blocks
    non_code_parts = re.split(r"```python.*?```", api_response, flags=re.DOTALL)

    # Convert non-code parts into comments
    # commented_text = "\n".join(
    #     "\n".join(f"# {line}" for line in part.strip().split("\n")) if part.strip() else ""
    #     for part in non_code_parts
    # )

    # multi line comment
    commented_text = "\n".join(
        f'"""{part.strip()}"""' if part.strip() else ""
        for part in non_code_parts
    )

    # Combine commented text with extracted code
    cleaned_code = f"{commented_text.strip()}\n\n" + "\n\n".join(code_blocks).strip()
    
    return cleaned_code.strip()




