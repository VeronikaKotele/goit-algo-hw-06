import csv

def reduce_rows(transactions: list, 
                filter: callable,
                limit_unique_combinations: int, 
                combo_fn: callable) -> list:
  unique_combinations_times = dict() # set of unique flow_id combinations to amount of times seen
  reduced_transactions = []
  for t in transactions:
    if filter(t):
      continue
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

def write_reduced_transactions_to_csv(transactions: list, csv_path: str) -> list:
  reduced_rows = reduce_rows(transactions, 
                             filter=lambda x: not x['flow_id_supplier'] or not x['flow_id_internal'] or not x['flow_id_customer'],
                             limit_unique_combinations=5, combo_fn=lambda x: (x['flow_id_supplier'], x['flow_id_internal'], x['flow_id_customer']))
  path = csv_path.replace('.csv', '_reduced.csv')
  with open(path, 'w', newline='', encoding='utf-8') as file:
      fieldnames = ['product_name', 'product_category', 'flow_id_supplier', 'flow_id_internal', 'flow_id_customer', 'order_value']
      writer = csv.DictWriter(file, fieldnames=fieldnames)
      writer.writeheader()
      for row in reduced_rows:
        writer.writerow(row)

  return reduced_rows