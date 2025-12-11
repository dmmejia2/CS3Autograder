"""
Configuration file for the CS3 Autograder
Edit the paths and autograder code here
"""

# ============================================================================
# FILE PATHS
# ============================================================================
INPUT_DIR = "/Users/daniel/Desktop/CS3 Exams/Scripts/Input"
OUTPUT_DIR = "/Users/daniel/Desktop/CS3 Exams/Scripts/Output"
GRADES_CSV = "/Users/daniel/Desktop/CS3 Exams/Scripts/Output/grades.csv"

# ============================================================================
# EXECUTION SETTINGS
# ============================================================================
EXECUTION_TIMEOUT = 20  # seconds per notebook
VIRTUAL_ENV_PATH = "/Users/daniel/Desktop/CS3 Exams/Scripts/myenv"

# ============================================================================
# AUTOGRADER CODE
# This code will be injected into each student's notebook
# ============================================================================
AUTOGRADER_CODE = '''

#******************************************************************************
#DO NOT MODIFY THE CODE BELOW
#******************************************************************************

POINTS_PER_PROBLEM = 4.0
points_by_problem = []


def grade_problem(problem_num, test_cases, solution_func, max_points):
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
# Graph Builders (NO SELF-LOOPS)
# ---------------------------------------------------------------

def build_graphAL_unweighted():
    g = GraphAL(vertices=12, directed=True)
    edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 4),
        (2, 5),
        (3, 6),
        (4, 7),
        (5, 8),
        (6, 9),
        (7, 10),
        (8, 10),
        (9, 10)
    ]
    for u, v in edges:
        g.insert_edge(u, v)
    return g


def build_graphAL_weighted():
    g = GraphAL(vertices=6, directed=True, weighted=True)
    g.insert_edge(0, 1, 2)
    g.insert_edge(1, 2, 4)
    g.insert_edge(2, 3, 6)
    g.insert_edge(3, 4, 8)
    g.insert_edge(4, 5, 10)
    return g


# ---------------------------------------------------------------
# ADJACENCY LIST GRADING (Problems 1–6)
# ---------------------------------------------------------------

def test_graphAL():
    print("=== Adjacency List Tests ===")

    section_score = 0
    unweighted = build_graphAL_unweighted()
    weighted = build_graphAL_weighted()

    # -----------------------------
    # Problem 1 — is_there_an_edge
    # -----------------------------
    def P1(graph, u, v):
        return graph.is_there_an_edge(u, v)

    try:
        section_score += grade_problem(1, [
        ((unweighted, 0, 1), True),   # Test 1: Edge 0->1 exists
        ((unweighted, 0, 3), True),   # Test 2: Edge 0->3 exists
        ((unweighted, 2, 5), True),   # Test 3: Edge 2->5 exists
        ((unweighted, 9, 10), True),  # Test 4: Edge 9->10 exists
        ((unweighted, 10, 9), False), # Test 5: Reverse edge does NOT exist
        ((unweighted, 0, 11), False), # Test 6: 11 is isolated, no edge
        ((weighted, 0, 1), True),     # Test 7: Weighted edge 0->1 exists
        ((weighted, 1, 2), True),     # Test 8: Weighted edge 1->2 exists
        ((weighted, 2, 5), False),    # Test 9: No edge 2->5
        ((GraphAL(4, True), 1, 2), False) # Test 10: Empty graph → no edges
    ], P1, POINTS_PER_PROBLEM)
    except Exception as e:
        print(f"Problem 1 CRASHED: {e}")
        points_by_problem.append(0.0)
        print("Problem 1 Score: 0.0 /", POINTS_PER_PROBLEM)

    # -----------------------------
    # Problem 2 — compute_in_degree
    # -----------------------------
    def P2(graph, v):
        return graph.compute_in_degree(v)

    try:
        section_score += grade_problem(2, [
        ((unweighted, 0), 0),   # Test 1: No incoming edges
        ((unweighted, 1), 1),   # Test 2: One incoming edge (0->1)
        ((unweighted, 4), 1),   # Test 3: One incoming (1->4)
        ((unweighted, 10), 3),  # Test 4: Incoming from 7,8,9
        ((unweighted, 5), 1),   # Test 5: Incoming from 2
        ((unweighted, 8), 1),   # Test 6: Incoming from 5
        ((weighted, 0), 0),     # Test 7: No incoming
        ((weighted, 3), 1),     # Test 8: Incoming from 2
        ((weighted, 5), 1),     # Test 9: Incoming from 4
        ((GraphAL(5, True), 3), 0) # Test 10: Empty graph → in-degree 0
    ], P2, POINTS_PER_PROBLEM)
    except Exception as e:
        print(f"Problem 2 CRASHED: {e}")
        points_by_problem.append(0.0)
        print("Problem 2 Score: 0.0 /", POINTS_PER_PROBLEM)

    # -----------------------------
    # Problem 3 — is_isolated
    # -----------------------------
    def P3(graph, v):
        return graph.is_isolated(v)

    iso_AL = GraphAL(6, directed=True)
    iso_AL.insert_edge(0, 1)
    iso_AL.insert_edge(2, 3)

    weighted_iso = GraphAL(6, directed=True, weighted=True)
    weighted_iso.insert_edge(0, 1, 2)
    weighted_iso.insert_edge(2, 4, 4)

    empty = GraphAL(5, directed=True)

    try:
        section_score += grade_problem(3, [
        ((iso_AL, 4), True),   # Test 1: No in/out edges
        ((iso_AL, 5), True),   # Test 2: Fully isolated
        ((iso_AL, 0), False),  # Test 3: Outgoing edge exists
        ((iso_AL, 1), False),  # Test 4: Incoming edge exists
        ((empty, 3), True),    # Test 5: Empty graph → all isolated
        ((weighted_iso, 3), True), # Test 6: Isolated in weighted graph
        ((weighted_iso, 4), False), # Test 7: Incoming edge exists
        ((weighted_iso, 2), False), # Test 8: Outgoing edge exists
        ((GraphAL(1, True), 0), True), # Test 9: Single vertex isolated
        ((GraphAL(3, True), 2), True)  # Test 10: Vertex isolated
    ], P3, POINTS_PER_PROBLEM)
    except Exception as e:
        print(f"Problem 3 CRASHED: {e}")
        points_by_problem.append(0.0)
        print("Problem 3 Score: 0.0 /", POINTS_PER_PROBLEM)

    # -----------------------------
    # Problem 4 — highest_out_degree_vertex
    # -----------------------------
    def P4(graph):
        return graph.highest_out_degree_vertex()

    cg = GraphAL(6, directed=True)
    cg.insert_edge(5, 1)

    try:
        section_score += grade_problem(4, [
        ((unweighted,), 0),   # Test 1
        ((weighted,), 0),     # Test 2
        ((cg,), 5),           # Test 3
        ((GraphAL(3, True),), 0), # Test 4
        ((GraphAL(1, True),), 0), # Test 5
        ((GraphAL(0, True),), -1),# Test 6
        ((build_graphAL_unweighted(),), 0), # Test 7
        ((build_graphAL_weighted(),), 0),   # Test 8
        ((GraphAL(4, True),), 0), # Test 9
        ((GraphAL(2, True),), 0)  # Test 10
    ], P4, POINTS_PER_PROBLEM)
    except Exception as e:
        print(f"Problem 4 CRASHED: {e}")
        points_by_problem.append(0.0)
        print("Problem 4 Score: 0.0 /", POINTS_PER_PROBLEM)

    # -----------------------------
    # Problem 5 — sorted_edge_values
    # -----------------------------
    def P5(graph):
        return graph.sorted_edge_values()

    emptyW = GraphAL(5, directed=True, weighted=True)

    try:
        section_score += grade_problem(5, [
        ((unweighted,), [1]*12),             # Test 1
        ((weighted,), [2,4,6,8,10]),         # Test 2
        ((emptyW,), []),                     # Test 3
        ((GraphAL(0, True),), []),           # Test 4
        ((GraphAL(1, True),), []),           # Test 5
        ((GraphAL(2, True, True),), []),     # Test 6
        ((build_graphAL_weighted(),), [2,4,6,8,10]), # Test 7
        ((build_graphAL_unweighted(),), [1]*12),     # Test 8
        ((cg,), [1]),                        # Test 9
        ((GraphAL(3, True),), [])            # Test 10
    ], P5, POINTS_PER_PROBLEM)
    except Exception as e:
        print(f"Problem 5 CRASHED: {e}")
        points_by_problem.append(0.0)
        print("Problem 5 Score: 0.0 /", POINTS_PER_PROBLEM)

    # -----------------------------
    # Problem 6 — get_adjacent_neighbors
    # -----------------------------
    def P6(graph, v):
        return graph.get_adjacent_neighbors(v)  # outgoing neighbors only

    # Build custom graphs for isolated and multi-neighbor tests
    gA = GraphAL(6, directed=True)
    gA.insert_edge(1, 0)
    gA.insert_edge(1, 2)
    gA.insert_edge(1, 4)

    gB = GraphAL(5, directed=True)
    gB.insert_edge(0, 3)
    gB.insert_edge(0, 2)

    gC = GraphAL(4, directed=False)
    gC.insert_edge(2, 1)
    gC.insert_edge(2, 3)

    gD = GraphAL(6, directed=True)
    # 5 isolated

    gE = GraphAL(6, directed=True)
    gE.insert_edge(3, 5)
    gE.insert_edge(3, 1)
    gE.insert_edge(3, 4)

    try:
        section_score += grade_problem(6, [
        ((gA, 1), [0,2,4]),         # Test 1: Multi outgoing neighbors
        ((gA, 0), []),              # Test 2: No outgoing edges
        ((gB, 0), [2,3]),           # Test 3: Two neighbors
        ((gB, 3), []),              # Test 4: No outgoing edges for 3
        ((gC, 2), [1,3]),           # Test 5: Undirected behaves normally
        ((gC, 1), [2]),             # Test 6: One neighbor
        ((gD, 5), []),              # Test 7: Isolated vertex
        ((gE, 3), [1,4,5]),         # Test 8: Three outgoing edges
        ((unweighted, 0), [1,2,3]), # Test 9: Main exam graph node 0
        ((unweighted, 10), [])      # Test 10: Node 10 has no outgoing edges
    ], P6, POINTS_PER_PROBLEM)
    except Exception as e:
        print(f"Problem 6 CRASHED: {e}")
        points_by_problem.append(0.0)
        print("Problem 6 Score: 0.0 /", POINTS_PER_PROBLEM)

    return section_score

# ---------------------------------------------------------------
# ADJACENCY MATRIX GRADING (Problems 7–12)
# ---------------------------------------------------------------

def build_graphAM_unweighted():
    g = GraphAM(vertices=12, directed=True)
    edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 4),
        (2, 5),
        (3, 6),
        (4, 7),
        (5, 8),
        (6, 9),
        (7, 10),
        (8, 10),
        (9, 10)
    ]
    for u, v in edges:
        g.insert_edge(u, v)
    return g


def build_graphAM_weighted():
    g = GraphAM(vertices=6, directed=True, weighted=True)
    g.insert_edge(0, 1, 2)
    g.insert_edge(1, 2, 4)
    g.insert_edge(2, 3, 6)
    g.insert_edge(3, 4, 8)
    g.insert_edge(4, 5, 10)
    return g


def test_graphAM():
    print("=== Adjacency Matrix Tests ===")

    section_score = 0
    unweighted = build_graphAM_unweighted()
    weighted = build_graphAM_weighted()

    # -----------------------------
    # Problem 7 — is_there_an_edge
    # -----------------------------
    def P7(graph, u, v):
        return graph.is_there_an_edge(u, v)

    try:
        section_score += grade_problem(7, [
        ((unweighted, 0, 1), True),    # Test 1: Edge 0->1 exists
        ((unweighted, 0, 3), True),    # Test 2: Edge 0->3 exists
        ((unweighted, 2, 5), True),    # Test 3: Edge 2->5 exists
        ((unweighted, 9, 10), True),   # Test 4: Edge 9->10 exists
        ((unweighted, 10, 9), False),  # Test 5: No reverse edge
        ((unweighted, 0, 11), False),  # Test 6: No edge to isolated vertex 11
        ((weighted, 0, 1), True),      # Test 7: Weighted edge 0->1 exists
        ((weighted, 1, 2), True),       # Test 8: Weighted edge 1->2 exists
        ((weighted, 2, 5), False),     # Test 9: No edge 2->5
        ((GraphAM(4, True), 1, 2), False) # Test 10: Empty 4-vertex graph
    ], P7, POINTS_PER_PROBLEM)
    except Exception as e:
        print(f"Problem 7 CRASHED: {e}")
        points_by_problem.append(0.0)
        print("Problem 7 Score: 0.0 /", POINTS_PER_PROBLEM)

    # -----------------------------
    # Problem 8 — compute_in_degree
    # -----------------------------
    def P8(graph, v):
        return graph.compute_in_degree(v)

    try:
        section_score += grade_problem(8, [
        ((unweighted, 0), 0),  # Test 1: No incoming edges
        ((unweighted, 1), 1),  # Test 2: Incoming from 0
        ((unweighted, 4), 1),  # Test 3: Incoming from 1
        ((unweighted, 10), 3), # Test 4: Incoming from 7,8,9
        ((unweighted, 5), 1),  # Test 5: Incoming from 2
        ((unweighted, 8), 1),  # Test 6: Incoming from 5

        ((weighted, 0), 0),    # Test 7: No incoming
        ((weighted, 3), 1),    # Test 8: Incoming from 2
        ((weighted, 5), 1),    # Test 9: Incoming from 4
        ((GraphAM(5, True), 3), 0) # Test 10: Empty matrix graph
    ], P8, POINTS_PER_PROBLEM)
    except Exception as e:
        print(f"Problem 8 CRASHED: {e}")
        points_by_problem.append(0.0)
        print("Problem 8 Score: 0.0 /", POINTS_PER_PROBLEM)

    # -----------------------------
    # Problem 9 — is_isolated
    # -----------------------------
    def P9(graph, v):
        return graph.is_isolated(v)

    iso = GraphAM(6, directed=True)
    iso.insert_edge(0, 1)
    iso.insert_edge(2, 3)

    wiso = GraphAM(6, directed=True, weighted=True)
    wiso.insert_edge(0, 1, 3)
    wiso.insert_edge(2, 4, 5)

    empty = GraphAM(5, directed=True)

    try:
        section_score += grade_problem(9, [
        ((iso, 4), True),     # Test 1: No in/out edges
        ((iso, 5), True),     # Test 2: Fully isolated
        ((iso, 0), False),    # Test 3: Outgoing edge exists
        ((iso, 1), False),    # Test 4: Incoming edge exists
        ((empty, 3), True),   # Test 5: Empty → all isolated

        ((wiso, 3), True),    # Test 6: Isolated in weighted graph
        ((wiso, 4), False),   # Test 7: Has incoming
        ((wiso, 2), False),   # Test 8: Has outgoing
        ((GraphAM(1, True), 0), True), # Test 9: Single isolated vertex
        ((GraphAM(3, True), 2), True)  # Test 10: Isolated in empty graph
    ], P9, POINTS_PER_PROBLEM)
    except Exception as e:
        print(f"Problem 9 CRASHED: {e}")
        points_by_problem.append(0.0)
        print("Problem 9 Score: 0.0 /", POINTS_PER_PROBLEM)

    # -----------------------------
    # Problem 10 — highest_out_degree_vertex
    # -----------------------------
    def P10(graph):
        return graph.highest_out_degree_vertex()

    cg = GraphAM(6, directed=True)
    cg.insert_edge(5, 1)

    try:
        section_score += grade_problem(10, [
        ((unweighted,), 0),  # Test 1: Node 0 highest
        ((weighted,), 0),    # Test 2: Node 0 highest
        ((cg,), 5),          # Test 3: Only node 5 has outgoing edges
        ((GraphAM(3, True),), 0), # Test 4: No edges → 0
        ((GraphAM(1, True),), 0), # Test 5: One vertex → 0
        ((GraphAM(0, True),), -1),# Test 6: Empty graph → -1
        ((build_graphAM_unweighted(),), 0), # Test 7
        ((build_graphAM_weighted(),), 0),   # Test 8
        ((GraphAM(4, True),), 0), # Test 9
        ((GraphAM(2, True),), 0)  # Test 10
    ], P10, POINTS_PER_PROBLEM)
    except Exception as e:
        print(f"Problem 10 CRASHED: {e}")
        points_by_problem.append(0.0)
        print("Problem 10 Score: 0.0 /", POINTS_PER_PROBLEM)

    # -----------------------------
    # Problem 11 — sorted_edge_values
    # -----------------------------
    def P11(graph):
        return graph.sorted_edge_values()

    emptyW = GraphAM(5, directed=True, weighted=True)

    try:
        section_score += grade_problem(11, [
        ((unweighted,), [1]*12),       # Test 1: 12 edges all weight 1
        ((weighted,), [2,4,6,8,10]),   # Test 2: Sorted weighted edges
        ((emptyW,), []),               # Test 3: No edges
        ((GraphAM(0, True),), []),     # Test 4: Empty graph
        ((GraphAM(1, True),), []),     # Test 5: No edges
        ((GraphAM(2, True, True),), []), # Test 6
        ((build_graphAM_weighted(),), [2,4,6,8,10]), # Test 7
        ((build_graphAM_unweighted(),), [1]*12),     # Test 8
        ((cg,), [1]),                  # Test 9: One unweighted edge
        ((GraphAM(3, True),), [])      # Test 10: No edges
    ], P11, POINTS_PER_PROBLEM)
    except Exception as e:
        print(f"Problem 11 CRASHED: {e}")
        points_by_problem.append(0.0)
        print("Problem 11 Score: 0.0 /", POINTS_PER_PROBLEM)

    # -----------------------------
    # Problem 12 — get_adjacent_neighbors
    # OUTGOING neighbors only
    # -----------------------------
    def P12(graph, v):
        return graph.get_adjacent_neighbors(v)

    # Custom AM graphs for testing
    AM1 = GraphAM(6, directed=True)
    AM1.insert_edge(1, 0)
    AM1.insert_edge(1, 2)
    AM1.insert_edge(1, 4)

    AM2 = GraphAM(5, directed=True)
    AM2.insert_edge(0, 3)
    AM2.insert_edge(0, 2)

    AM3 = GraphAM(4, directed=False)
    AM3.insert_edge(2, 1)
    AM3.insert_edge(2, 3)

    AM4 = GraphAM(6, directed=True)
    # 5 isolated

    AM5 = GraphAM(6, directed=True)
    AM5.insert_edge(3, 5)
    AM5.insert_edge(3, 1)
    AM5.insert_edge(3, 4)

    try:
        section_score += grade_problem(12, [
        ((AM1, 1), [0,2,4]),           # Test 1: Three outgoing neighbors
        ((AM1, 0), []),                # Test 2: No outgoing neighbors
        ((AM2, 0), [2,3]),             # Test 3: Two neighbors sorted
        ((AM2, 3), []),                # Test 4: No outgoing neighbors
        ((AM3, 2), [1,3]),             # Test 5: Undirected behaves normally
        ((AM3, 1), [2]),               # Test 6: One outgoing (undirected)
        ((AM4, 5), []),                # Test 7: Isolated vertex
        ((AM5, 3), [1,4,5]),           # Test 8: Multiple outgoing edges
        ((unweighted, 0), [1,2,3]),    # Test 9: Main exam graph
        ((unweighted, 10), [])         # Test 10: No outgoing from 10
    ], P12, POINTS_PER_PROBLEM)
    except Exception as e:
        print(f"Problem 12 CRASHED: {e}")
        points_by_problem.append(0.0)
        print("Problem 12 Score: 0.0 /", POINTS_PER_PROBLEM)

    return section_score


# ---------------------------------------------------------------
# RUN BOTH SECTIONS AND PRINT CSV RESULT
# ---------------------------------------------------------------

try:
    al_score = test_graphAL()
    am_score = test_graphAM()
    final_score = al_score + am_score

    # CSV format: first_name,last_name,student_id,score1,...,score12,total
    csv_line = (
        str(first_name) + "," +
        str(last_name) + "," +
        str(student_id) + "," +
        ",".join(str(int(score)) for score in points_by_problem) +
        "," + "{:.2f}".format(final_score)
    )

    print(csv_line)
except Exception as e:
    # If there's an error, output zeros for all problems
    num_problems = 12
    csv_line = (
        str(first_name) + "," +
        str(last_name) + "," +
        str(student_id) + "," +
        ",".join(["0"] * num_problems) +
        ",0.00"
    )
    print(f"ERROR: {e}")
    print(csv_line)
#******************************************************************************
#DO NOT MODIFY THE CODE ABOVE
#******************************************************************************

'''

