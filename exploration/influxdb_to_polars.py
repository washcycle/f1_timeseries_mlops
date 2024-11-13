# %%
import polars as pl
import influxdb_client
from influxdb_client import InfluxDBClient
import os

# %%
print(f"{'influxdb client version':<30} {influxdb_client.__version__ :<10}")
print(f"{'polars version':<30} {pl.__version__:<10}")

# %%
# InfluxDB connection

influx_db_client_config = {
    "bucket": "f1_data",
    "org": "influxdata",
    "token": os.getenv("INFLUDXDB_F1_DATA_TOKEN"),
    "url": "http://localhost:55737",
}

# %%

with InfluxDBClient(**influx_db_client_config, debug=False) as client:
    query = '''
    from(bucket:"f1_data")
        |> range(start: 2024-11-02T14:03:00Z, stop: 2024-11-02T14:40:00Z)
    '''
    result = pl.DataFrame(client.query_api().query_data_frame(query))
result

# %%
