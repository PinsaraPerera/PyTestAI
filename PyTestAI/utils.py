# PyTestAI/utils.py
import os
import re
import ast
from pathlib import Path

def get_api_key() -> str:
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

def payload_setup(file_path: str, source_code: str, model: str = "deepseek-chat", tempreture: int = 1.0) -> dict:
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
def extract_marked_definitions(file_path: Path) -> str:
    """Extracts imports and functions/classes marked with @include_in_test and returns them as a single string."""
    
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
                extracted_definitions.append(definition_code)

    # initialize extracted_imports with PyTestAI import
    extracted_imports.insert(0, "from PyTestAI import include_in_test")

    # Construct the final source code string
    extracted_code = "\n".join(extracted_imports) + "\n\n" + "\n\n".join(extracted_definitions)

    return extracted_code.strip()

def clean_api_response(api_response: str) -> str:
    """
    Extracts Python code from the API response while converting non-code parts into comments.

    Args:
        api_response (str): The raw response from the API.

    Returns:
        str: A cleaned-up version of the test code with comments.
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




