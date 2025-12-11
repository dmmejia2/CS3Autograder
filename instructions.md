# Step-by-Step Instructions to Run the CS3 Autograder

## Prerequisites

Before running the autograder, ensure you have:
- Python 3 installed on your system
- Access to the student notebook files
- A virtual environment set up (see Step 1)

---

## Step 1: Set Up Virtual Environment

1. **Navigate to the Scripts directory:**
   ```bash
   cd "/Users/daniel/Desktop/CS3 Exams/Scripts"
   ```

2. **Create a virtual environment (if not already created):**
   ```bash
   python3 -m venv myenv
   ```

3. **Activate the virtual environment:**
   - **On macOS/Linux:**
     ```bash
     source myenv/bin/activate
     ```
   - **On Windows:**
     ```bash
     myenv\Scripts\activate
     ```

4. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   You should see output indicating that `nbformat`, `nbconvert`, and `jupyter` are being installed.

---

## Step 2: Configure Paths

1. **Open `config.py` in a text editor**

2. **Update the following paths to match your system:**
   ```python
   INPUT_DIR = "/path/to/your/student/notebooks"
   OUTPUT_DIR = "/path/to/output/directory"
   GRADES_CSV = "/path/to/output/grades.csv"
   ```

   **Example:**
   ```python
   INPUT_DIR = "/Users/daniel/Desktop/CS3 Exams/Scripts/Input"
   OUTPUT_DIR = "/Users/daniel/Desktop/CS3 Exams/Scripts/Output"
   GRADES_CSV = "/Users/daniel/Desktop/CS3 Exams/Scripts/Output/grades.csv"
   ```

3. **Verify the autograder code** (optional):
   - The autograder code is already configured in `AUTOGRADER_CODE`
   - Only modify this if you need to change the grading logic

4. **Adjust timeout if needed** (optional):
   ```python
   EXECUTION_TIMEOUT = 20  # seconds per notebook
   ```
   Increase this if student notebooks take longer to execute.

---

## Step 3: Prepare Student Notebooks

1. **Place all student notebook files (`.ipynb`) in the Input directory:**
   - The directory path should match `INPUT_DIR` in `config.py`
   - Ensure the notebooks are properly formatted Jupyter notebooks

2. **Verify student notebooks contain:**
   - Student information (first_name, last_name, student_id)
   - Student code implementations
   - Proper notebook structure

---

## Step 4: Run the Autograder

1. **Ensure the virtual environment is activated:**
   - You should see `(myenv)` at the beginning of your terminal prompt
   - If not, run: `source myenv/bin/activate` (macOS/Linux) or `myenv\Scripts\activate` (Windows)

2. **Run the autograder:**
   ```bash
   python run_autograder.py
   ```

3. **Monitor the output:**
   - The script will process each notebook one by one
   - You'll see progress for each student: `[1/97] Processing: filename.ipynb`
   - For each notebook, you'll see:
     - Step 1: Adding autograder cell
     - Step 2: Executing notebook
     - Step 3: Extracting results
     - Success (✓) or Failure (✗) status

---

## Step 5: Review Results

1. **Check the output CSV file:**
   - Location: Path specified in `GRADES_CSV` in `config.py`
   - Format: `first_name,last_name,student_id,problem_1,problem_2,...,problem_12,total`

2. **Review the summary at the end:**
   - Total notebooks processed
   - Number of successful executions
   - Number of failed executions (graded with zeros)

3. **Check executed notebooks (optional):**
   - Executed notebooks are saved in the `OUTPUT_DIR`
   - You can open these to see the autograder output for each student

---

## Error Handling

The autograder is designed to handle errors gracefully:

### If a student's notebook crashes:
- The autograder continues processing other notebooks
- The crashed notebook receives 0 points for all problems
- An error message is printed to the console
- The student still appears in the CSV output with zeros

### If a specific problem function fails:
- The autograder continues grading other problems
- The failed problem receives 0 points
- Other problems are graded normally
- Example: If Problem 3 crashes, Problems 1, 2, 4-12 will still be graded

### Common Issues:

1. **"No .ipynb files found":**
   - Check that `INPUT_DIR` path is correct
   - Verify student notebooks are in the Input directory

2. **"TimeoutError":**
   - Increase `EXECUTION_TIMEOUT` in `config.py`
   - Check if student notebooks have infinite loops

3. **"Module not found":**
   - Ensure virtual environment is activated
   - Run: `pip install -r requirements.txt`

4. **"Permission denied":**
   - Check file permissions for Input and Output directories
   - Ensure you have read/write access

---

## Example Workflow

```bash
# 1. Navigate to directory
cd "/Users/daniel/Desktop/CS3 Exams/Scripts"

# 2. Activate virtual environment
source myenv/bin/activate

# 3. Verify configuration (optional)
cat config.py | grep INPUT_DIR

# 4. Run autograder
python run_autograder.py

# 5. View results
cat Output/grades.csv
```

---

## Tips

- **Test with a single notebook first:** Before running on all students, test with one notebook to verify everything works
- **Backup student files:** The autograder modifies notebooks (adds autograder cell), so keep backups if needed
- **Check logs:** Review the console output for any warnings or errors
- **Verify CSV format:** Open the CSV file in Excel or a text editor to verify the format is correct

---

## Troubleshooting

If you encounter issues:

1. **Verify virtual environment:**
   ```bash
   which python  # Should point to myenv/bin/python
   ```

2. **Reinstall dependencies:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Check Python version:**
   ```bash
   python --version  # Should be Python 3.x
   ```

4. **Test notebook execution manually:**
   ```bash
   jupyter nbconvert --to notebook --execute test_notebook.ipynb
   ```

---

## Next Steps

After running the autograder:
1. Review the CSV file for accuracy
2. Check any failed notebooks manually if needed
3. Import grades into your grading system
4. Provide feedback to students based on the results

