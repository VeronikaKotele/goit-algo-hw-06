from collections import deque
from enum import Enum

# class syntax
class GraphSearchMethod(Enum):
    BFS = 1
    DFS = 2

def find_related_leafs(G, company_id, method=GraphSearchMethod.BFS):
    """Find all leaf companies related to the given company in the directional graph."""
    related_leafs_with_path = set()
    queue = deque(({"id": neighbor_id, "path": [company_id]}) for neighbor_id in G.neighbors(company_id))
    visited = set([company_id])
    while queue:
        if method == GraphSearchMethod.BFS:
            current = queue.popleft()
        elif method == GraphSearchMethod.DFS:
            current = queue.pop()
        else:
            raise ValueError("Invalid graph search method")
        current_id = current["id"]
        if current_id in visited:
            continue
        visited.add(current_id)
        if G.out_degree(current_id) == 0:  # Leaf node
            related_leafs_with_path.add(current)
        else:
            for neighbor in G.neighbors(current_id):
                queue.append({"id": neighbor, "path": current["path"] + [current_id]})
    return related_leafs_with_path

def find_related_leafs_compare(G, company_id):
    """Find all leaf companies related to the given company in the directional graph."""
    bfs_result = find_related_leafs(G, company_id, method=GraphSearchMethod.BFS)
    dfs_result = find_related_leafs(G, company_id, method=GraphSearchMethod.DFS)

    print(f"BFS found {len(bfs_result)} leaf companies:")
    for leaf in bfs_result:
        print(f"  Leaf ID: {leaf['id']}, Path: {' -> '.join(leaf['path'] + [leaf['id']])}")

    print(f"\nDFS found {len(dfs_result)} leaf companies:")
    for leaf in dfs_result:
        print(f"  Leaf ID: {leaf['id']}, Path: {' -> '.join(leaf['path'] + [leaf['id']])}")

    difference = bfs_result.symmetric_difference(dfs_result)
    if difference:
        print("\nDifferences found between BFS and DFS results:")
        unique_ids = {leaf['id'] for leaf in difference}
        print(f"Unique leaf IDs in difference: {', '.join(unique_ids)}")
        for id in unique_ids:
            bfs_path = next((leaf['path'] for leaf in bfs_result if leaf['id'] == id), None)
            dfs_path = next((leaf['path'] for leaf in dfs_result if leaf['id'] == id), None)
            print(f"  Leaf ID: {id}, Path for BFS: {' -> '.join(bfs_path + [id])}, for DFS: {' -> '.join(dfs_path + [id])}  ")