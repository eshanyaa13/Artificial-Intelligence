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

def print_solution(map, bridges):
    solution_map = np.full(map.shape, '.', dtype=str)
    for r in range(map.shape[0]):
        for c in range(map.shape[1]):
            if map[r, c] > 0:
                solution_map[r, c] = str(map[r, c])

    # Updated symbol selection for bridge planks
    symbols = {
        'H': {1: '-', 2: '=', 3: 'E'},  # Horizontal bridge symbols
        'V': {1: '|', 2: '\"', 3: '#'}   # Vertical bridge symbols
    }

    for (r1, c1), (r2, c2), orientation, planks in bridges:
        if planks > 0:  # Skip if no bridge is built
            symbol = symbols[orientation][planks]
            if orientation == 'H':
                for c in range(c1 + 1, c2):
                    solution_map[r1, c] = symbol
            else:  # Vertical bridge
                for r in range(r1 + 1, r2):
                    solution_map[r, c1] = symbol

    for row in solution_map:
        print(''.join(row))

def update_bridge_counts(bridges, island_bridge_counts):
    for bridge in bridges:
        if bridge[3] > 0:  # If planks > 0
            for island in [bridge[0], bridge[1]]:
                island_bridge_counts[island] += bridge[3]

def is_dead_end(map, island_bridge_counts):
    for island, count in island_bridge_counts.items():
        if count > map[island]:
            return True
    return False

def search_for_solution(map, bridges, island_bridge_counts, index=0):
    if index == len(bridges):
        if is_solution_valid(map, bridges):
            print_solution(map, bridges)
            return True
        else:
            return False

    (r1, c1), (r2, c2), orientation = bridges[index][:3]
    for planks in range(4):  # Try 0 to 3 planks
        # Temporarily update counts to reflect the addition of the current bridge
        island_bridge_counts[(r1, c1)] += planks
        island_bridge_counts[(r2, c2)] += planks
        bridges[index] = ((r1, c1), (r2, c2), orientation, planks)
        
        if not is_dead_end(map, island_bridge_counts) and search_for_solution(map, bridges, island_bridge_counts, index + 1):
            return True
        
        # Revert counts if this path is not successful
        island_bridge_counts[(r1, c1)] -= planks
        island_bridge_counts[(r2, c2)] -= planks
    
    return False

def main():
    nrow, ncol, map = scan_map()
    potential_bridges = identify_potential_bridges(map)
    modified_bridges = [(bridge[0], bridge[1], bridge[2], 0) for bridge in potential_bridges]  # Initialize with 0 planks

    # Initialize island_bridge_counts
    island_bridge_counts = {(r, c): 0 for r in range(map.shape[0]) for c in range(map.shape[1]) if map[r, c] > 0}

    if not search_for_solution(map, np.array(modified_bridges, dtype=object), island_bridge_counts):
        print("No solution found.")

if __name__ == "__main__":
    main()
