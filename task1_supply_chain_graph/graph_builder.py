import networkx as nx
from .models import Company, Connection, Transaction, GlobalTransactionStatistics

def build_graph(companies: list[Company], 
                connections: list[Connection], 
                statistics: GlobalTransactionStatistics
                ) -> nx.Graph:
    """Builds a NetworkX graph from companies, connections, transactions, and statistics"""

    filtered_companies = [company for company in companies if company.id in statistics.statistics_per_company]
    filtered_connections = [connection for connection in connections if connection.flow_id in statistics.statistics_per_flow]

    min_node_size = 10.0
    max_node_size = 30.0
    d_node_size = max_node_size - min_node_size
    min_edge_weight = 1.0
    max_edge_weight = 3.0
    d_edge_weight = max_edge_weight - min_edge_weight

    def get_company_size(company: Company) -> float:
        return statistics.statistics_per_company[company.id].exported.total_value + statistics.statistics_per_company[company.id].imported.total_value
    company_sizes = {company.id : get_company_size(company) for company in filtered_companies}
    min_company_size = min(company_sizes.values())
    max_company_size = max(company_sizes.values())
    d_company_size = max_company_size - min_company_size

    min_connection_size = min(statistics.statistics_per_flow.values(), key=lambda x: x.total_value).total_value
    max_connection_size = max(statistics.statistics_per_flow.values(), key=lambda x: x.total_value).total_value
    d_connection_size = max_connection_size - min_connection_size

    def compute_node_size(company: Company) -> float:
        k = (company_sizes[company.id] - min_company_size) / d_company_size
        return min_node_size + k * d_node_size
    
    def compute_edge_size(connection: Connection) -> float:
        k = (statistics.statistics_per_flow[connection.flow_id].total_value - min_connection_size) / d_connection_size
        return min_edge_weight + k * d_edge_weight

    G = nx.Graph()

    for company in filtered_companies:
        G.add_node(
            company.id,
            size=compute_node_size(company),
            **company._asdict(),
        )
    for connection in filtered_connections:
        if (connection.id_from not in G.nodes) or (connection.id_to not in G.nodes):
            continue
        G.add_edge(
            connection.id_from,
            connection.id_to,
            weight=compute_edge_size(connection),
            **connection._asdict(),
        )

    return G
