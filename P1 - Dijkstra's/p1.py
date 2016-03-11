from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush
import sys


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    dist = {}
    prev = {}
    pq = []
    path = []
    index = 0
    dist[initial_position] = 0
    item = (dist[initial_position], index, initial_position)
    index += 1
    heappush(pq, item)
    while pq :
       curr_cell = heappop(pq)[2]
       neighbors = adj(graph, curr_cell)
       for curr_neighbor in neighbors:
          new_dist = dist[curr_cell] + curr_neighbor[1]
          if curr_neighbor[0] not in dist or new_dist < dist[curr_neighbor[0]]:
             dist[curr_neighbor[0]] = new_dist
             item = (new_dist, index, curr_neighbor[0])
             index += 1
             heappush(pq, item)
             prev[curr_neighbor[0]] = curr_cell
          if curr_neighbor[0] == destination:
             itor = curr_neighbor[0]
             while True:
                path.insert(0, itor)
                if itor not in prev:
                    break
                else:
                    itor = prev[itor]
    return path


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    dist = {}
    prev = {}
    pq = []
    index = 0
    dist[initial_position] = 0
    item = (dist[initial_position], index, initial_position)
    index += 1
    heappush(pq, item)
    while pq :
       curr_cell = heappop(pq)[2] 
       neighbors = adj(graph, curr_cell)
       for curr_neighbor in neighbors:
          new_dist = dist[curr_cell] + curr_neighbor[1] 
          if curr_neighbor[0] not in dist or new_dist < dist[curr_neighbor[0]]:
             dist[curr_neighbor[0]] = new_dist
             item = (new_dist, index, curr_neighbor[0])
             index += 1
             heappush(pq, item)
             prev[curr_neighbor[0]] = curr_cell
    return dist


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
             [((0,1), 1),
              ((1,0), 1),
              ((1,1), 1.4142135623730951),
              ... ]
    """
    result = []
    for x in range (cell[0]-1, cell[0]+2):
       for y in range(cell[1]-1, cell[1]+2):
          if (x,y) in level['walls']:
             pass
          elif (x,y) == cell:
             pass
          else:
             cost = find_cost(level, cell, (x,y))
             result.append(((x,y), cost))
    return result
    
    
def find_cost(level, cell1, cell2):
    """assumes cells are next to each other, returns cost to move
       between them
    """
    cost1 = level['spaces'][cell1]
    cost2 = level['spaces'][cell2]
    distance = get_distance(cell1, cell2)
    return (cost1 * distance) + (cost2 * distance)

    
def get_distance(p0, p1):
    return sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    #show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")

        
def write_path(filename, src_waypoint, dst_waypoint, ofname):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    #print("finding path from ", src_waypoint, " to ", dst_waypoint, " of this graph:")
    #show_level(level)
    #print("writing output to file: ", ofname)
    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]
    
    #save stdout
    tempstdout = sys.stdout
    stdout = open(ofname, "w")
    
    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")
    stdout = tempstdout


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    #print("costs of the following maze saved to my_maze_costs.csv")
    #show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    #test_filename, test_src_waypoint, test_dst_waypoint = 'example.txt', 'a','e'
    filename, source, destination = 'test_maze.txt', 'a', 'd'
    ofname = 'my_maze_path.txt'
    

    # Use this function call to find the route between two waypoints.
    test_route(filename, source, destination)
    
    # Writes path to file
    #write_path(filename, source, destination, ofname)
    
    #switch to my_maze
    filename = 'my_maze.txt'
    
    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, source, 'my_maze_costs.csv')
