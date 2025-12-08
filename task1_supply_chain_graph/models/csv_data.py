"""
Data models for Supply Chain entities, connections, and transactions
"""


class Company:
    """Represents a company/entity in the supply chain"""
    id: str
    type: str
    name: str
    country: str
    lat: str
    lon: str


class Connection:
    """Represents a connection/flow between entities"""
    Flow_Id: str
    Id_From: str
    Id_To: str


class Transaction:
    """Represents a transaction in the supply chain"""
    product_name: str
    product_category: str
    flow_id_supplier: str
    flow_id_internal: str
    flow_id_customer: str
    order_value: int
