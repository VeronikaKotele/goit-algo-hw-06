from collections import deque
from enum import Enum

# class syntax
class GraphSearchMethod(Enum):
    BFS = 1
    DFS = 2

def find_related_leafs(G, company_id, method=GraphSearchMethod.BFS):
    """Find all leaf companies related to the given company in the directional graph."""
    related_leafs_with_path = dict()
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
            related_leafs_with_path[current_id] = current["path"] + [current_id]
        else:
            for neighbor in G.neighbors(current_id):
                queue.append({"id": neighbor, "path": current["path"] + [current_id]})
    return related_leafs_with_path

def find_related_leafs_compare(G, company_id):
    """Find all leaf companies related to the given company in the directional graph."""
    bfs_result = find_related_leafs(G, company_id, method=GraphSearchMethod.BFS)
    dfs_result = find_related_leafs(G, company_id, method=GraphSearchMethod.DFS)

    print(f"BFS found {len(bfs_result)} leaf companies:")
    for leaf_id, path in bfs_result.items():
        print(f"  Leaf ID: {leaf_id}, Path: {' -> '.join(path)}")

    print(f"\nDFS found {len(dfs_result)} leaf companies:")
    for leaf_id, path in dfs_result.items():
        print(f"  Leaf ID: {leaf_id}, Path: {' -> '.join(path)}")

    difference = set(bfs_result.keys()).symmetric_difference(set(dfs_result.keys()))
    if (difference) or (len(bfs_result) != len(dfs_result)):
        print("Warning! Number of leaf companies found differs between BFS and DFS.")

    print("\nComparing paths for common leaf companies found by both methods:")
    all_matched = True
    for leaf_id, path in bfs_result.items():
        if leaf_id in dfs_result:
            if path != dfs_result[leaf_id]:
                path_for_bfs = ' -> '.join(path)
                path_for_dfs = ' -> '.join(dfs_result[leaf_id])
                print(f"Different path for leaf ID: {leaf_id}, Path for BFS: {path_for_bfs}, for DFS: {path_for_dfs}")
                all_matched = False
    if all_matched:
        print("All paths match between BFS and DFS for common leaf companies.")
