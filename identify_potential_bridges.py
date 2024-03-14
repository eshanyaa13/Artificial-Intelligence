import numpy as np
import sys
from scan_print_map import scan_map

def identify_potential_bridges(map):
    nrow, ncol = map.shape
    potential_bridges = []
    island_degrees = {}  # Track the degree of each island, considering limits

    for r in range(nrow):
        for c in range(ncol):
            if map[r][c] > 0:  # An island is found
                max_bridges = map[r][c]  # Maximum bridges that can be connected to this island
                possible_connections = 0  # Initialize possible connections count

                # Check right for potential horizontal bridges
                for c2 in range(c + 1, ncol):
                    if map[r][c2] > 0:  # Another island found
                        potential_bridges.append(((r, c), (r, c2), 'H'))  # Record potential bridge
                        possible_connections += 1
                        break  # Stop checking further in this direction
                    elif map[r][c2] != 0:  # Water or part of a bridge encountered
                        break  # Stop checking further in this direction
                
                # Check down for potential vertical bridges
                for r2 in range(r + 1, nrow):
                    if map[r2][c] > 0:  # Another island found
                        potential_bridges.append(((r, c), (r2, c), 'V'))  # Record potential bridge
                        possible_connections += 1
                        break  # Stop checking further in this direction
                    elif map[r2][c] != 0:  # Water or part of a bridge encountered
                        break  # Stop checking further in this direction
                
                # Check left for potential horizontal bridges (Optional, depending on your needs)
                
                # Check up for potential vertical bridges (Optional, depending on your needs)

                # Update the degree of the island considering the limit
                # Degree cannot exceed the number on the island (max_bridges)
                island_degrees[(r, c)] = min(possible_connections, max_bridges)

    return potential_bridges, island_degrees

def main():
    nrow, ncol, map = scan_map()  # Assuming a function from scan_print_map.py
    potential_bridges, island_degrees = identify_potential_bridges(map)
    print("Potential Bridges:", potential_bridges)
    print("Island Degrees:", island_degrees)

if __name__ == "__main__":
    main()
