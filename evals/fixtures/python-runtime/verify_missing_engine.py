from pathlib import Path
import pandas as pd

path = Path(__file__).with_name('sample.parquet')
try:
    pd.read_parquet(path)
except ImportError as exc:
    message = str(exc).lower()
    print(type(exc).__name__ + ': ' + str(exc))
    assert 'pyarrow' in message or 'fastparquet' in message
else:
    raise AssertionError('read_parquet deveria falhar sem pyarrow/fastparquet')
