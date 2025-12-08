"""
Data models for Supply Chain entities, connections, and transactions
"""


from typing import NamedTuple


class Company(NamedTuple):
    """Represents a company/entity in the supply chain"""
    id: str
    type: str
    name: str
    country: str
    lat: str
    lon: str


class Connection(NamedTuple):
    """Represents a connection/flow between entities"""
    flow_id: str
    id_from: str
    id_to: str


class Transaction(NamedTuple):
    """Represents a transaction in the supply chain"""
    product_name: str
    product_category: str
    flow_id_supplier: str
    flow_id_internal: str
    flow_id_customer: str
    order_value: float
