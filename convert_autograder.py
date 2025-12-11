#!/usr/bin/env python3
"""
Helper script to convert autograder code to robust format with error handling.
This script can help identify where to add try-except blocks.
"""

import re
import sys


def analyze_autograder_code(code):
    """
    Analyzes autograder code and suggests where to add error handling.
    
    Args:
        code: String containing the autograder code
        
    Returns:
        dict: Analysis results with suggestions
    """
    analysis = {
        'grade_problem_calls': [],
        'test_functions': [],
        'main_execution': None,
        'suggestions': []
    }
    
    # Find all grade_problem calls
    grade_pattern = r'grade_problem\s*\(\s*(\d+)\s*,'
    matches = re.finditer(grade_pattern, code)
    for match in matches:
        problem_num = match.group(1)
        # Find the line number (approximate)
        line_num = code[:match.start()].count('\n') + 1
        analysis['grade_problem_calls'].append({
            'problem_num': problem_num,
            'line': line_num,
            'needs_wrapping': 'try:' not in code[max(0, match.start()-200):match.start()]
        })
    
    # Find test section functions
    test_pattern = r'def\s+(test_\w+)\s*\('
    matches = re.finditer(test_pattern, code)
    for match in matches:
        func_name = match.group(1)
        line_num = code[:match.start()].count('\n') + 1
        analysis['test_functions'].append({
            'name': func_name,
            'line': line_num
        })
    
    # Find main execution block (usually after "# RUN" comment)
    main_pattern = r'#\s*RUN.*?\n(.*?)(?:#\*\*|$)'
    match = re.search(main_pattern, code, re.DOTALL | re.IGNORECASE)
    if match:
        analysis['main_execution'] = {
            'found': True,
            'has_try': 'try:' in match.group(1)
        }
    
    # Generate suggestions
    unwrapped_problems = [p for p in analysis['grade_problem_calls'] if p['needs_wrapping']]
    if unwrapped_problems:
        analysis['suggestions'].append(
            f"Found {len(unwrapped_problems)} grade_problem() calls that need try-except wrapping"
        )
    
    return analysis


def generate_wrapped_grade_problem(problem_num, test_cases_code, func_name, points_var="POINTS_PER_PROBLEM"):
    """
    Generates a wrapped grade_problem call with error handling.
    
    Args:
        problem_num: Problem number (int or str)
        test_cases_code: String containing the test cases list
        func_name: Name of the function to test (e.g., "P1")
        points_var: Variable name for points per problem
        
    Returns:
        str: Wrapped code
    """
    return f'''    try:
        section_score += grade_problem({problem_num}, [
{test_cases_code}
    ], {func_name}, {points_var})
    except Exception as e:
        print(f"Problem {problem_num} CRASHED: {{e}}")
        points_by_problem.append(0.0)
        print("Problem {problem_num} Score: 0.0 /", {points_var})'''


def generate_wrapped_test_section(section_name, section_code, expected_problems):
    """
    Generates a wrapped test section function call.
    
    Args:
        section_name: Name of the test function (e.g., "test_graphAL")
        section_code: The actual test section code
        expected_problems: Number of problems in this section
        
    Returns:
        str: Wrapped code
    """
    return f'''    try:
        {section_name}_score = {section_name}()
    except Exception as e:
        print(f"ERROR in {section_name}: {{e}}")
        {section_name}_score = 0
        # Ensure we have {expected_problems} entries for this section
        while len(points_by_problem) < {expected_problems}:
            points_by_problem.append(0.0)'''


def print_analysis_report(analysis):
    """Prints a formatted analysis report."""
    print("=" * 70)
    print("AUTOGRADER CODE ANALYSIS")
    print("=" * 70)
    print()
    
    print(f"Found {len(analysis['grade_problem_calls'])} grade_problem() calls")
    unwrapped = [p for p in analysis['grade_problem_calls'] if p['needs_wrapping']]
    if unwrapped:
        print(f"  ⚠️  {len(unwrapped)} need try-except wrapping:")
        for p in unwrapped:
            print(f"     - Problem {p['problem_num']} at line {p['line']}")
    else:
        print("  ✅ All grade_problem() calls are wrapped")
    print()
    
    print(f"Found {len(analysis['test_functions'])} test section functions:")
    for func in analysis['test_functions']:
        print(f"  - {func['name']} at line {func['line']}")
    print()
    
    if analysis['main_execution']:
        if analysis['main_execution']['has_try']:
            print("  ✅ Main execution block has error handling")
        else:
            print("  ⚠️  Main execution block needs error handling")
    else:
        print("  ⚠️  Could not find main execution block")
    print()
    
    if analysis['suggestions']:
        print("SUGGESTIONS:")
        for suggestion in analysis['suggestions']:
            print(f"  - {suggestion}")
    print("=" * 70)


def main():
    """Main function to analyze autograder code."""
    if len(sys.argv) < 2:
        print("Usage: python convert_autograder.py <autograder_code_file>")
        print("   or: python convert_autograder.py --help")
        sys.exit(1)
    
    if sys.argv[1] == '--help':
        print(__doc__)
        print("\nThis script analyzes autograder code and suggests where to add error handling.")
        print("\nIt does NOT automatically convert the code, but provides guidance.")
        print("Use the prompt in AUTOGRADER_CONVERSION_PROMPT.md for actual conversion.")
        sys.exit(0)
    
    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        
        analysis = analyze_autograder_code(code)
        print_analysis_report(analysis)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error analyzing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

