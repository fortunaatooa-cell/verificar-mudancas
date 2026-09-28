from pathlib import Path
import pandas as pd

path = Path(__file__).with_name('sample.parquet')
pd.DataFrame({'id': [1, 2], 'name': ['alpha', 'beta']}).to_parquet(path, engine='pyarrow', index=False)
print(f'created {path.name}')
