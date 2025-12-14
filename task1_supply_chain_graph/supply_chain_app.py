from enum import Enum
import networkx as nx
from .statistics import GlobalTransactionStatistics
from .draw_with_matplotlib import draw_graph_with_matplotlib
from .draw_with_plotly import plot_graph_nodes, highlight_path
from .task2 import find_related_leafs_compare
from .task3 import GraphPathNotFound, dijkstra_shortest_path

class SupplyChainApp:
    class Tasks(Enum):
        VISUALIZE_GRAPH = '1'
        FIND_RELATED_LEAFS = '2'
        SHORTEST_PATH = '3'
        SHOW_STATISTICS = '4'
        QUIT = 'q'

    class DisplayTools(Enum):
        MATPLOTLIB = '1'
        PLOTLY = '2'

    class ShortestPathAlgorithms(Enum):
        CUSTOM_DIJKSTRA = '1'
        NETWORKX_BUILTIN = '2'

    @staticmethod
    def print_info():
        print("Supply Chain Graph Application")
        print("This application allows you to visualize and analyze a supply chain graph.")
        print("You can visualize the graph, find related distribution centers,")
        print("compute shortest paths between companies, and view transaction statistics.")
        print("Graph node and edge sizes are proportional to transaction volumes.")
        print("Enter 'quit', 'exit', or 'q' at any prompt to stop the application.\n")

    def __init__(self, graph: nx.Graph, statistics: GlobalTransactionStatistics):
        self.graph = graph
        self.statistics = statistics
        self.display_tool = SupplyChainApp.DisplayTools.PLOTLY.value

    def set_display_tool(self, tool: DisplayTools):
        self.display_tool = tool

    def run(self):
        while True:
            task = self.get_task_choice()
            if task == SupplyChainApp.Tasks.QUIT:
                break

            if task == SupplyChainApp.Tasks.VISUALIZE_GRAPH:
                self.display_tool = self.get_valid_display_tool()
                if self.display_tool is None:
                    break
                self.show_graph()
            elif task == SupplyChainApp.Tasks.FIND_RELATED_LEAFS:
                company_id = self.get_valid_company_id("\nEnter company ID or name to start search for related distribution centers (grapth leafs): ")
                if company_id is None:
                    break
                find_related_leafs_compare(self.graph, company_id)
            elif task == SupplyChainApp.Tasks.SHORTEST_PATH:
                source = self.get_valid_company_id("\nEnter source company ID or name: ")
                if source is None:
                    break
                target = self.get_valid_company_id("Enter target company ID or name: ")
                if target is None:
                    break
                if source == target:
                    print("Source and target must be different. Please try again.")
                    continue


                alg_to_use = self.get_valid_algorithm_choice()
                if alg_to_use is None:
                    break
                path, total_weight = self.find_shortest_path(source, target, alg_to_use.value)
                if not path:
                    print(f"✗ No path exists between {self.graph.nodes[source]['name']} ({source}) and {self.graph.nodes[target]['name']} ({target}).")
                    continue

                print(f"\n✓ Shortest path found ({len(path)} nodes, weight: {total_weight:.2f}):")
                # Show company names in path
                path_names = [self.graph.nodes[node]['name'] for node in path]
                print(f"Path: {' → '.join(path_names)}")

                self.highlight_path(path)

            elif task == SupplyChainApp.Tasks.SHOW_STATISTICS:
                self.show_statistics_summary()

        confirm_leave = input("Are you sure you want to quit? (y/n): ").strip().lower()
        if confirm_leave == 'y':
            print("Exiting the Supply Chain Graph Application. Goodbye!")
        else:
            print("Returning to the application.")
            self.run()

    def show_graph(self):
        """Show the graph using the selected display tool."""
        try:
            if self.display_tool == SupplyChainApp.DisplayTools.MATPLOTLIB.value:
                draw_graph_with_matplotlib(self.graph)
            elif self.display_tool == SupplyChainApp.DisplayTools.PLOTLY.value:
                fig = plot_graph_nodes(self.graph)
                fig.show()
        except Exception as e:
            print(f"Error displaying graph: {e}, recommending to switch display tool or restart app.")

    def find_shortest_path(self, source: str, target: str, algorithm: str) -> tuple[list[str], float]:
        """Find the shortest path between source and target using the specified algorithm."""
        if algorithm == SupplyChainApp.ShortestPathAlgorithms.CUSTOM_DIJKSTRA.value:
            try:
                path, total_weight = dijkstra_shortest_path(self.graph, source, target)
                return path, total_weight
            except GraphPathNotFound:
                return [], 0.0
        elif algorithm == SupplyChainApp.ShortestPathAlgorithms.NETWORKX_BUILTIN.value:
            try:
                path = nx.shortest_path(self.graph, source, target, weight="weight")
                total_weight = nx.shortest_path_length(self.graph, source, target, weight="weight")
                return path, total_weight
            except nx.NetworkXNoPath:
                return [], 0.0
        else:
            raise ValueError(f"Invalid algorithm choice: {algorithm}")

    def highlight_path(self, highlight_path_nodes: list[str]):
        """Highlight a path on the plotly figure."""
        if self.display_tool == SupplyChainApp.DisplayTools.MATPLOTLIB.value:
            draw_graph_with_matplotlib(self.graph, highlight_path_nodes)
        elif self.display_tool == SupplyChainApp.DisplayTools.PLOTLY.value:
            fig = plot_graph_nodes(self.graph)
            highlight_path(self.graph, fig, highlight_path_nodes)

    def show_statistics_summary(self):
        print("\nGlobal Transaction Statistics:")
        global_stats = self.statistics['global_statistics']
        print(f"  Total Transactions: {global_stats['quantity']}")
        print(f"  Total Value: {global_stats['total_value']:.2f}")
        print(f"  Average Value: {global_stats['average_value']:.2f}")
        print(f"  Max Value: {global_stats['max_value']:.2f}")
        print(f"  Min Value: {global_stats['min_value']:.2f}")

        show_for_company = input("\nDo you want to see statistics for a specific company? (y/n): ").strip().lower()
        if show_for_company == 'y':
            company_id = self.get_valid_company_id("Enter company ID or name: ")
            if company_id is None:
                return
            if company_id not in self.statistics['statistics_per_company']:
                print(f"No statistics available for Company ID {company_id}.")
            else:
                company_stats = self.statistics['statistics_per_company'][company_id]
                print(f"\nStatistics for Company ID {company_id} - {self.graph.nodes[company_id]['name']}:")
                exported = company_stats['exported']
                imported = company_stats['imported']
                print("  Exported:")
                print(f"    Total Transactions: {exported['quantity']}")
                print(f"    Total Value: {exported['total_value']:.2f}")
                print(f"    Average Value: {exported['average_value']:.2f}")
                print(f"    Max Value: {exported['max_value']:.2f}")
                print(f"    Min Value: {exported['min_value']:.2f}")
                print("  Imported:")
                print(f"    Total Transactions: {imported['quantity']}")
                print(f"    Total Value: {imported['total_value']:.2f}")
                print(f"    Average Value: {imported['average_value']:.2f}")
                print(f"    Max Value: {imported['max_value']:.2f}")
                print(f"    Min Value: {imported['min_value']:.2f}")

    def get_task_choice(self) -> Tasks:
        """Get and validate task choice from user input."""
        while True:
            task = input("\nChoose task - \n"
            "(1) Visualize graph or change display tool\n" \
            "(2) Execute and compare BFS/DFS leaf search, \n"
            "(3) Find shortest path between companies \n"
            "(4) Show statistics summary \n"
            "(q) Quit: ").strip()

            for t in SupplyChainApp.Tasks:
                if task == t.value:
                    return t
            if task.lower() in ['quit', 'exit']:
                return SupplyChainApp.Tasks.QUIT
            print("Invalid task choice. Please try again.")

    def get_valid_display_tool(self) -> DisplayTools | None:
        """Get and validate display tool choice from user input."""
        while True:
            value = input("\nChoose graph display tool - \n"
            "(1) Show graph with matplotlib - connection-driven placing, process-blocking until window closed\n"
            "(2) Show graph with plotly - place company nodes on earth map, non-blocking, opens in web browser\n"
            "(q) Quit: ").strip()
            if value in [dt.value for dt in SupplyChainApp.DisplayTools]:
                return value
            elif value in ['q', 'quit', 'exit']:
                return None
            print(f"Invalid choice '{value}'. Please enter '1' or '2'.")

    def get_valid_algorithm_choice(self) -> ShortestPathAlgorithms | None:
        """Get and validate shortest path algorithm choice from user input."""
        while True:
            value = input("\nChoose shortest path algorithm - \n"
            "(1) Custom Dijkstra's algorithm (considers edge weights) \n"
            "(2) Built-in NetworkX algorithm (considers edge weights) \n"
            "(q) Quit: ").strip()
            for alg in SupplyChainApp.ShortestPathAlgorithms:
                if value == alg.value:
                    return alg
            if value.lower() in ['q', 'quit', 'exit']:
                return None
            print("Invalid algorithm choice. Please try again.")

    def get_valid_company_id(self, prompt, allow_quit=True) -> str | None:
        """Get and validate a company ID from user input."""
        while True:
            value = input(prompt).strip()
            if allow_quit and value.lower() in ['quit', 'exit', 'q']:
                return None
            if value in self.graph.nodes():
                return value
            for node, data in self.graph.nodes(data=True):
                if data['name'].lower() == value.lower():
                    return data['id']
            print(f"Company ID or name '{value}' not found. Try again.")