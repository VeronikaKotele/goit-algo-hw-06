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
      return [Connection(Flow_Id=row['Flow_Id'], Id_From=row['Id_From'], Id_To=row['Id_To']) for row in rows]  # type: ignore
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
  row['order_value'] = int(float(row['Actual_qty'])) if row['Actual_qty'] else 0
  del row['Actual_qty']
  # del row['Order_qty']
  # del row['Actual_qty']
  # del row['Order_value_COM']
  # del row['Actual_value_COM']
  # del row['Order_value_Sell']
  # del row['Actual_value_Sell']


def load_transactions(csv_path: str) -> list[Transaction]:
    """
    Loads transactions from CSV file
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        List of Transaction objects
    """
    #try:
    rows = load_rows_from_csv(csv_path, transform=csv_row_to_transaction)  # type: ignore
    reduced_rows = reduce_rows(rows, limit_unique_combinations=5, combo_fn=lambda x: (x['flow_id_supplier'], x['flow_id_internal'], x['flow_id_customer']))
    with open('data/reduced_transactions.csv', 'w', newline='', encoding='utf-8') as file:
      fieldnames = ['product_name', 'product_category', 'flow_id_supplier', 'flow_id_internal', 'flow_id_customer', 'order_value']
      writer = csv.DictWriter(file, fieldnames=fieldnames)
      writer.writeheader()
      for row in reduced_rows:
        writer.writerow(row)
    return reduced_rows  # type: ignore
    #except Exception as error:
    #  print(f'Error loading connections from CSV: {error}')
    #  return []

def reduce_rows(transactions: list, limit_unique_combinations: int, combo_fn: callable) -> list:
  unique_combinations_times = dict(tuple, int) # set of unique flow_id combinations to amount of times seen
  reduced_transactions = []
  for t in transactions:
    combo = combo_fn(t)
    times = unique_combinations_times.get(combo, 0)
    if not times:
      unique_combinations_times[combo] = 1
    else:
      times += 1
      unique_combinations_times[combo] = times
      if times < limit_unique_combinations:
        reduced_transactions.append(t)

  return reduced_transactions