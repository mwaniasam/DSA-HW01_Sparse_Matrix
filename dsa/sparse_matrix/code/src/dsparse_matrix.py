import os

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
    # Set the base path for input files
    base_path = os.path.join(os.getcwd(), "dsa", "sparse_matrix", "sample_inputs")
    file1 = os.path.join(base_path, r"C:\Users\LENOVO\.vscode\DSA-HW01_Sparse_Matrix\dsa\sparse_matrix\sample_inputs\matrixfile1.txt")
    file2 = os.path.join(base_path, r"C:\Users\LENOVO\.vscode\DSA-HW01_Sparse_Matrix\dsa\sparse_matrix\sample_inputs\matrixfile1 copy.txt")

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

    choice = input("Enter your choice (1/2/3): ")

    try:
        if choice == "1":
            result = matrix1.add(matrix2)
            operation_name = "Addition"
        elif choice == "2":
            result = matrix1.subtract(matrix2)
            operation_name = "Subtraction"
        elif choice == "3":
            result = matrix1.multiply(matrix2)
            operation_name = "Multiplication"
        else:
            print("Invalid choice. Exiting.")
            exit()

        # Display result
        print(f"Result of {operation_name}:")
        print(result.matrix)

        # Prompt user to save result
        save_choice = input("Do you want to save the result? (yes/no): ")
        if save_choice.lower() == "yes":
            file_name = input("Enter a file name to save the result (e.g., my_matrix.txt): ")
            file_path = os.path.join(base_path, file_name)
            dir_path = os.path.dirname(file_path)
            
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            
            result.save_to_file(file_path)
            print(f"Result saved to {file_path}")
        else:
            print("Result not saved.")
    except Exception as e:
        print(f"Error: {e}")