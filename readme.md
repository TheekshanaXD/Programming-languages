# RPAL Compiler Project

This project features a compiler for the **RPAL language**, meticulously developed in Python. It's designed to process RPAL programs, offering functionalities to execute them and inspect their Abstract Syntax Tree (AST) and Standardized AST (ST).

------

## Features

- **RPAL Program Execution**: Compile and run RPAL source code.
- **Abstract Syntax Tree (AST) Generation**: Visualize the program's structure as an AST.
- **Standardized AST (ST) Generation**: View the program's structure in a standardized AST format.
- **Flexible Input**: Supports a main input file (`input.txt`) and additional test cases from a dedicated `tests/` directory.
- **Automated Tasks**: Includes a `Makefile` for streamlined command execution (requires `make` to be installed).

------

## Project Structure

Your project's core files are organized as follows:

- **`myrpal.py`**: The main Python script containing the compiler logic.
- **`input.txt`**: The primary RPAL test program located in the project's root directory.
- **`tests/`**: A directory containing additional RPAL test case files (e.g., `ex1.rpal`, `ex2.rpal`, etc.).
- **`Makefile`**: (Optional) For users with `make` installed, this file provides shortcuts for common operations.

------

## Prerequisites

To run this project, you'll need:

- **Python 3**: Ensure you have a recent version of Python 3 installed on your system. You can download it from [python.org](https://www.python.org/).
- **`make` (Optional but Recommended)**: While not strictly required, having `make` installed (e.g., via WSL, Chocolatey, or Git  on Windows) simplifies command execution using the provided `Makefile`.

------

## Usage

Navigate to the root directory of your project (e.g., `Programming-Languages-Project`) in your command line before running any commands.

You can interact with the compiler using two methods: direct Python execution or via `make`.

### 1. Direct Python Execution

This method uses standard Python commands and works on any system with Python installed.

- **Syntax:**

  ```bash
  python .\myrpal.py <input_file_path> [options]
  ```

- **To Compile and Run an RPAL Program:**

  ```Bash
  python .\myrpal.py input.txt
  ```

  - Example with a test file:

    ```
    python .\myrpal.py .\tests\Test_7.rpal
    ```

- **To Print the Abstract Syntax Tree (AST):**

  ```bash
  python .\myrpal.py input.txt -ast
  ```

  - Example with a test file:

    ```bash
    python .\myrpal.py .\tests\Test_7.rpal -ast
    ```

- **To Print the Standardized Abstract Syntax Tree (ST):**

  ```bash
  python .\myrpal.py input.txt -st
  ```

  - Example with a test file:

    ```bash
    python .\myrpal.py .\tests\Test_7.rpal -st
    ```

### 2. Using `make`

If you have `make` installed, you can use the `Makefile` for more concise commands.

- **Syntax:**

  ```bash
  make <target> file=<input_file_path>
  ```

- **To Compile and Run an RPAL Program:**

  ```bash
  make run file=./input.txt
  ```

  - Example with a test file:

    ```bash
    make run file=./tests/Test_7.rpal
    ```

- **To Print the Abstract Syntax Tree (AST):**

  ```bash
  make ast file=./input.txt
  ```

  - Example with a test file:

    ```bash
    make ast file=./tests/Test_7.rpal
    ```

- **To Print the Standardized Abstract Syntax Tree (ST):**

  ```bash
  make st file=./input.txt
  ```

  - Example with a test file:

    ```bash
    make st file=./tests/Test_7.rpal
    ```



### Cleaning Up

To remove generated Python bytecode files (`.pyc` and `_pycache_` directories), use the `clean` target:



```
make clean
```

------



## Getting Started

1. **Clone this repository** to your local machine.
2. **Navigate** to the project's root directory in your terminal.
3. **Ensure Python 3** is installed and accessible in your system's PATH.
4. (Optional) **Install `make`** if you plan to use the `Makefile` shortcuts.
5. Begin by running an example: `python .\myrpal.py input.txt` or `make run file=./input.txt`.