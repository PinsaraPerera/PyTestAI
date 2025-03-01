# PyTestAI-Generator

`PyTestAI-Generator` is a **CLI tool** that automatically generates `pytest`-compatible test cases for your Python files using the **DeepSeek API**.  
It creates a ready-to-run test file (`test_<filename>.py`) in the same directory, ensuring **proper imports and test coverage**.The new version requires users to mark the functions they want to generate test cases for with the `@include_in_test` decorator.

---

## Features  

✔ **Automated Test Generation** – No need to write tests manually.  
✔ **AI-Powered** – Uses the DeepSeek API to generate meaningful test cases.  
✔ **Ready-to-Run** – Generates test files that can be executed directly with `pytest`.  
✔ **Customizable** – Includes AI-generated comments for better understanding.  
✔ **Simple CLI Interface** – Just run a command, and your tests are ready!  

---

## Installation  

### **Prerequisites**  
🔹 **Python 3.8 or higher**  
🔹 **A valid DeepSeek API key**  

### **Install the package**  
```bash
pip install PyTestAI-Generator
```

### **Set the DeepSeek API Key**  
Set your DeepSeek API key as an **environment variable**:  

#### ✅ macOS / Linux  
```bash
export DEEPSEEK_API_KEY="your_api_key_here"
```

#### ✅ Windows (Command Prompt)  
```cmd
set DEEPSEEK_API_KEY="your_api_key_here"
```

#### ✅ Windows (PowerShell)  
```powershell
$env:DEEPSEEK_API_KEY="your_api_key_here"
```

---

## 🛠 Usage  
### **New Usage Workflow**  
Starting with this version, you must mark the functions or classes you want to generate test cases for with the `@include_in_test` decorator. After marking the relevant functions/classes, you can use the `pytestai` command to generate the tests.

1. **Mark Functions/Classes with `@include_in_test`**  
   For every function or class you want to include in the test case generation, decorate it with `@include_in_test`. For example:
   ```python
   from PyTestAI import include_in_test

   @include_in_test
   def add(a, b):
       return a + b
   ```

2. **Generate the Test File**  
   Once your functions are decorated, run the `pytestai` command followed by the **path to your Python file**:
   ```bash
   pytestai path/to/your_file.py
   ```

   This will generate a test file named **`test_your_file.py`** in the same directory.

---

## Example  

Given a Python file **`math_ops.py`**:  
```python
# math_ops.py
from PyTestAI import include_in_test

@include_in_test
def add(a, b):
    return a + b

@include_in_test
def subtract(a, b):
    return a - b
```

Run:  
```bash
pytestai math_ops.py
```

This will generate **`test_math_ops.py`**:  
```python
# Here is a pytest-compatible test file for the `math_ops.py` module. This test file imports the `add` and `subtract` functions and includes test cases to verify their functionality.


# test_math_ops.py

# Import the functions to be tested
from math_ops import add, subtract

# Test cases for the add function
def test_add():
    # Test addition of two positive numbers
    assert add(2, 3) == 5, "Addition of 2 and 3 should be 5"
    
    # Test addition of a positive and a negative number
    assert add(-1, 1) == 0, "Addition of -1 and 1 should be 0"
    
    # Test addition of two negative numbers
    assert add(-5, -7) == -12, "Addition of -5 and -7 should be -12"
    
    # Test addition with zero
    assert add(0, 0) == 0, "Addition of 0 and 0 should be 0"
    assert add(5, 0) == 5, "Addition of 5 and 0 should be 5"

# Test cases for the subtract function
def test_subtract():
    # Test subtraction of two positive numbers
    assert subtract(5, 3) == 2, "Subtraction of 5 and 3 should be 2"
    
    # Test subtraction of a positive and a negative number
    assert subtract(5, -3) == 8, "Subtraction of 5 and -3 should be 8"
    
    # Test subtraction of two negative numbers
    assert subtract(-5, -3) == -2, "Subtraction of -5 and -3 should be -2"
    
    # Test subtraction with zero
    assert subtract(0, 0) == 0, "Subtraction of 0 and 0 should be 0"
    assert subtract(5, 0) == 5, "Subtraction of 5 and 0 should be 5"
    assert subtract(0, 5) == -5, "Subtraction of 0 and 5 should be -5"
```
---

## ⚙ Configuration  

### **Environment Variables**  
- `DEEPSEEK_API_KEY` – Your **DeepSeek API key** (required for the tool to function).

---

## 🎯 Contributing  

Contributions are **welcome**!

### **Steps to Contribute**  
1. **Fork** the repository.  
2. **Create a new branch** (`feature-branch`).  
3. **Make your changes & commit them** (`git commit -m "Added new feature"`).  
4. **Submit a pull request** on GitHub.  

💡 Feel free to open an **issue** if you encounter a bug or have a feature request!

---

## License  

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🛠 Support  

If you have any issues or questions, feel free to open an **issue** on the  
[GitHub Repository](https://github.com/PinsaraPerera/PyTestAI).

---

## 🙌 Acknowledgments  

- **DeepSeek** – For providing the AI-powered API used to generate test cases.  
- **pytest** – For being an amazing Python testing framework.  

---

## 👨‍💻 Author  

**[Pawan Perera](https://www.pawanperera.com)**  
- GitHub: [Pawan Perera](https://github.com/PinsaraPerera)  
- Email: 1pawanpinsara@gmail.com  

---

### **Important Change:**  
In the new version, you must decorate each function or class you want to include in the test case generation with the `@include_in_test` decorator. If no decorator is applied, that function/class will be excluded from the generated test cases.


