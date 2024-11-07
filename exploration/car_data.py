# %%
from urllib.request import urlopen
import json
import polars as pl

response = urlopen('https://api.openf1.org/v1/car_data?driver_number=55&session_key=9159&speed>=315')
data = json.loads(response.read().decode('utf-8'))

# Convert the data to a Polars DataFrame
df = pl.DataFrame(data)
df

# %%
df = df.with_columns(pl.col("date").str.to_datetime())

# %%
response = urlopen('https://api.openf1.org/v1/car_data')
data = json.loads(response.read().decode('utf-8'))


# %%
