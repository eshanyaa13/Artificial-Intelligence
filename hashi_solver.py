# hashi_solver.py
import numpy as np
import sys
from scan_print_map import scan_map
from identify_potential_bridges import identify_potential_bridges

def is_solution_valid(map, bridges):
    # Initialize a dictionary to count bridges for each island
    bridge_count = {(r, c): 0 for r in range(map.shape[0]) for c in range(map.shape[1]) if map[r, c] > 0}

    # Count bridges based on the solution
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
    solution_map = np.full(puzzle_map.shape, '.', dtype=str)
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
    for island, count in island_bridge_counts.items():
        if count > map[island]:
            return True
    return False


def update_bridge_counts(bridges, island_bridge_counts):
    # Resets island bridge counts for a fresh calculation
    for island in island_bridge_counts.keys():
        island_bridge_counts[island] = 0
    
    # Recalculate bridge counts based on current bridge placements
    for (r1, c1), (r2, c2), orientation, planks in bridges:
        if planks > 0:  # Consider only placed bridges
            island_bridge_counts[(r1, c1)] += planks
            island_bridge_counts[(r2, c2)] += planks

def forward_check(map, island_bridge_counts):
    for island, count in island_bridge_counts.items():
        if count > map[island]:
            return False
    return True

def forward_check_and_arc_consistency(map, bridges, island_bridge_counts):
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
    nrow, ncol, map = scan_map()
    potential_bridges, island_degrees = identify_potential_bridges(map)

    potential_bridges.sort(key=lambda x: island_degrees[x[0]] + island_degrees[x[1]])

    modified_bridges = [(bridge[0], bridge[1], bridge[2], 0) for bridge in potential_bridges]

    # Initialize island_bridge_counts with 0 for each island
    island_bridge_counts = {(r, c): 0 for r in range(nrow) for c in range(ncol) if map[r, c] > 0}

    if not search_for_solution(map, np.array(modified_bridges, dtype=object), island_bridge_counts):
        print("No solution found.")

if __name__ == "__main__":
    main()
