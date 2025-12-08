from pathlib import Path
from .csv_loader import load_companies, load_connections, load_transactions
from .statistics import calculate_statistics
from .graph_builder import build_graph
from .visualizer import plot_graph_nodes

def main():
    # Get the directory of this script and construct paths relative to it
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"

    companies = load_companies(str(data_dir / "companies.csv"))
    connections = load_connections(str(data_dir / "connections.csv"))
    transactions = load_transactions(str(data_dir / "transactions.csv"))

    statistics = calculate_statistics(transactions)

    G = build_graph(companies, connections, statistics)

    fig = plot_graph_nodes(G)
    fig.show()

if __name__ == "__main__":
    main()
