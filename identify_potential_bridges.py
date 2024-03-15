import numpy as np
from scan_print_map import scan_map

def identify_potential_bridges(map):
    """
    Identify all possible bridges between islands in the puzzle.

    Args:
        map (np.array): 2D array representing the Hashiwokakero puzzle, where
                        each cell contains the number of bridges connectable to
                        that island, or 0 for water.

    Returns:
        tuple: A tuple containing a list of potential bridges and a dictionary
               mapping each island to its maximum number of connectable bridges.
    """
    nrow, ncol = map.shape
    potential_bridges = []  # To store the coordinates and direction of potential bridges
    island_degrees = {}  # To store the maximum number of bridges for each island

    # Scan the map for islands and identify possible bridges
    for r in range(nrow):
        for c in range(ncol):
            if map[r][c] > 0:  # Found an island
                max_bridges = map[r][c]  # Maximum bridges for this island
                possible_connections = 0  # Count of possible connections

                # Look to the right for possible horizontal bridges
                for c2 in range(c + 1, ncol):
                    if map[r][c2] > 0:
                        potential_bridges.append(((r, c), (r, c2), 'H'))
                        possible_connections += 1
                        break
                    elif map[r][c2] != 0:
                        break

                # Look downwards for possible vertical bridges
                for r2 in range(r + 1, nrow):
                    if map[r2][c] > 0:
                        potential_bridges.append(((r, c), (r2, c), 'V'))
                        possible_connections += 1
                        break
                    elif map[r2][c] != 0:
                        break

                # Only right and down directions are checked to avoid redundancy

                # Update the island's degree (max possible connections)
                island_degrees[(r, c)] = min(possible_connections, max_bridges)

    return potential_bridges, island_degrees

def main():
    """
    Main function to load the puzzle map, identify potential bridges, and display them.
    """
    nrow, ncol, map = scan_map()  # Load the puzzle map
    potential_bridges, island_degrees = identify_potential_bridges(map)
    
    # Output potential bridges and their respective degrees
    print("Potential Bridges:", potential_bridges)
    print("Island Degrees:", island_degrees)

if __name__ == "__main__":
    main()
