# PyTestAI/cli.py

import argparse
import sys
from pathlib import Path
from .generator import generate_test_cases

def display_menu():
    """Display menu when no arguments are provided."""
    print("\nPython Test Case Generator CLI")
    print("=" * 35)
    print("Usage:")
    print("  generate-tests <file_path>")
    print("\nOptions:")
    print("  -h, --help    Show this help message and exit")
    print("\nExample:")
    print("  generate-tests my_script.py\n")

def main():
    parser = argparse.ArgumentParser(description="Generate pytest test cases for a Python file.")
    parser.add_argument("file_path", type=str, nargs="?", help="Path to the Python file.")

    args = parser.parse_args()

    if not args.file_path:
        display_menu()
        sys.exit(1)

    file_path = Path(args.file_path)

    if not file_path.exists():
        print(f"Error: The file '{file_path}' does not exist.")
        sys.exit(1)

    if not file_path.is_file():
        print(f"Error: '{file_path}' is not a valid file.")
        sys.exit(1)

    try:
        test_file_path = generate_test_cases(file_path)
        print(f"✅ Test file generated: {test_file_path}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
