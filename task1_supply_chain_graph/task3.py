import heapq

class GraphPathNotFound(Exception):
    pass

def dijkstra_shortest_path(G, source, target):
    queue = []
    heapq.heappush(queue, (0, source))
    distances = {node: float('inf') for node in G.nodes}
    distances[source] = 0
    previous_nodes = {node: None for node in G.nodes}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor in G.neighbors(current_node):
            weight = G[current_node][neighbor].get('weight', 1)
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    path = []
    current_node = target
    if distances[target] == float('inf'):
        raise GraphPathNotFound(f"No path exists between {source} and {target}.")

    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path.reverse()

    return path, distances[target]