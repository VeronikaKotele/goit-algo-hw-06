import csv
from .types import Company, Connection, Transaction

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
      return load_rows_from_csv(csv_path)  # type: ignore
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
      return load_rows_from_csv(csv_path)  # type: ignore
    except Exception as error:
      print(f'Error loading connections from CSV: {error}')
      return []


def csv_row_to_transaction(row: dict):
  """
  Converts a CSV row to a Transaction object
  
  Args:
    row: dict representing a CSV row
      
  Returns:
    Updated in-place dict representing a Transaction object
  """
  row['Order_qty'] = int(float(row['Order_qty'])) if row['Order_qty'] else 0
  row['Actual_qty'] = int(float(row['Actual_qty'])) if row['Actual_qty'] else 0
  row['Order_value_COM'] = int(float(row['Order_value_COM'])) if row['Order_value_COM'] else 0
  row['Actual_value_COM'] = int(float(row['Actual_value_COM'])) if row['Actual_value_COM'] else 0
  row['Order_value_Sell'] = int(float(row['Order_value_Sell'])) if row['Order_value_Sell'] else 0
  row['Actual_value_Sell'] = int(float(row['Actual_value_Sell'])) if row['Actual_value_Sell'] else 0


def load_transactions(csv_path: str) -> list[Transaction]:
    """
    Loads transactions from CSV file
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        List of Transaction objects
    """
    try:
      return load_rows_from_csv(csv_path, transform=csv_row_to_transaction)  # type: ignore
    except Exception as error:
      print(f'Error loading connections from CSV: {error}')
      return []
