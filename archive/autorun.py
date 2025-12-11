import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def execute_notebook(notebook_filename, output_filename=None, timeout=600):
    """
    Executes a Jupyter Notebook (.ipynb) file and saves the executed output.

    Parameters:
    - notebook_filename: str, path to the input .ipynb file.
    - output_filename: str (optional), path to save the executed notebook.
    - timeout: int, maximum execution time in seconds.
    """
    try:
        # Ensure nbformat is available
        if not nbformat:
            raise ImportError("nbformat module not found. Install it using `pip install nbformat`")

        # Read the notebook content
        with open(notebook_filename, 'r', encoding='utf-8') as nb_file:
            notebook = nbformat.read(nb_file, as_version=4)

        # Configure the notebook executor
        executor = ExecutePreprocessor(timeout=timeout, kernel_name='python3')

        # Execute the notebook
        executor.preprocess(notebook, {'metadata': {'path': os.path.dirname(notebook_filename)}})
        print(f"Execution of {notebook_filename} completed successfully.")

        # Save the executed notebook
        output_path = output_filename if output_filename else notebook_filename
        with open(output_path, 'w', encoding='utf-8') as nb_file:
            nbformat.write(notebook, nb_file)
            print(f"Executed notebook saved as {output_path}.")
    
    except ImportError as e:
        print(f"Module Import Error: {e}. Try running `pip install nbformat nbconvert`.")
    except TimeoutError:
        print(f"TimeoutError: Execution of {notebook_filename} exceeded {timeout} seconds. Skipping...")
    except Exception as e:
        print(f"Error executing {notebook_filename}: {e}")

def execute_notebooks_in_directory(directory, output_dir=None, timeout=600):
    """
    Executes all .ipynb files in a directory.

    Parameters:
    - directory: str, path to the directory containing .ipynb files.
    - output_dir: str (optional), directory to save executed notebooks.
    - timeout: int, maximum execution time in seconds.
    """
    if not os.path.isdir(directory):
        print(f"Directory {directory} does not exist.")
        return

    notebooks = [f for f in os.listdir(directory) if f.endswith('.ipynb')]
    if not notebooks:
        print(f"No .ipynb files found in {directory}.")
        return

    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    for notebook in notebooks:
        input_path = os.path.join(directory, notebook)
        output_path = os.path.join(output_dir, notebook) if output_dir else None
        print(f"Processing {notebook}...")
        execute_notebook(input_path, output_path, timeout=timeout)

# Example usage
if __name__ == "__main__":
    notebook_directory = "/Users/daniel/Desktop/CS3 Exams/Exam 3/Input"
    output_directory = "/Users/daniel/Desktop/CS3 Exams/Exam 3/Output"
    execution_timeout = 20

    execute_notebooks_in_directory(notebook_directory, output_directory, timeout=execution_timeout)
