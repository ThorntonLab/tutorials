import sqlite3
import pandas as pd
from collections import namedtuple

Datum = namedtuple('Datum', ['x', 'y'])

data = [Datum(1, i) for i in range(10)]
data.extend([Datum(2, i*i) for i in range(11, 21)])

df = pd.DataFrame(data, columns=Datum._fields)

with sqlite3.connect("test.db") as conn:
    df.to_sql('data', conn, if_exists='replace',index=False)
