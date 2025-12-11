# Additional Considerations for CS3 Autograder

## Error Handling Improvements

The autograder now has robust error handling:

1. **Individual Problem Failures**: Each problem (1-12) is wrapped in try-except blocks. If one problem crashes due to:
   - Missing function implementation
   - Syntax errors in student code
   - Attribute errors (e.g., method doesn't exist)
   - Any other exception
   
   The autograder will:
   - Assign 0 points to that problem
   - Continue grading all other problems
   - Print an error message indicating which problem failed

2. **Section Failures**: If an entire section (GraphAL or GraphAM) fails, the other section will still be graded.

3. **Notebook Execution Failures**: If a notebook fails to execute entirely, it will:
   - Extract student information from the notebook or filename
   - Assign 0 points to all problems
   - Continue processing other notebooks

## Username Extraction

The autograder now extracts usernames from filenames when student names are unknown. It looks for patterns like:
- `Exam Three - Part I_username_attempt_...`
- Extracts the username between `Part I_` and `_attempt`

If names are still unknown after extraction, it uses "Unknown" as fallback.

## Things to Consider

### 1. **Backup Student Files**
- The autograder modifies notebooks by adding an autograder cell
- Consider backing up original student submissions before running
- The autograder creates `.bak` files, but these are excluded from git

### 2. **Execution Time**
- Each notebook has a timeout (default: 20 seconds)
- If students have infinite loops or very slow code, increase `EXECUTION_TIMEOUT` in `config.py`
- Consider running on a subset first to estimate total time

### 3. **CSV Output Format**
- The CSV file has a header row: `first_name,last_name,student_id,problem_1,...,problem_12,total`
- Scores are integers (points per problem)
- Total is a float with 2 decimal places
- Verify the CSV format before importing into grading systems

### 4. **Partial Credit**
- The autograder gives partial credit based on test cases passed
- Each problem has multiple test cases
- Score = (passed_tests / total_tests) * max_points

### 5. **Student Information**
- The autograder expects student info in a specific format in the notebook
- If students didn't fill in their information correctly, the autograder will:
  - Try to extract from notebook cells
  - Fall back to username from filename
  - Use "Unknown" as last resort

### 6. **Virtual Environment**
- Always activate the virtual environment before running
- If you get import errors, verify the virtual environment is activated
- Dependencies are listed in `requirements.txt`

### 7. **Output Files**
- Executed notebooks are saved in `OUTPUT_DIR`
- These can be large if you have many students
- Consider cleaning up old output files periodically
- Output directory is excluded from git

### 8. **Testing**
- Test with a single notebook first to verify configuration
- Check that paths in `config.py` are correct
- Verify autograder code matches your exam requirements

### 9. **Grading Workflow**
1. Place all student notebooks in `Input/` directory
2. Run `python run_autograder.py`
3. Review the CSV output file
4. Check any failed notebooks manually if needed
5. Import CSV into your grading system

### 10. **Error Messages**
- The autograder prints detailed error messages to the console
- Review these to identify common issues:
  - Syntax errors in student code
  - Missing function implementations
  - Import errors
  - Timeout issues

### 11. **File Naming**
- The autograder processes all `.ipynb` files in the Input directory
- Filenames should follow a consistent pattern for username extraction
- Avoid special characters in filenames that might cause issues

### 12. **Resource Usage**
- Running on many notebooks can be resource-intensive
- Monitor system resources (CPU, memory) during execution
- Consider running in batches if you have hundreds of students

### 13. **Version Control**
- The `Input/` and `Output/` directories are excluded from git
- Only the autograder code and configuration are committed
- Keep student data private and secure

### 14. **Autograder Code Updates**
- If you need to modify the autograder logic, edit `AUTOGRADER_CODE` in `config.py`
- Test changes with a sample notebook before running on all students
- The autograder code is injected into each student's notebook

### 15. **Post-Processing**
- After running, you may want to:
  - Sort CSV by student name or ID
  - Calculate statistics (average, median, etc.)
  - Generate reports
  - Identify students who need manual review

## Best Practices

1. **Always test first**: Run on 1-2 notebooks before processing all students
2. **Keep backups**: Backup original student submissions
3. **Review failures**: Manually check notebooks that failed completely
4. **Verify scores**: Spot-check some results to ensure accuracy
5. **Document changes**: Note any modifications to autograder code
6. **Secure data**: Keep student information and grades secure
7. **Version control**: Commit changes to autograder code regularly

## Troubleshooting

See `instructions.md` for detailed troubleshooting steps.

## Support

If you encounter issues:
1. Check the console output for error messages
2. Review the executed notebooks in the Output directory
3. Verify configuration in `config.py`
4. Test with a single notebook to isolate issues

