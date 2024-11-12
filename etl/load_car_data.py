# %%
from csv import DictReader
import reactivex as rx
from reactivex import operators as ops
import requests
import os

from influxdb_client import Point, InfluxDBClient, WriteOptions

from openf1.api import CarData, OpenF1API

import polars as pl
import duckdb

# %%
# get driver and session from duckdb
con = duckdb.connect(database="data/f1_data.duckdb")
sessions = con.sql(
    """
                   SELECT * FROM sessions 
                   WHERE session_type='Race'"""
).pl()
sessions = sessions.with_columns(pl.col("date_start").str.to_datetime()).with_columns(
    pl.col("date_end").str.to_datetime()
)

# %%
lastest_session = sessions.filter(pl.col("session_key") == 9635).to_dict(
    as_series=False
)
print(lastest_session)

# %%
openf1 = OpenF1API()

# %%
drivers = openf1.get_drivers(lastest_session["session_key"][0])

driver = drivers
driver = next(driver for driver in drivers if driver.last_name == "Alonso")
print(driver)

# %%
openf1 = OpenF1API()

car_data = openf1.get_car_data(
    driver_number=driver.driver_number, session_key=lastest_session["session_key"][0]
)

# %%%
with InfluxDBClient(
    url="http://127.0.0.1:58885",
    token=os.getenv("INFLUDXDB_F1_DATA_TOKEN"),
    org="influxdata",
    debug=True,
) as client:

    """
    Create client that writes data in batches with 50_000 items.
    """
    with client.write_api(
        write_options=WriteOptions(batch_size=500, flush_interval=500)
    ) as write_api:

        """
        Write data into InfluxDB
        """
        write_api.write(
            bucket="f1_data",
            record=[measurement.to_influxdb_point() for measurement in car_data],
        )

# %%
