"""
Template for creating a robust autograder with error handling.
Copy this structure when creating a new autograder.

Key patterns:
1. Each grade_problem() call wrapped in try-except
2. Each test section wrapped in try-except
3. Main execution has comprehensive error handling
4. Always ensures correct number of problem scores
5. Always outputs valid CSV
"""

#******************************************************************************
#DO NOT MODIFY THE CODE BELOW
#******************************************************************************

POINTS_PER_PROBLEM = 4.0  # Adjust as needed
points_by_problem = []


def grade_problem(problem_num, test_cases, solution_func, max_points):
    """Grades a single problem with test cases."""
    passed_tests = 0
    num_tests = len(test_cases)

    for i in range(num_tests):
        inputs, expected = test_cases[i]
        try:
            output = solution_func(*inputs)
            if output == expected:
                passed_tests += 1
            else:
                print("Problem", problem_num, "- Test", (i+1), "FAILED. Output:", output, "Expected:", expected)
        except Exception as ex:
            print("Problem", problem_num, "- Test", (i+1), "EXCEPTION:", ex)

    score = (passed_tests / num_tests) * max_points
    points_by_problem.append(score)
    print("Problem", problem_num, "Score:", score, "/", max_points)
    return score


# ---------------------------------------------------------------
# TEST SECTION 1 (Problems 1-N)
# ---------------------------------------------------------------

def test_section1():
    """Test section for problems 1 through N."""
    print("=== Section 1 Tests ===")
    
    section_score = 0
    
    # Setup code (create test data, etc.)
    # ...
    
    # -----------------------------
    # Problem 1 — description
    # -----------------------------
    def P1(arg1, arg2):
        return student_function(arg1, arg2)
    
    # WRAP EACH grade_problem CALL IN try-except
    try:
        section_score += grade_problem(1, [
            ((arg1_val, arg2_val), expected_result),  # Test 1
            ((arg1_val2, arg2_val2), expected_result2),  # Test 2
            # ... more test cases
        ], P1, POINTS_PER_PROBLEM)
    except Exception as e:
        print(f"Problem 1 CRASHED: {e}")
        points_by_problem.append(0.0)
        print("Problem 1 Score: 0.0 /", POINTS_PER_PROBLEM)
    
    # -----------------------------
    # Problem 2 — description
    # -----------------------------
    def P2(arg1):
        return student_function2(arg1)
    
    try:
        section_score += grade_problem(2, [
            ((arg1_val,), expected_result),
            # ... more test cases
        ], P2, POINTS_PER_PROBLEM)
    except Exception as e:
        print(f"Problem 2 CRASHED: {e}")
        points_by_problem.append(0.0)
        print("Problem 2 Score: 0.0 /", POINTS_PER_PROBLEM)
    
    # Repeat for all problems in this section...
    
    return section_score


# ---------------------------------------------------------------
# TEST SECTION 2 (Problems N+1 to M)
# ---------------------------------------------------------------

def test_section2():
    """Test section for problems N+1 through M."""
    print("=== Section 2 Tests ===")
    
    section_score = 0
    
    # Setup code...
    
    # Problem N+1, N+2, etc. - all wrapped in try-except
    # ...
    
    return section_score


# ---------------------------------------------------------------
# RUN ALL SECTIONS AND PRINT CSV RESULT
# ---------------------------------------------------------------

try:
    # Safely extract student info with fallbacks
    try:
        student_first = str(first_name)
        student_last = str(last_name)
        student_id_val = str(student_id)
    except:
        student_first = "Unknown"
        student_last = "Unknown"
        student_id_val = "Unknown"
    
    # Run each test section independently (each in try-except)
    try:
        section1_score = test_section1()
    except Exception as e:
        print(f"ERROR in test_section1: {e}")
        section1_score = 0
        # Ensure we have correct number of entries for section 1
        expected_section1_problems = 6  # Adjust based on your exam
        while len(points_by_problem) < expected_section1_problems:
            points_by_problem.append(0.0)
    
    try:
        section2_score = test_section2()
    except Exception as e:
        print(f"ERROR in test_section2: {e}")
        section2_score = 0
        # Ensure we have correct number of entries for section 2
        expected_total_problems = 12  # Adjust based on your exam
        while len(points_by_problem) < expected_total_problems:
            points_by_problem.append(0.0)
    
    # Ensure we have exactly the correct number of problem scores
    total_problems = 12  # Adjust based on your exam
    while len(points_by_problem) < total_problems:
        points_by_problem.append(0.0)
    # Truncate if somehow we have more
    points_by_problem = points_by_problem[:total_problems]
    
    final_score = section1_score + section2_score  # Add all section scores
    
    # CSV format: first_name,last_name,student_id,score1,...,scoreN,total
    csv_line = (
        student_first + "," +
        student_last + "," +
        student_id_val + "," +
        ",".join(str(int(score)) for score in points_by_problem) +
        "," + "{:.2f}".format(final_score)
    )
    
    print(csv_line)
    
except Exception as e:
    # If there's a catastrophic error, output zeros for all problems
    try:
        student_first = str(first_name)
        student_last = str(last_name)
        student_id_val = str(student_id)
    except:
        student_first = "Unknown"
        student_last = "Unknown"
        student_id_val = "Unknown"
    
    total_problems = 12  # Adjust based on your exam
    csv_line = (
        student_first + "," +
        student_last + "," +
        student_id_val + "," +
        ",".join(["0"] * total_problems) +
        ",0.00"
    )
    print(f"ERROR: {e}")
    print(csv_line)

#******************************************************************************
#DO NOT MODIFY THE CODE ABOVE
#******************************************************************************

