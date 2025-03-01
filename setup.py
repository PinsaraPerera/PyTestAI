from setuptools import setup, find_packages

# Read long description from README.md safely
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PyTestAI-Generator",
    version="2.0.0",
    packages=find_packages(include=["PyTestAI", "PyTestAI.*"]),  
    install_requires=[
        "requests>=2.25.1,<2.32.3",
        "colorama>=0.4.6,<0.5.0",
        "tqdm>=4.62.1,<4.67.1",
        "pytest>=8.1.1,<8.4.4",
    ],
    entry_points={
        "console_scripts": [
            "pytestai=PyTestAI.cli:main",
        ],
    },
    description="A CLI tool to generate pytest test cases using AI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Pawan Pinsara",
    author_email="1pawanpinsara@gmail.com",
    url="https://github.com/PinsaraPerera/PyTestAI",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
)
