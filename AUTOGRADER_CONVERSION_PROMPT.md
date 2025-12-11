# Prompt for Converting Autograder Code to Robust Format

Copy and paste this prompt when you need to convert a new autograder to the robust error-handling format:

---

## Prompt:

I have autograder code that I need to convert to a robust format where each problem is isolated with error handling. Here is my autograder code:

```
[PASTE YOUR AUTOGRADER CODE HERE]
```

Please convert this code to match the following requirements:

1. **Wrap each `grade_problem()` call in a try-except block** that:
   - Catches any exception
   - Prints an error message: `"Problem X CRASHED: {error}"`
   - Appends 0.0 to `points_by_problem` list
   - Prints: `"Problem X Score: 0.0 / {POINTS_PER_PROBLEM}"`
   - Continues to the next problem

2. **Wrap each test section function** (like `test_graphAL()`, `test_graphAM()`, etc.) in a try-except block that:
   - Catches any exception
   - Prints an error message
   - Returns 0 for the section score
   - Ensures the `points_by_problem` list has the correct number of entries

3. **In the main execution block**, wrap the entire execution in a try-except that:
   - Safely extracts student info (first_name, last_name, student_id) with fallback to "Unknown"
   - Runs each test section independently (each in its own try-except)
   - Ensures `points_by_problem` has exactly the correct number of entries (pad with 0.0 if needed, truncate if too many)
   - Always outputs a valid CSV line even if everything fails

4. **Maintain the exact same structure and logic** - only add error handling, don't change the grading logic.

5. **Format the output** to match this pattern:
   ```python
   try:
       section_score += grade_problem(1, [
           # test cases
       ], P1, POINTS_PER_PROBLEM)
   except Exception as e:
       print(f"Problem 1 CRASHED: {e}")
       points_by_problem.append(0.0)
       print("Problem 1 Score: 0.0 /", POINTS_PER_PROBLEM)
   ```

6. **For the main execution block**, use this pattern:
   ```python
   try:
       # Safely get student info
       try:
           student_first = str(first_name)
           student_last = str(last_name)
           student_id_val = str(student_id)
       except:
           student_first = "Unknown"
           student_last = "Unknown"
           student_id_val = "Unknown"
       
       # Run each section independently
       try:
           section1_score = test_section1()
       except Exception as e:
           print(f"ERROR in test_section1: {e}")
           section1_score = 0
           # Ensure correct number of entries
           while len(points_by_problem) < expected_count:
               points_by_problem.append(0.0)
       
       # Repeat for each section...
       
       # Ensure exact number of problem scores
       while len(points_by_problem) < total_problems:
           points_by_problem.append(0.0)
       points_by_problem = points_by_problem[:total_problems]
       
       # Generate CSV output
       final_score = section1_score + section2_score + ...
       csv_line = (
           student_first + "," +
           student_last + "," +
           student_id_val + "," +
           ",".join(str(int(score)) for score in points_by_problem) +
           "," + "{:.2f}".format(final_score)
       )
       print(csv_line)
   except Exception as e:
       # Fallback: output zeros
       # ... (similar structure)
   ```

Please convert my code following these exact patterns. The converted code should handle any errors gracefully and continue grading other problems even if one fails.

---

## Usage Instructions:

1. Copy the prompt above
2. Replace `[PASTE YOUR AUTOGRADER CODE HERE]` with your actual autograder code
3. Paste into your AI assistant (ChatGPT, Claude, etc.)
4. Review the converted code
5. Test with a sample notebook to verify it works

## Key Points to Verify:

- ✅ Each `grade_problem()` call is wrapped in try-except
- ✅ Each test section function call is wrapped in try-except
- ✅ Main execution block has comprehensive error handling
- ✅ `points_by_problem` list is always the correct length
- ✅ CSV output is always generated, even on failure
- ✅ Student info extraction has fallbacks
- ✅ Error messages are clear and informative

