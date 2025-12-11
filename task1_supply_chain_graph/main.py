from pathlib import Path
import networkx as nx
from .csv_loader import load_companies, load_connections, load_transactions
from .statistics import calculate_statistics
from .graph_builder import build_graph
from .visualizer import plot_graph_nodes, highlight_path
from .draw_with_matplotlib import draw_graph_with_matplotlib
from .task2 import find_related_leafs_compare

def get_valid_company_id(G, prompt, allow_quit=True):
    """Get and validate a company ID from user input."""
    while True:
        value = input(prompt).strip()
        if allow_quit and value.lower() in ['quit', 'exit', 'q']:
            return None
        if value in G.nodes():
            return value
        for node, data in G.nodes(data=True):
            if data['name'].lower() == value.lower():
                return data['id']
        print(f"Company ID or name '{value}' not found. Try again.")

def main():
    # Get the directory of this script and construct paths relative to it
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"

    companies = load_companies(str(data_dir / "companies.csv"))
    connections = load_connections(str(data_dir / "connections.csv"))
    transactions = load_transactions(str(data_dir / "transactions.csv"))

    statistics = calculate_statistics(transactions)

    G = build_graph(companies, connections, statistics)

    # test grapth without map
    #draw_graph_with_matplotlib(G)

    # visualize graph with map
    fig = plot_graph_nodes(G)
    fig.show()

    print(f"\nGraph loaded with {len(G.nodes())} companies and {len(G.edges())} connections.")
    print("Enter 'quit', 'exit', or 'q' to stop.\n")
    
    # Show sample company IDs
    sample_ids = list(G.nodes())[:5]
    print(f"Sample company IDs: {', '.join(sample_ids)}")
    
    while True:
        source = get_valid_company_id(G, "\nEnter source company ID or name: ")
        if source is None:
            break
            
        target = get_valid_company_id(G, "Enter target company ID or name: ")
        if target is None:
            break
            
        if source == target:
            print("Source and target must be different. Please try again.")
            continue
            
        try:
            path = nx.shortest_path(G, source, target, weight="weight")
            total_weight = nx.shortest_path_length(G, source, target, weight="weight")
            print(f"\n✓ Shortest path found ({len(path)} nodes, weight: {total_weight:.2f}):")
            # Show company names in path
            path_names = [G.nodes[node]['name'] for node in path]
            print(f"Path: {' → '.join(path_names)}")
            
            highlight_path(G, fig, path)
            fig.show() # show in new window

        except nx.NetworkXNoPath:
            print(f"✗ No path exists between {source} and {target}.")
    
    print("\nExiting...")

if __name__ == "__main__":
    main()
