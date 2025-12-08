# graph_loader.py
import csv
import networkx as nx
from .types import Company, Connection, Transaction
from scv_loader import load_companies, load_connections, load_transactions

def build_graph(nodes, edges):
    G = nx.Graph()

    # Add nodes with attributes
    for n in nodes:
        G.add_node(
            n["id"],
            label=n["label"],
            lat=n["lat"],
            lon=n["lon"]
        )

    # Add weighted edges
    for e in edges:
        G.add_edge(
            e["source"],
            e["target"],
            weight=e["weight"]
        )

    return G
