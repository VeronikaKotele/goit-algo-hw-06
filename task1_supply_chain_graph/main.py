from pathlib import Path
import networkx as nx
from .csv_loader import load_companies, load_connections, load_transactions
from .statistics import calculate_statistics
from .graph_builder import build_graph
from .visualizer import plot_graph_nodes, highlight_path
from .draw_with_matplotlib import draw_graph_with_matplotlib

def main():
    # Get the directory of this script and construct paths relative to it
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"

    companies = load_companies(str(data_dir / "companies.csv"))
    connections = load_connections(str(data_dir / "connections.csv"))
    transactions = load_transactions(str(data_dir / "transactions.csv"))

    statistics = calculate_statistics(transactions)

    G = build_graph(companies, connections, statistics)

    #draw_graph_with_matplotlib(G)

    fig = plot_graph_nodes(G)
    fig.show()

    source = input("Enter source company ID: ").strip()
    target = input("Enter target company ID: ").strip()

    while True:
        if source == target:
            print("Enter different source and target company IDs.")
            source = input("Enter source company ID: ").strip()
            target = input("Enter target company ID: ").strip()
            continue
        if source not in G.nodes():
            print("source IDs not found in the graph. Please try again.")
            source = input("Enter source company ID: ").strip()
            continue
        if target not in G.nodes():
            print("target company IDs not found in the graph. Please try again.")
            target = input("Enter target company ID: ").strip()
            continue
        try:
            path = nx.shortest_path(G, source, target, weight="weight")
            print("Shortest path found.")
            print(path)
            highlight_path(G, fig, path)
            fig.update()
            # Update highlight trace (last trace)
            # highlight_idx = len(fig.data) - 1
            # fig.data[highlight_idx].lines.color = 'red'
            # fig.data[highlight_idx].lines.width = 6

            # # Redraw only this figure:
            # plot.plotly_chart(fig, use_container_width=True)

            source = input("Enter source company ID: ").strip()
            target = input("Enter target company ID: ").strip()
        except nx.NetworkXNoPath:
            print("No path found between the specified companies. Please try again.")
            source = input("Enter source company ID: ").strip()
            target = input("Enter target company ID: ").strip()

if __name__ == "__main__":
    main()
