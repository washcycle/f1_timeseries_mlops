# %%
from csv import DictReader
import reactivex as rx
from reactivex import operators as ops
import requests
import os

from influxdb_client import Point, InfluxDBClient, WriteOptions

# %%

data = get_sessions()

# %%%
with InfluxDBClient(
    url="http://192.168.49.2:30905",
    token=os.getenv("INFLUXDB_TOKEN"),
    org="influxdata",
    debug=True,
) as client:

    """
    Create client that writes data in batches with 50_000 items.
    """
    with client.write_api(
        write_options=WriteOptions(batch_size=50_000, flush_interval=10_000)
    ) as write_api:

        """
        Write data into InfluxDB
        """
        write_api.write(bucket="f1_data", record=data)
