from pathlib import Path
from .csv_loader import load_companies, load_connections, load_transactions
from .statistics import calculate_statistics
from .graph_builder import build_graph
from .supply_chain_app import SupplyChainApp

def main():
    print("Hi, it's supply chain data visualizer!")
    print("It loads data about companies and transactions from csv and builds an oriented graph, " \
    "so you can explore and get insights about supply chain data and find useful information")
    print("PS: pardon for not the most user-friendly UX, reactive grapth visuals would require a setup with extra dependencies, " \
    "so this is a quick console-based solution for homework purpose.")

    # Get the directory of this script and construct paths relative to it
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"

    print("Loading data about companies, connections and transactions...")
    companies = load_companies(str(data_dir / "companies.csv"))
    connections = load_connections(str(data_dir / "connections.csv"))
    transactions = load_transactions(str(data_dir / "transactions.csv"))

    print("Calculating statistics based on transactions...")
    statistics = calculate_statistics(transactions)

    print("Building graph...")
    graph = build_graph(companies, connections, statistics)
    print(f"\nGraph loaded with {len(graph.nodes())} companies and {len(graph.edges())} connections.")
    print("Enter 'quit', 'exit', or 'q' to stop.\n")

    print("Loading application...")
    app = SupplyChainApp(graph, statistics)
    print("Application loaded.")
    app.print_info()
    print("Graph will be displayed separately, but user interaction is still through console. Ready to start?")
    display_tool = app.get_valid_display_tool()
    if display_tool is not None:
        app.set_display_tool(display_tool)
        app.show_graph()
        app.run()
    
    print("\nExiting...")

if __name__ == "__main__":
    main()
