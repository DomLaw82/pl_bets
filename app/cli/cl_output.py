from tabulate import tabulate
import sys

CURSOR_UP_ONE = '\x1b[1A' 
ERASE_LINE = '\x1b[2K'

intro = """
==================================
    Welcome to the pl_stats db
==================================
"""
main_menu = """
=============
  Main Menu
=============

1: Add match
2: Add game Performance
3: Add player
4: Add team
5: Add country
6: Add competition
7: Ingest squad data
8: Ingest team and match data
9: Exit

Select an option: """

def print_dict_table(data):
  if not isinstance(data, dict):
      print("Input data is not a dictionary.")
      return

  rows = []
  headers = set()
  
  # Flatten the nested dictionaries and collect unique keys
  for key, nested_dict in data.items():
      row = {"Key": key}
      for nested_key, nested_value in nested_dict.items():
          row[nested_key] = nested_value
          headers.add(nested_key)
      rows.append(row)
  
  headers = list(["Key"] + sorted(headers))  # Include "Key" column and sort headers

  # Convert rows to a list of dictionaries
  table = [[row.get(header, "") for header in headers] for row in rows]

  # Print the table
  print(tabulate(table, headers = headers, tablefmt="grid"))


def delete_last_lines(n=1): 
  for _ in range(n): 
    sys.stdout.write(CURSOR_UP_ONE) 
    sys.stdout.write(ERASE_LINE) 