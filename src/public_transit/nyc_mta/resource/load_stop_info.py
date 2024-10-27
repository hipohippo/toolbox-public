import pandas as pd
from pathlib import Path


def load_stop_info():
    return pd.read_csv(Path(__file__).parent / "stops.csv")
