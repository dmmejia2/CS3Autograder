# import os
# import nbformat

# def extract_last_output_from_notebook(notebook_path):
#     """
#     Extracts the last line of output from a single .ipynb file.

#     Parameters:
#     - notebook_path: str, path to the .ipynb file.

#     Returns:
#     - str: The last line of output, or None if no output is found.
#     """
#     try:
#         # Open and read the notebook file
#         with open(notebook_path, 'r', encoding='utf-8') as nb_file:
#             notebook = nbformat.read(nb_file, as_version=4)

#         # Extract cells from the notebook
#         cells = notebook.get('cells', [])
#         if not cells:
#             return None

#         # Find the last executed code cell with outputs
#         for cell in reversed(cells):
#             if cell['cell_type'] == 'code' and 'outputs' in cell:
#                 outputs = cell['outputs']
#                 for output in outputs:
#                     if output.get('output_type') == 'stream' and 'text' in output:
#                         # Get the last line of the output
#                         last_output = output['text'].strip().split('\n')[-1]
#                         return last_output
#         return None
#     except Exception as e:
#         print(f"Error processing {notebook_path}: {e}")
#         return None

# def process_notebooks_in_directory(directory, output_file_path):
#     """
#     Processes all .ipynb files in a directory and writes the last output line from each to a text file.

#     Parameters:
#     - directory: str, path to the directory containing .ipynb files.
#     - output_file_path: str, path to the output text file.
#     """
#     try:
#         # Ensure the directory exists
#         if not os.path.isdir(directory):
#             print(f"Directory {directory} does not exist.")
#             return

#         # Find all .ipynb files in the directory
#         notebooks = [f for f in os.listdir(directory) if f.endswith('.ipynb')]
#         if not notebooks:
#             print(f"No .ipynb files found in {directory}.")
#             return

#         # Open the output file for writing
#         with open(output_file_path, 'w', encoding='utf-8') as out_file:
#             for notebook in notebooks:
#                 notebook_path = os.path.join(directory, notebook)
#                 print(f"Processing {notebook_path}...")
#                 last_output = extract_last_output_from_notebook(notebook_path)
#                 if last_output:
#                     out_file.write(f"{last_output}\n")
#                     print(f"Extracted last output from {notebook}.")
#                 else:
#                     print(f"No output found in {notebook}.")
#         print(f"All outputs written to {output_file_path}.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Example usage
# if __name__ == "__main__":
#     # Directory containing .ipynb files
#     notebook_directory = "/Users/daniel/Library/CloudStorage/OneDrive-TheUniversityofTexasatElPaso/Teaching/Fall 2024/CS3/CS3 Exams/Final Exam/Output"  # Replace with your directory path

#     # Path to the output text file
#     output_file = "/Users/daniel/Library/CloudStorage/OneDrive-TheUniversityofTexasatElPaso/Teaching/Fall 2024/CS3/CS3 Exams/Final Exam/Output/output.csv"

#     # Process all notebooks in the directory
#     process_notebooks_in_directory(notebook_directory, output_file)


import os
import nbformat

def extract_last_output_from_notebook(notebook_path):
    """
    Extracts the very last line of output from a single .ipynb file.

    Parameters:
    - notebook_path: str, path to the .ipynb file.

    Returns:
    - str: The very last line of printed output, or None if no output is found.
    """
    try:
        # Open and read the notebook file
        with open(notebook_path, 'r', encoding='utf-8') as nb_file:
            notebook = nbformat.read(nb_file, as_version=4)

        # Extract cells from the notebook
        cells = notebook.get('cells', [])
        if not cells:
            return None

        # Initialize a variable to store the last output
        last_output = None

        # Iterate through all code cells to find outputs
        for cell in cells:
            if cell['cell_type'] == 'code' and 'outputs' in cell:
                for output in cell['outputs']:
                    # Handle stream outputs (e.g., print statements)
                    if output.get('output_type') == 'stream' and 'text' in output:
                        last_output = output['text'].strip().split('\n')[-1]

                    # Handle execution result outputs (e.g., display statements)
                    elif output.get('output_type') == 'execute_result' and 'data' in output:
                        if 'text/plain' in output['data']:
                            last_output = output['data']['text/plain'].strip()

        return last_output
    except Exception as e:
        print(f"Error processing {notebook_path}: {e}")
        return None

def process_notebooks_in_directory(directory, output_file_path):
    """
    Processes all .ipynb files in a directory and writes the very last output line from each to a text file.

    Parameters:
    - directory: str, path to the directory containing .ipynb files.
    - output_file_path: str, path to the output text file.
    """
    try:
        # Ensure the directory exists
        if not os.path.isdir(directory):
            print(f"Directory {directory} does not exist.")
            return

        # Find all .ipynb files in the directory
        notebooks = [f for f in os.listdir(directory) if f.endswith('.ipynb')]
        if not notebooks:
            print(f"No .ipynb files found in {directory}.")
            return

        # Open the output file for writing
        with open(output_file_path, 'w', encoding='utf-8') as out_file:
            for notebook in notebooks:
                notebook_path = os.path.join(directory, notebook)
                print(f"Processing {notebook_path}...")
                last_output = extract_last_output_from_notebook(notebook_path)
                if last_output:
                    out_file.write(f"{notebook},{last_output}\n")
                    print(f"Extracted last output from {notebook}.")
                else:
                    print(f"No output found in {notebook}.")
        print(f"All outputs written to {output_file_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Directory containing .ipynb files
    notebook_directory = "/Users/daniel/Desktop/CS3 Exams/Exam 3/Output"  # Replace with your directory path

    # Path to the output text file
    output_file = "/Users/daniel/Desktop/CS3 Exams/Exam 3/Output/Exam3Grades.csv"  # Replace with your desired output file path

    # Process all notebooks in the directory
    process_notebooks_in_directory(notebook_directory, output_file)