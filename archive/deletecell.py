import os
import nbformat

def delete_specific_cell_from_notebooks(directory, output_directory, unique_code_fragment):
    """
    Deletes a specific cell from all Jupyter Notebooks in a directory based on a unique code fragment.

    Parameters:
    - directory: str, path to the directory containing the .ipynb files.
    - output_directory: str, path to save the modified .ipynb files.
    - unique_code_fragment: str, a unique piece of text to identify the cell to delete.
    """
    try:
        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Get a list of all .ipynb files in the directory
        notebooks = [f for f in os.listdir(directory) if f.endswith('.ipynb')]
        if not notebooks:
            print(f"No .ipynb files found in {directory}.")
            return

        print(f"Found {len(notebooks)} notebook(s) to process.")

        for notebook_name in notebooks:
            input_path = os.path.join(directory, notebook_name)
            output_path = os.path.join(output_directory, notebook_name)

            # Load the notebook
            with open(input_path, 'r', encoding='utf-8') as nb_file:
                notebook = nbformat.read(nb_file, as_version=4)

            # Identify and delete the cell
            original_cell_count = len(notebook['cells'])
            notebook['cells'] = [
                cell for cell in notebook['cells']
                if unique_code_fragment not in cell.get('source', '')
            ]
            updated_cell_count = len(notebook['cells'])

            if original_cell_count != updated_cell_count:
                print(f"Deleted {original_cell_count - updated_cell_count} cell(s) from {notebook_name}.")
            else:
                print(f"No matching cells found in {notebook_name}.")

            # Save the updated notebook
            with open(output_path, 'w', encoding='utf-8') as nb_file:
                nbformat.write(notebook, nb_file)

        print(f"Processing completed. Updated notebooks saved to {output_directory}.")
    except Exception as e:
        print(f"Error processing notebooks: {e}")

# Example usage
if __name__ == "__main__":
    # Path to the directory containing .ipynb files
    input_directory = "/Users/daniel/Library/CloudStorage/OneDrive-TheUniversityofTexasatElPaso/Teaching/Fall 2024/CS3/CS3 Exams/Final Exam/InputTwo"  # Update this path as needed

    # Path to save modified .ipynb files
    output_directory = "/Users/daniel/Library/CloudStorage/OneDrive-TheUniversityofTexasatElPaso/Teaching/Fall 2024/CS3/CS3 Exams/Final Exam/InputThree"  # Update this path as needed

    # Unique code fragment to identify the cell to delete
    unique_code_fragment = "def grade_p1(answer_list_points):"  # Replace with the unique identifier

    # Process all notebooks in the input directory
    delete_specific_cell_from_notebooks(input_directory, output_directory, unique_code_fragment)
