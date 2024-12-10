from collections import deque
import heapq

def get_graph_from_user():
    graph = {}
    num_nodes = int(input("Enter the number of nodes: "))

    for _ in range(num_nodes):
        node = input("Enter a node: ")
        neighbors = input(f"Enter neighbors of {node} (space-separated): ").split()
        graph[node] = neighbors

    edge_costs = {}
    num_edges = int(input("Enter the number of edges: "))
    for _ in range(num_edges):
        node1, node2, cost = input("Enter an edge (node1 node2 cost): ").split()
        edge_costs[(node1, node2)] = int(cost)
        edge_costs[(node2, node1)] = int(cost)  # Assuming undirected graph

    start = input("Enter the start node: ")
    goal = input("Enter the goal node: ")

    return graph, start, goal, edge_costs

def calculate_path_cost(graph, path, edge_costs):
    cost = 0
    for i in range(len(path) - 1):
        current_node, next_node = path[i], path[i+1]
        cost += edge_costs[(current_node, next_node)]
    return cost

def heuristic(node, goal):
    # Replace with a more suitable heuristic for your specific problem
    # Here, we're using a simple Euclidean distance heuristic
    x1, y1 = node
    x2, y2 = goal
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def ao_star_search(graph, start, goal, edge_costs, heuristic):
    open_list = [(heuristic(start, goal), 0, [start])]  # (f_score, g_score, path)
    closed_list = set()

    while open_list:
        _, current_g_score, current_path = heapq.heappop(open_list)
        current_node = current_path[-1]

        if current_node == goal:
            return current_path

        if current_node not in closed_list:
            closed_list.add(current_node)

            for neighbor in graph[current_node]:
                if isinstance(neighbor, tuple):  # AND node
                    for child in neighbor:
                        new_path = current_path + [child]
                        new_g_score = current_g_score + edge_costs[(current_node, child)]
                        new_f_score = new_g_score + heuristic(child, goal)
                        heapq.heappush(open_list, (new_f_score, new_g_score, new_path))
                else:  # OR node
                    new_path = current_path + [neighbor]
                    new_g_score = current_g_score + edge_costs[(current_node, neighbor)]
                    new_f_score = new_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (new_f_score, new_g_score, new_path))

    return None

if __name__ == "__main__":
    graph, start, goal, edge_costs = get_graph_from_user()

    path = ao_star_search(graph, start, goal, edge_costs, heuristic)

    if path:
        print("Shortest path found:", path)
        print("Path cost:", calculate_path_cost(graph, path, edge_costs))
    else:
        print("No path found.")