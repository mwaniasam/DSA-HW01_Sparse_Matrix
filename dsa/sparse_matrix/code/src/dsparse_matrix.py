import os
import time  # Import the time module to generate unique filenames

class SparseMatrix:
    def __init__(self, file_path=None, rows=0, cols=0):
        """
        Initializes a SparseMatrix object.
        Args:
            file_path (str, optional): Path to the input file. Defaults to None.
            rows (int, optional): Number of rows. Defaults to 0.
            cols (int, optional): Number of columns. Defaults to 0.
        """
        self.rows = rows
        self.cols = cols
        self.matrix = {}  # Dictionary to store non-zero elements

        if file_path:
            self.load_from_file(file_path)

    def load_from_file(self, file_path):
        """
        Loads a sparse matrix from a file.
        Args:
            file_path (str): Path to the input file.
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file has an invalid format.
        """
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file if line.strip()]
                if not lines:
                    raise ValueError("Input file is empty.")

                # Read rows and columns
                self.rows = int(lines[0].split('=')[1].strip())
                self.cols = int(lines[1].split('=')[1].strip())

                # Read matrix elements
                for line in lines[2:]:
                    if not line.startswith('(') or not line.endswith(')'):
                        raise ValueError("Input file has wrong format.")

                    try:
                        row, col, value = map(int, line.strip('()').split(','))
                        self.matrix[(row, col)] = value
                    except ValueError:
                        raise ValueError("Input file has wrong format: floating-point values or invalid format.")
        except FileNotFoundError:
            raise FileNotFoundError("Matrix file not found.")

    def get_element(self, row, col):
        """
        Retrieves the value at a specific row and column.
        Args:
            row (int): Row index.
            col (int): Column index.
        Returns:
            int: The value at the specified position (0 if not found).
        """
        return self.matrix.get((row, col), 0)

    def set_element(self, row, col, value):
        """
        Sets the value at a specific row and column.
        Args:
            row (int): Row index.
            col (int): Column index.
            value (int): Value to set.
        """
        if value != 0:
            self.matrix[(row, col)] = value
        elif (row, col) in self.matrix:
            del self.matrix[(row, col)]

    def add(self, other):
        """
        Adds two sparse matrices.
        Args:
            other (SparseMatrix): The other matrix to add.
        Returns:
            SparseMatrix: The result of the addition.
        Raises:
            ValueError: If matrix dimensions do not match.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for addition.")

        result = SparseMatrix(rows=self.rows, cols=self.cols)

        keys = set(self.matrix.keys()).union(other.matrix.keys())
        for key in keys:
            value = self.get_element(*key) + other.get_element(*key)
            result.set_element(*key, value)

        return result

    def subtract(self, other):
        """
        Subtracts one sparse matrix from another.
        Args:
            other (SparseMatrix): The matrix to subtract.
        Returns:
            SparseMatrix: The result of the subtraction.
        Raises:
            ValueError: If matrix dimensions do not match.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must match for subtraction.")

        result = SparseMatrix(rows=self.rows, cols=self.cols)

        keys = set(self.matrix.keys()).union(other.matrix.keys())
        for key in keys:
            value = self.get_element(*key) - other.get_element(*key)
            result.set_element(*key, value)

        return result

    def multiply(self, other):
        """
        Multiplies two sparse matrices.
        Args:
            other (SparseMatrix): The matrix to multiply with.
        Returns:
            SparseMatrix: The result of the multiplication.
        Raises:
            ValueError: If the number of columns in the first matrix does not match the number of rows in the second matrix.
        """
        if self.cols != other.rows:
            raise ValueError("Number of columns in the first matrix must equal the number of rows in the second matrix for multiplication.")

        result = SparseMatrix(rows=self.rows, cols=other.cols)

        for (i, k), v in self.matrix.items():
            for j in range(other.cols):
                if (k, j) in other.matrix:
                    result.set_element(i, j, result.get_element(i, j) + v * other.matrix[(k, j)])

        return result

    def multiply_scalar(self, scalar):
        """
        Multiplies the matrix by a scalar value.
        Args:
            scalar (int): The scalar value to multiply with.
        Returns:
            SparseMatrix: The result of the scalar multiplication.
        """
        result = SparseMatrix(rows=self.rows, cols=self.cols)

        for (row, col), value in self.matrix.items():
            result.set_element(row, col, value * scalar)

        return result

    def save_to_file(self, file_path):
        """
        Saves the sparse matrix to a file.
        Args:
            file_path (str): Path to the output file.
        """
        with open(file_path, 'w') as file:
            file.write(f"rows={self.rows}\n")
            file.write(f"cols={self.cols}\n")
            for (row, col), value in sorted(self.matrix.items()):
                file.write(f"({row}, {col}, {value})\n")


if __name__ == "__main__":
    # Set the base path for input and output files
    base_path = os.path.join(os.getcwd(), "dsa", "sparse_matrix")
    input_dir = os.path.join(base_path, "sample_inputs")
    output_dir = os.path.join(base_path, "sample_results")

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define input file paths
    file1 = os.path.join(input_dir, "matrixfile1.txt")
    file2 = os.path.join(input_dir, "matrixfile1 copy.txt")

    # Load matrices from files
    try:
        matrix1 = SparseMatrix(file1)
        matrix2 = SparseMatrix(file2)
    except Exception as e:
        print(f"Error: {e}")
        exit()

    # Display matrix dimensions
    print(f"Matrix 1: {matrix1.rows}x{matrix1.cols}")
    print(f"Matrix 2: {matrix2.rows}x{matrix2.cols}")

    # Prompt user for operation
    print("Choose an operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Scalar Multiplication")

    choice = input("Enter your choice (1/2/3/4): ")

    try:
        # Generate a unique timestamp for the filename
        timestamp = int(time.time())

        if choice == "1":
            result = matrix1.add(matrix2)
            operation_name = "addition"
            file_name = os.path.join(output_dir, f"result_addition_{timestamp}.txt")
        elif choice == "2":
            result = matrix1.subtract(matrix2)
            operation_name = "subtraction"
            file_name = os.path.join(output_dir, f"result_subtraction_{timestamp}.txt")
        elif choice == "3":
            result = matrix1.multiply(matrix2)
            operation_name = "multiplication"
            file_name = os.path.join(output_dir, f"result_multiplication_{timestamp}.txt")
        elif choice == "4":
            scalar = int(input("Enter the scalar value (integer): "))
            result = matrix1.multiply_scalar(scalar)
            operation_name = f"scalar_multiplication_{scalar}"
            file_name = os.path.join(output_dir, f"result_scalar_multiplication_{scalar}_{timestamp}.txt")
        else:
            print("Invalid choice. Exiting.")
            exit()

        # Display result
        print(f"Result of {operation_name}:")
        print(result.matrix)

        # Prompt user to save result
        save_choice = input("Do you want to save the result? (yes/no): ")
        if save_choice.lower() == "yes":
            result.save_to_file(file_name)
            print(f"Result saved to {file_name}")
        else:
            print("Result not saved.")
    except Exception as e:
        print(f"Error: {e}")