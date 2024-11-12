# %%
import polars as pl
import duckdb
import requests

# %%
def get_drivers():
    # call the f1openapi and get session data
    response = requests.get("https://api.openf1.org/v1/drivers")
    data = response.json()
    drivers = []

    for session in data:
        # Convert points to a list of dictionaries
        drivers.append(
            {
                "driver_number": session["driver_number"],
                "broadcast_name": session["broadcast_name"],
                "full_name": session["full_name"],
                "name_acronym": session["name_acronym"],
                "team_name": session["team_name"],
                "team_colour": session["team_colour"],
                "first_name": session["first_name"],
                "last_name": session["last_name"],
                "headshot_url": session["headshot_url"],
                "country_code": session["country_code"],
                "session_key": session["session_key"],
                "meeting_key": session["meeting_key"],
            }
        )

    # Create a Polars DataFrame
    df = pl.DataFrame(drivers)

    # Write the DataFrame to a DuckDB database
    import os

    os.makedirs("data", exist_ok=True)

    con = duckdb.connect("data/f1_data.duckdb")
    con.execute("CREATE TABLE drivers AS SELECT * FROM df")
    con.close()

# %%
data = get_drivers()

# %%

with duckdb.connect("data/f1_data.duckdb") as con:
    df = con.execute("SELECT * FROM f1_data.drivers").pl()
    print(df.head(10, truncate=False))

# %%
