#!/Users/aryankapoor/COMP3411/Assignment_1/myvenv/bin/python


'''
Briefly describe how your program works, including any algorithms and data structures employed, and explain any design decisions you made along the way.

Our program solves the Hashiwokakero (or Hashi) puzzle using a systematic approach, breaking down the process into distinct phases. 
Initially, we represent the puzzle as a rectangular array using NumPy, facilitating efficient numerical operations and state representation. 
This representation is crucial for identifying islands (numbers) and water (dots).In the first phase, we employ 
the identify_potential_bridges function to scan the puzzle grid and list all feasible bridges between islands. This is achieved by iterating 
through the grid, and when an island is encountered, we look rightward and downward to find another island to connect with a bridge, avoiding 
redundant checks and crossings. This function also keeps track of the maximum number of bridges each island can connect to, storing this information 
in a dictionary that maps island coordinates to their corresponding bridge limits.

In the main hashi_solver.py, we then use a backtracking algorithm to find a valid solution. This method systematically explores potential bridge 
placements, incrementally building a solution and backtracking when a configuration leads to a dead end or violates the puzzle rules. Bridges are 
represented as tuples containing their endpoints, orientation, and the number of planks (0 to 3). We prioritize exploring bridge connections between 
islands with fewer connectivity options, as this heuristic can lead to quicker identification of dead ends and reduce the search space.The validity of 
a solution is continuously checked through functions like is_solution_valid, ensuring that the number of bridges connected to each island matches the 
required number and that bridges do not cross each other or islands. The forward_check_and_arc_consistency function further optimizes the search by 
pruning paths that cannot possibly fulfill all island bridge requirements. Through these strategies, our program can efficiently navigate the complex 
search space of Hashiwokakero puzzles, aiming to find a valid solution that satisfies all game rules.

'''



# hashi_solver.py
import numpy as np
from scan_print_map import scan_map
from identify_potential_bridges import identify_potential_bridges

def is_solution_valid(map, bridges):
    """
    Validates if the current bridge configuration satisfies all puzzle constraints.
    """
    # Count bridges connected to each island
    bridge_count = {(r, c): 0 for r in range(map.shape[0]) for c in range(map.shape[1]) if map[r, c] > 0}

    # Iterate over each bridge and update counts
    for (r1, c1), (r2, c2), orientation, planks in bridges:
        if planks == 0:  # Skip if no bridge is built
            continue
        # Increment bridge counts for both islands
        bridge_count[(r1, c1)] += planks
        bridge_count[(r2, c2)] += planks

        # Check for bridge crossing or incorrect placement
        if orientation == 'H':
            for c in range(min(c1, c2) + 1, max(c1, c2)):
                if map[r1, c] != 0 or bridge_count.get((r1, c), 0) > 0:
                    return False
        else:  # Vertical bridge
            for r in range(min(r1, r2) + 1, max(r1, r2)):
                if map[r, c1] != 0 or bridge_count.get((r, c1), 0) > 0:
                    return False

    # Validate bridge count matches island number
    for (r, c), count in bridge_count.items():
        if map[r, c] != count:
            return False

    return True

def print_solution(puzzle_map, bridges):
    """
    Prints the solved puzzle map with all bridges placed.
    """
    # Initialize the solution map
    solution_map = np.full(puzzle_map.shape, '.', dtype=str)

    # Fill in the islands and their numbers
    for r in range(puzzle_map.shape[0]):
        for c in range(puzzle_map.shape[1]):
            if puzzle_map[r, c] > 0:
                # Check if the island number is greater than 9 and convert accordingly
                if puzzle_map[r, c] > 9:
                    # Convert numbers 10, 11, 12, etc., to 'a', 'b', 'c', etc.
                    solution_map[r, c] = chr(puzzle_map[r, c] - 10 + ord('a'))
                else:
                    # For numbers 1-9, simply convert to string
                    solution_map[r, c] = str(puzzle_map[r, c])
    
    # Apply bridges to the solution map
    for bridge in bridges:
        (r1, c1), (r2, c2), orientation, planks = bridge
        if planks > 0:
            # Choose the symbol based on the number of planks
            if orientation == 'H':
                symbol = '-' if planks == 1 else '=' if planks == 2 else 'E'
                for c in range(min(c1, c2) + 1, max(c1, c2)):
                    solution_map[r1, c] = symbol
            else:  # orientation == 'V'
                symbol = '|' if planks == 1 else '\"' if planks == 2 else '#'
                for r in range(min(r1, r2) + 1, max(r1, r2)):
                    solution_map[r, c1] = symbol

    # Print the solution map
    for row in solution_map:
        print(''.join(row))

def is_dead_end(map, island_bridge_counts):
    """
    Checks if the current bridge configuration leads to a dead-end.
    """
    # A dead-end occurs if any island exceeds its bridge count
    for island, count in island_bridge_counts.items():
        if count > map[island]:
            return True
    return False


def update_bridge_counts(bridges, island_bridge_counts):
    """
    Updates the count of bridges connected to each island based on current configuration.
    """
    # Resets island bridge counts for a fresh calculation
    for island in island_bridge_counts.keys():
        island_bridge_counts[island] = 0
    
    # Recalculate bridge counts based on current bridge placements
    for (r1, c1), (r2, c2), orientation, planks in bridges:
        if planks > 0:  # Consider only placed bridges
            island_bridge_counts[(r1, c1)] += planks
            island_bridge_counts[(r2, c2)] += planks

def forward_check(map, island_bridge_counts):
    """
    Performs a forward check to ensure no island exceeds its bridge count.
    """
    for island, count in island_bridge_counts.items():
        if count > map[island]:
            return False
    return True

def forward_check_and_arc_consistency(map, bridges, island_bridge_counts):
    """
    Checks the current bridge configuration for consistency and forward feasibility.
    """
    # Iterate over islands in island_bridge_counts
    for (r, c), current_count in island_bridge_counts.items():
        required_count = map[r, c]  # Directly access required count from map
        
        if current_count > required_count:
            return False
        
        # Estimate potential bridges for the island
        potential_bridge_options = 0
        for bridge in bridges:
            if (r, c) in [bridge[0], bridge[1]] and bridge[3] == 0:
                potential_bridge_options += 3  # Assume maximum possibility
        
        if current_count + potential_bridge_options < required_count:
            return False
    
    return True

def search_for_solution(map, bridges, island_bridge_counts, index=0):
    """
    Recursive function to search for a valid solution to the Hashiwokakero puzzle.
    """
    if index == len(bridges):
        if is_solution_valid(map, bridges):
            print_solution(map, bridges)
            return True
        else:
            return False

    (r1, c1), (r2, c2), orientation = bridges[index][:3]
    for planks in range(4):  # Try placing 0 to 3 planks
        bridges[index] = ((r1, c1), (r2, c2), orientation, planks)
        update_bridge_counts(bridges, island_bridge_counts)
        
        if forward_check_and_arc_consistency(map, bridges, island_bridge_counts):
            if search_for_solution(map, bridges, island_bridge_counts, index + 1):
                return True
        
        # Revert bridge placement if the path does not lead to a solution
        bridges[index] = ((r1, c1), (r2, c2), orientation, 0)

    return False  # No valid configuration found along this path

def main():
    """
    Main function to solve the Hashiwokakero puzzle.
    """
    nrow, ncol, map = scan_map()
    potential_bridges, island_degrees = identify_potential_bridges(map)

    # Sort bridges based on connectivity potential
    potential_bridges.sort(key=lambda x: island_degrees[x[0]] + island_degrees[x[1]])

    modified_bridges = [(bridge[0], bridge[1], bridge[2], 0) for bridge in potential_bridges]

    # Initialize island_bridge_counts with 0 for each island
    island_bridge_counts = {(r, c): 0 for r in range(nrow) for c in range(ncol) if map[r, c] > 0}

    if not search_for_solution(map, np.array(modified_bridges, dtype=object), island_bridge_counts):
        print("No solution found.")

if __name__ == "__main__":
    main()
