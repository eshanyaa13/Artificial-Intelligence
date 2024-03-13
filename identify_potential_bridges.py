# identify_potential_bridges.py
import numpy as np
import sys
from scan_print_map import scan_map

def identify_potential_bridges(map):
    nrow, ncol = map.shape
    potential_bridges = []
    island_degrees = {}  # Track the degree of each island

    for r in range(nrow):
        for c in range(ncol):
            if map[r][c] > 0:  # An island is found
                island_degrees[(r, c)] = 0  # Initialize degree count
                # Check right for potential horizontal bridges
                for c2 in range(c + 1, ncol):
                    if map[r][c2] > 0:  # Another island found
                        potential_bridges.append(((r, c), (r, c2), 'H'))  # Record potential bridge
                        island_degrees[(r, c)] += 1
                        island_degrees[(r, c2)] = island_degrees.get((r, c2), 0) + 1
                        break
                    elif map[r][c2] != 0:  # Water or part of a bridge encountered
                        break
                # Check down for potential vertical bridges
                for r2 in range(r + 1, nrow):
                    if map[r2][c] > 0:  # Another island found
                        potential_bridges.append(((r, c), (r2, c), 'V'))  # Record potential bridge
                        island_degrees[(r, c)] += 1
                        island_degrees[(r2, c)] = island_degrees.get((r2, c), 0) + 1
                        break
                    elif map[r2][c] != 0:  # Water or part of a bridge encountered
                        break
    return potential_bridges, island_degrees

def main():
    # This example assumes the existence of a function to read the map, which you need to implement or adjust accordingly
    nrow, ncol, map = scan_map()  # Assuming a function from scan_print_map.py
    potential_bridges = identify_potential_bridges(map)
    print("Potential Bridges:", potential_bridges)

if __name__ == "__main__":
    main()

