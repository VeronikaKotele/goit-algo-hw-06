import csv
from .models import Company, Connection, Transaction

def load_rows_from_csv(csv_path: str, transform: callable = None) -> list[dict]:
  """
  Loads rows from a CSV file
  
  Args:
    csv_path: Path to the CSV file
      
  Returns:
    List of dictionaries representing CSV rows
  """
  try:
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as file:
      reader = csv.DictReader(file)
      for row in reader:
        if transform:
          transform(row)
        rows.append(row)
      print(f"Loading CSV from: {csv_path}")
      return rows
  except Exception as error:
    print(f'Error loading data from CSV: {error}')
    return []

def load_companies(csv_path: str) -> list[Company]:
    """
    Loads company markers from a CSV file
    
    Args:
      csv_path: Path to the CSV file
        
    Returns:
      List of Company objects
    """
    try:
      rows = load_rows_from_csv(csv_path)
      return [Company(**row) for row in rows]  # type: ignore
    except Exception as error:
      print(f'Error loading companies from CSV: {error}')
      return []


def load_connections(csv_path: str) -> list[Connection]:
    """
    Loads connection markers from a CSV file
    
    Args:
      csv_path: Path to the CSV file
        
    Returns:
      List of Connection objects
    """
    try:
      rows = load_rows_from_csv(csv_path)
      return [Connection(flow_id=row['flow_id'], id_from=row['id_from'], id_to=row['id_to']) for row in rows]  # type: ignore
    except Exception as error:
      print(f'Error loading connections from CSV: {error}')
      return []

def load_transactions(csv_path: str) -> list[Transaction]:
    """
    Loads transactions from CSV file
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        List of Transaction objects
    """
    try:
      rows = load_rows_from_csv(csv_path)
      return [Transaction(
          product_name=row['product_name'],
          product_category=row['product_category'],
          flow_id_supplier=row['flow_id_supplier'],
          flow_id_internal=row['flow_id_internal'],
          flow_id_customer=row['flow_id_customer'],
          order_value=float(row['order_value'])
      ) for row in rows]  # type: ignore
    except Exception as error:
      print(f'Error loading connections from CSV: {error}')
      return []
