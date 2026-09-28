from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import platform
import sys
import pandas as pd
import pyarrow

path = Path(__file__).with_name('sample.parquet')
df = pd.read_parquet(path)
assert list(df['id']) == [1, 2]
assert list(df['name']) == ['alpha', 'beta']

instant = datetime(2026, 9, 28, 2, 30, tzinfo=timezone.utc)
local = instant.astimezone(ZoneInfo('America/Sao_Paulo'))
assert instant.date().isoformat() == '2026-09-28'
assert local.date().isoformat() == '2026-09-27'

print('python:', sys.version.split()[0], 'machine:', platform.machine())
print('pandas:', pd.__version__, 'pyarrow:', pyarrow.__version__)
print('utc date:', instant.date(), 'sao-paulo date:', local.date())
print('read_parquet OK with compatible engine')
