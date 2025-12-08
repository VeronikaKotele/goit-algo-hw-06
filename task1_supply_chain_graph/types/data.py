"""
Data models for Supply Chain entities, connections, and transactions
"""

from typing import TypedDict


class Company(TypedDict):
    """Represents a company/entity in the supply chain"""
    id: str
    type: str
    name: str
    country: str
    lat: str
    lon: str


class Connection(TypedDict):
    """Represents a connection/flow between entities"""
    Flow_Id: str
    Id_From: str
    Id_To: str
    step_type: str


class Transaction(TypedDict):
    """Represents a transaction in the supply chain"""
    product_key: str
    product_name: str
    global_business_function: str
    category: str
    packaging: str
    nart_packaging: str
    flow_id_supplier: str
    flow_id_internal: str
    flow_id_customer: str
    order_qty: int
    actual_qty: int
    order_value_com: int
    actual_value_com: int
    order_value_sell: int
    actual_value_sell: int
