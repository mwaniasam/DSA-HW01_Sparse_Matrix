Sparse Matrix Operations

Overview
This Python program implements a `SparseMatrix` class to efficiently store and perform operations on large sparse matrices. The program reads sparse matrices from input files, performs addition, subtraction, and multiplication operations, and allows the user to save the results to a file.


Directory Structure
The project is organized as follows:

dsa/
├── sparse_matrix/
│   ├── code/
│   │   └── src/
│   │       └── sparse_matrix.py       # Main Python script
│   ├── sample_inputs/
│   │   ├── matrixfile1.txt            # Sample input file 1
│   │   ├── matrixfile2.txt            # Sample input file 2
│   │   └── result_matrix.txt          # Output file for results
└── README.md                          # This file


Requirements
Python 3.x
Input files in the specified format (see Input File Format below).


Input File Format
Input files must follow this format:

rows=<number_of_rows>
cols=<number_of_columns>
(row, column, value)
(row, column, value)
...

Example:

rows=8433
cols=3180
(0, 381, -694)
(0, 128, -838)
(0, 639, 857)


How to Run the Code
1.Clone or Download the Repository:
   Ensure the directory structure is maintained as shown above.
   Place your input files in the `/dsa/sparse_matrix/sample_inputs/` directory.

2.Run the Script:
   Navigate to the `/dsa/sparse_matrix/code/src/` directory and run the script:
   python sparse_matrix.py

3.Follow the Prompts:
   The program will load the matrices from the input files.
   Choose an operation (addition, subtraction, or multiplication).
   Optionally save the result to a file.


Features
Efficient Storage: Uses a dictionary to store only non-zero elements, optimizing memory usage.
Matrix Operations:
  Addition
  Subtraction
  Multiplication
Input Validation:
  Checks for invalid formats, floating-point values, and mismatched dimensions.
User Interaction:
  Allows the user to select an operation and save the result.


Implementation Details
Classes
SparseMatrix:
  Stores the matrix dimensions and non-zero elements in a dictionary.
  Methods:
    load_from_file(file_path): Loads a matrix from a file.
    get_element(row, col): Retrieves the value at a specific position.
    set_element(row, col, value): Sets the value at a specific position.
    add(other): Adds two matrices.
    subtract(other): Subtracts one matrix from another.
    multiply(other): Multiplies two matrices.
    save_to_file(file_path): Saves the matrix to a file.

Error Handling
Handles the following errors:
  File not found.
  Invalid file format (e.g., floating-point values, incorrect parentheses).
  Mismatched dimensions for matrix operations.

Example Usage
1.Input Files:
matrixfile1.txt:
     rows=3
     cols=3
     (0, 0, 1)
     (1, 1, 2)
     (2, 2, 3)

matrixfile2.txt:
     rows=3
     cols=3
     (0, 0, 4)
     (1, 1, 5)
     (2, 2, 6)

2. Run the Script:
    python3 sparse_matrix.py

3. Output:
   Matrix 1: 3x3
   Matrix 2: 3x3
   Choose an operation:
   1. Addition
   2. Subtraction
   3. Multiplication
   Enter your choice (1/2/3): 1
   Result of Addition:
   {(0, 0): 5, (1, 1): 7, (2, 2): 9}
   Do you want to save the result? (yes/no): yes
   Result saved to /dsa/sparse_matrix/sample_inputs/result_matrix.txt

Limitations
    The program assumes that the input files are well-formatted and does not handle extremely large files that exceed system memory.


Contributing
    If you would like to contribute to this project, feel free to open an issue or submit a pull request.
