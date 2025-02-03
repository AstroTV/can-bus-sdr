import pandas as pd
import sys


if len(sys.argv) != 2 or not sys.argv[1].endswith(".csv"):
    print("Usage: python process_csv.py <example.csv>")
    exit(1)
filename = sys.argv[1]
ds = pd.read_csv(filename,delimiter=';')
print(ds)