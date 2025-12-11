# CS3 Autograder

A unified autograder system for CS3 exams that processes student Jupyter notebooks, executes them, and extracts grading results.

## Features

- **Unified workflow**: Single script handles all three steps (add autograder, execute, read results)
- **Error handling**: Continues grading even if a student's code crashes, assigning 0 points to failed problems
- **Centralized configuration**: All paths and autograder code in one config file
- **Virtual environment support**: Uses virtual environment for isolated dependencies

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Paths

Edit `config.py` to set your paths:

```python
INPUT_DIR = "/path/to/student/notebooks"
OUTPUT_DIR = "/path/to/output/notebooks"
GRADES_CSV = "/path/to/output/grades.csv"
VIRTUAL_ENV_PATH = "/path/to/virtual/env"
```

### 4. Configure Autograder Code

Edit the `AUTOGRADER_CODE` variable in `config.py` to customize the autograder logic.

## Usage

### Run the Autograder

```bash
# Make sure virtual environment is activated
source myenv/bin/activate

# Run the autograder
python run_autograder.py
```

The script will:
1. Add the autograder cell to each student's notebook
2. Execute each notebook
3. Extract the CSV results
4. Write all grades to a CSV file

### Error Handling

If a student's notebook crashes or fails to execute:
- The script continues processing other notebooks
- The failed notebook receives 0 points for all problems
- An error message is printed to the console
- The student's information is still included in the CSV output

## File Structure

```
.
├── config.py              # Configuration file (paths and autograder code)
├── run_autograder.py      # Main autograder script
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore rules
├── Input/                # Student notebooks (not committed to git)
├── Output/               # Executed notebooks and results (not committed)
└── myenv/               # Virtual environment (not committed)
```

## Configuration

### Paths

All file paths are configured in `config.py`:

- `INPUT_DIR`: Directory containing student notebooks
- `OUTPUT_DIR`: Directory for executed notebooks
- `GRADES_CSV`: Path to output CSV file with grades
- `EXECUTION_TIMEOUT`: Timeout in seconds for notebook execution (default: 20)

### Autograder Code

The autograder code is stored in the `AUTOGRADER_CODE` variable in `config.py`. This code is injected into each student's notebook before execution.

## Output Format

The CSV output file contains one row per student with the following format:

```
first_name,last_name,student_id,problem_1,problem_2,...,problem_12,total
```

If a student's notebook crashes, all problem scores will be 0, but the student will still appear in the CSV.

## Notes

- The `Input/` folder is excluded from git (contains student code)
- The `Output/` folder is excluded from git (generated files)
- The virtual environment is excluded from git
- Backup files (`.bak`) are automatically created but excluded from git

## Troubleshooting

### Notebook execution timeout

If notebooks are timing out, increase `EXECUTION_TIMEOUT` in `config.py`.

### Missing dependencies

Make sure the virtual environment is activated and all dependencies are installed:

```bash
source myenv/bin/activate
pip install -r requirements.txt
```

### Permission errors

Ensure you have read/write permissions for the input and output directories.

