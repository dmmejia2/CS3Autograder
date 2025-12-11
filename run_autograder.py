#!/usr/bin/env python3
"""
Unified CS3 Autograder
Combines all three steps: adding autograder cell, executing notebooks, and reading results
"""

import os
import json
import textwrap
import shutil
import sys
import re
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from config import (
    INPUT_DIR, OUTPUT_DIR, GRADES_CSV, 
    EXECUTION_TIMEOUT, AUTOGRADER_CODE
)


def extract_username_from_filename(filename):
    """
    Extracts username from notebook filename.
    Expected format: "Exam Three - Part I_username_attempt_..."
    
    Returns:
        str: Username or None if not found
    """
    try:
        # Remove .ipynb extension
        name = filename.replace('.ipynb', '')
        
        # Try to find username pattern: text_username_attempt or text_username_attempt
        # Common patterns:
        # - "Part I_username_attempt"
        # - "Part I_username_attempt_"
        # - "_username_attempt"
        
        # Look for pattern: _username_attempt
        match = re.search(r'_([a-zA-Z0-9]+)_attempt', name)
        if match:
            return match.group(1)
        
        # Alternative: look for pattern after "Part I_" or similar
        match = re.search(r'Part\s+I_([a-zA-Z0-9]+)_', name)
        if match:
            return match.group(1)
        
        # Try to find any word between underscores that looks like a username
        # (alphanumeric, typically lowercase)
        parts = name.split('_')
        for i, part in enumerate(parts):
            # Username is usually after "Part I" or similar exam identifier
            if i > 0 and len(part) > 0 and part.isalnum() and part.islower():
                # Check if next part is "attempt" or a date
                if i + 1 < len(parts):
                    next_part = parts[i + 1]
                    if next_part == 'attempt' or (len(next_part) > 4 and next_part.replace('-', '').isdigit()):
                        return part
        
        return None
    except Exception:
        return None


def add_autograder_cell(notebook_path):
    """
    Adds the autograder cell to a notebook.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Check if autograder cell already exists
        for cell in notebook.get('cells', []):
            if 'DO NOT MODIFY THE CODE BELOW' in cell.get('source', ''):
                print(f"  Autograder cell already exists in {os.path.basename(notebook_path)}")
                return True
        
        # Remove any common leading whitespace
        code_block = textwrap.dedent(AUTOGRADER_CODE)
        
        # Create a new code cell
        cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": code_block.splitlines(keepends=True)
        }
        
        # Append the new cell
        notebook['cells'].append(cell)
        
        # Write back to the notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1)
        
        return True
    except Exception as e:
        print(f"  ERROR adding autograder cell to {os.path.basename(notebook_path)}: {e}")
        return False


def execute_notebook(notebook_path, output_path):
    """
    Executes a notebook and saves the result.
    
    Returns:
        bool: True if successful, False if crashed
    """
    try:
        # Read the notebook content
        with open(notebook_path, 'r', encoding='utf-8') as nb_file:
            notebook = nbformat.read(nb_file, as_version=4)
        
        # Configure the notebook executor
        executor = ExecutePreprocessor(timeout=EXECUTION_TIMEOUT, kernel_name='python3')
        
        # Execute the notebook
        executor.preprocess(notebook, {'metadata': {'path': os.path.dirname(notebook_path)}})
        
        # Save the executed notebook
        with open(output_path, 'w', encoding='utf-8') as nb_file:
            nbformat.write(notebook, nb_file)
        
        return True
    except TimeoutError:
        print(f"  TIMEOUT: {os.path.basename(notebook_path)} exceeded {EXECUTION_TIMEOUT} seconds")
        return False
    except Exception as e:
        print(f"  ERROR executing {os.path.basename(notebook_path)}: {e}")
        return False


def extract_csv_output(notebook_path):
    """
    Extracts the CSV line from the last output of a notebook.
    
    Returns:
        str: CSV line or None if not found
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
                        text = output['text']
                        # Look for CSV line (contains commas and numbers)
                        lines = text.strip().split('\n')
                        for line in lines:
                            # Check if this looks like a CSV line (has commas and student info)
                            if ',' in line and (line.count(',') >= 2):
                                last_output = line
                    
                    # Handle execution result outputs
                    elif output.get('output_type') == 'execute_result' and 'data' in output:
                        if 'text/plain' in output['data']:
                            text = output['data']['text/plain'].strip()
                            if ',' in text and (text.count(',') >= 2):
                                last_output = text
        
        return last_output
    except Exception as e:
        print(f"  ERROR reading output from {os.path.basename(notebook_path)}: {e}")
        return None


def process_student_notebook(notebook_filename):
    """
    Processes a single student notebook through all three steps.
    
    Returns:
        tuple: (success, csv_line, error_message)
    """
    notebook_path = os.path.join(INPUT_DIR, notebook_filename)
    output_path = os.path.join(OUTPUT_DIR, notebook_filename)
    
    # Step 1: Add autograder cell
    print(f"  Step 1: Adding autograder cell...")
    if not add_autograder_cell(notebook_path):
        return (False, None, "Failed to add autograder cell")
    
    # Step 2: Execute notebook
    print(f"  Step 2: Executing notebook...")
    execution_success = execute_notebook(notebook_path, output_path)
    
    # Step 3: Extract CSV output
    print(f"  Step 3: Extracting results...")
    csv_line = extract_csv_output(output_path)
    
    if not execution_success:
        # If execution failed, create a CSV line with zeros
        # Try to extract student info from the notebook
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            first_name = "Unknown"
            last_name = "Unknown"
            student_id = "Unknown"
            
            # Try to find student info in cells
            for cell in notebook.get('cells', []):
                source = cell.get('source', '')
                if 'first_name' in source:
                    # Try to extract from source code
                    for line in source.split('\n'):
                        if 'first_name' in line and '=' in line:
                            try:
                                first_name = line.split('=')[1].strip().strip('"').strip("'")
                            except:
                                pass
                        if 'last_name' in line and '=' in line:
                            try:
                                last_name = line.split('=')[1].strip().strip('"').strip("'")
                            except:
                                pass
                        if 'student_id' in line and '=' in line:
                            try:
                                student_id = line.split('=')[1].strip().strip('"').strip("'")
                            except:
                                pass
            
            # If names are still unknown, try to extract username from filename
            if first_name == "Unknown" or last_name == "Unknown":
                username = extract_username_from_filename(notebook_filename)
                if username:
                    # Use username as both first and last name, or split if possible
                    first_name = username
                    last_name = username
            
            # Create CSV line with zeros for all problems
            num_problems = 12
            csv_line = (
                f"{first_name},{last_name},{student_id}," +
                ",".join(["0"] * num_problems) +
                ",0.00"
            )
        except:
            # Fallback: try to extract username from filename
            username = extract_username_from_filename(notebook_filename)
            if username:
                csv_line = f"{username},{username},Unknown,{','.join(['0'] * 12)},0.00"
            else:
                csv_line = f"Unknown,Unknown,Unknown,{','.join(['0'] * 12)},0.00"
        
        return (False, csv_line, "Notebook execution failed or crashed")
    
    if csv_line is None:
        # If CSV output is None but execution succeeded, try to extract student info
        # This might happen if autograder code had errors but notebook executed
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            first_name = "Unknown"
            last_name = "Unknown"
            student_id = "Unknown"
            
            # Try to find student info in cells
            for cell in notebook.get('cells', []):
                source = cell.get('source', '')
                if 'first_name' in source:
                    for line in source.split('\n'):
                        if 'first_name' in line and '=' in line:
                            try:
                                first_name = line.split('=')[1].strip().strip('"').strip("'")
                            except:
                                pass
                        if 'last_name' in line and '=' in line:
                            try:
                                last_name = line.split('=')[1].strip().strip('"').strip("'")
                            except:
                                pass
                        if 'student_id' in line and '=' in line:
                            try:
                                student_id = line.split('=')[1].strip().strip('"').strip("'")
                            except:
                                pass
            
            # If names are still unknown, try to extract username from filename
            if first_name == "Unknown" or last_name == "Unknown":
                username = extract_username_from_filename(notebook_filename)
                if username:
                    first_name = username
                    last_name = username
            
            # Create CSV line with zeros (autograder didn't produce output)
            num_problems = 12
            csv_line = (
                f"{first_name},{last_name},{student_id}," +
                ",".join(["0"] * num_problems) +
                ",0.00"
            )
            return (False, csv_line, "Could not extract CSV output from autograder")
        except:
            username = extract_username_from_filename(notebook_filename)
            if username:
                csv_line = f"{username},{username},Unknown,{','.join(['0'] * 12)},0.00"
            else:
                csv_line = f"Unknown,Unknown,Unknown,{','.join(['0'] * 12)},0.00"
            return (False, csv_line, "Could not extract CSV output")
    
    return (True, csv_line, None)


def main():
    """
    Main function to run the autograder on all student notebooks.
    """
    print("=" * 70)
    print("CS3 Autograder - Unified Processing")
    print("=" * 70)
    
    # Check if input directory exists
    if not os.path.isdir(INPUT_DIR):
        print(f"ERROR: Input directory does not exist: {INPUT_DIR}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Input directory: {INPUT_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Grades CSV: {GRADES_CSV}")
    print()
    
    # Find all .ipynb files in the input directory
    notebooks = [f for f in os.listdir(INPUT_DIR) if f.endswith('.ipynb')]
    
    if not notebooks:
        print(f"No .ipynb files found in {INPUT_DIR}")
        sys.exit(1)
    
    print(f"Found {len(notebooks)} notebook(s) to process")
    print()
    
    # Process each notebook
    results = []
    successful = 0
    failed = 0
    
    for i, notebook in enumerate(notebooks, 1):
        print(f"[{i}/{len(notebooks)}] Processing: {notebook}")
        success, csv_line, error = process_student_notebook(notebook)
        
        if success:
            results.append(csv_line)
            successful += 1
            print(f"  ✓ Success")
        else:
            if csv_line:
                results.append(csv_line)
                failed += 1
                print(f"  ✗ Failed: {error} (graded with zeros)")
            else:
                failed += 1
                print(f"  ✗ Failed: {error} (no output generated)")
        
        print()
    
    # Write all results to CSV file
    print("=" * 70)
    print("Writing results to CSV...")
    try:
        with open(GRADES_CSV, 'w', encoding='utf-8') as f:
            # Write header
            f.write("first_name,last_name,student_id,")
            f.write(",".join([f"problem_{i}" for i in range(1, 13)]))
            f.write(",total\n")
            
            # Write results
            for csv_line in results:
                f.write(f"{csv_line}\n")
        
        print(f"✓ Results written to: {GRADES_CSV}")
    except Exception as e:
        print(f"ERROR writing CSV file: {e}")
        sys.exit(1)
    
    # Print summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total notebooks processed: {len(notebooks)}")
    print(f"Successful: {successful}")
    print(f"Failed (graded with zeros): {failed}")
    print(f"Results saved to: {GRADES_CSV}")
    print("=" * 70)


if __name__ == "__main__":
    main()

