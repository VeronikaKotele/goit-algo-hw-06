import matplotlib.pyplot as plt
import networkx as nx

def draw_graph_with_matplotlib(G: nx.Graph):
    pos = nx.spring_layout(G)  # positions for all nodes

    # nodes
    node_sizes = [G.nodes[node].get('size', 300) for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='lightblue')

    # edges
    edge_weights = [G[u][v].get('weight', 1) for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=edge_weights, edge_color='gray', arrows=True)

    # labels
    labels = {node: G.nodes[node].get('name', node) for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=5)

    plt.title("Supply Chain Graph")
    plt.axis('off')  # Turn off the axis
    plt.show()

if __name__ == "__main__":
    # Example usage
    G = nx.DiGraph()
    G.add_node("1", name="Company A", size=20)
    G.add_node("2", name="Company B", size=30)
    G.add_edge("1", "2", weight=2)

    draw_graph_with_matplotlib(G)