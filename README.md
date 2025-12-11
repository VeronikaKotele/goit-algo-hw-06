# Supply Chain Graph Visualization

A Python-based supply chain network analysis and visualization tool that maps global company connections and transaction flows on an interactive geographic map.

## Overview

This project analyzes supply chain networks by:
- Loading company data, connections, and transactions from CSV files
- Building a directed graph representation of the supply chain network
- Calculating transaction statistics per company and flow
- Visualizing the network on an interactive map with geographic coordinates
- Finding and highlighting shortest paths between companies

## Features

- **Geographic Visualization**: Interactive map display using Plotly with company locations plotted on OpenStreetMap
- **Network Analysis**: Graph-based representation using NetworkX for analyzing supply chain relationships
- **Transaction Statistics**: Comprehensive statistics including transaction counts, values (total, average, min, max) per company and flow
- **Shortest Path Finding**: Interactive shortest path calculation between any two companies in the network
- **Dynamic Node Sizing**: Node sizes represent total transaction volume (imports + exports)
- **Dynamic Edge Weighting**: Edge thickness represents transaction flow volume

## Project Structure

```
goit-algo-hw-06/
├── task1_supply_chain_graph/
│   ├── __init__.py
│   ├── __main__.py
│   ├── main.py                    # Main application entry point
│   ├── csv_loader.py              # CSV data loading utilities
│   ├── csv_utils.py               # CSV helper functions
│   ├── graph_builder.py           # Graph construction logic
│   ├── statistics.py              # Transaction statistics calculation
│   ├── visualizer.py              # Plotly map visualization
│   ├── draw_with_matplotlib.py    # Alternative matplotlib visualization
│   ├── data/
│   │   ├── companies.csv          # Company information (id, name, type, country, lat, lon)
│   │   ├── connections.csv        # Connection flows between companies
│   │   └── transactions.csv       # Transaction records
│   └── models/
│       ├── __init__.py
│       ├── csv_data.py            # Data models for companies, connections, transactions
│       └── statistics_data.py     # Statistics data structures
├── conspects.py
├── dijkstra.py
└── README.md
```

## Requirements

- Python 3.8+
- NetworkX
- Plotly
- Matplotlib (optional, for alternative visualization)
- CSV support (built-in)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd goit-algo-hw-06
```

2. Install required dependencies:
```bash
pip install networkx plotly matplotlib
```

## Usage

### Running the Application

Run the main application as a module:
```bash
python -m task1_supply_chain_graph
```

### Interactive Path Finding

Once the application starts:
1. An interactive map will display showing all companies and connections
2. You will be prompted to enter source and target company IDs
3. The shortest path will be calculated and highlighted on the map
4. Continue entering new source/target pairs to explore different paths
5. The application validates IDs and ensures source ≠ target

Example interaction:
```
Enter source company ID or name: 42006406 # or Supplier R26
Enter target company ID or name: F001005176 # or Mystic Voyager B2A
✓ Shortest path found (4 nodes, weight: 3.96):
42006406 → 273 → 29 → F001005176
Path: Supplier R26 → Production Center China → Supplier S7 → Cosmic Nova TIW
```

## Data Format

### companies.csv
```csv
id,type,name,country,lat,lon
0001,Market Affiliate,Market Affiliate Germany,DE,53.550341,10.000654
```

### connections.csv
```csv
flow_id,id_from,id_to
```

### transactions.csv
```csv
flow_id_supplier,flow_id_internal,flow_id_customer,order_value
```

## Key Components

### Graph Builder
Constructs a NetworkX directed graph with:
- Nodes representing companies with geographic coordinates
- Edges representing supply chain connections
- Weighted edges based on transaction volumes
- Dynamic node sizing based on total transaction activity

### Statistics Calculator
Computes comprehensive transaction metrics:
- Global statistics across all transactions
- Per-flow statistics for each connection
- Per-company statistics (imported vs. exported)
- Min, max, average, and total transaction values

### Visualizer
Creates interactive map visualizations:
- Geographic plotting using Plotly Scattermapbox
- Node markers sized by transaction volume
- Edge lines weighted by flow volume
- Path highlighting for shortest path analysis

## Algorithms

- **Shortest Path**: Uses NetworkX's implementation (Dijkstra's algorithm) with edge weights
- **Graph Construction**: Filters companies and connections based on transaction data
- **Statistics**: Iterative calculation of min/max/avg/total values

## License

This project is part of the GoIT Algorithm Homework series.

## Author

Created for algorithm analysis and graph theory coursework.
