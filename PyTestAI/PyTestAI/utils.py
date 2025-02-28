# PyTestAI/utils.py
import os

def get_api_key():
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

def payload_setup(file_path: str, source_code: str) -> dict:
    """
    Prepare the API request payload.

    Returns:
        dict: The API request payload.
    """
    return {
        "model": "deepseek-chat",
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
