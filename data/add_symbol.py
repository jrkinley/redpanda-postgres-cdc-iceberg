import os
import sys
import pandas as pd
from pandas import DataFrame


def get_symbol(name):
    """Returns 'META' from 'MSFT_historical_max.csv'."""
    parts = name.split("_")
    symbol = ""
    if len(parts) == 3:
        symbol = parts[0]
    return symbol


def add_symbol(path: str):
    name = os.path.basename(path)
    symbol = get_symbol(name)
    print(f'Adding "{symbol}" column to file {name}.')
    quotes_pd: DataFrame = pd.read_csv(path)
    if "Symbol" in list(quotes_pd):
        print("Symbol column already exists.")
        return
    quotes_pd.insert(0, "Symbol", symbol)
    print(quotes_pd.head())
    quotes_pd.to_csv(path, index=False)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Enter path to Nasdaq historical quotes file!")
        sys.exit(1)
    path = sys.argv[1]
    add_symbol(path)
