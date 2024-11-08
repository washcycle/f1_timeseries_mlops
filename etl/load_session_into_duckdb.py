# %%
import polars as pl
import duckdb
import requests

# %%
def get_sessions():
    # call the f1openapi and get session data
    response = requests.get("https://api.openf1.org/v1/sessions")
    data = response.json()
    sessions = []

    for session in data:
        # Convert points to a list of dictionaries
        sessions.append(
            {
                "location": session["location"],
                "country_code": session["country_code"],
                "circuit_short_name": session["circuit_short_name"],
                "session_type": session["session_type"],
                "session_name": session["session_name"],
                "date_end": session["date_end"],
                "date_start": session["date_start"],
                "gmt_offset": session["gmt_offset"],
                "session_key": session["session_key"],
                "meeting_key": session["meeting_key"],
                "year": session["year"],                
            }
        )

    # Create a Polars DataFrame
    df = pl.DataFrame(sessions)

    # Write the DataFrame to a DuckDB database
    import os
    os.makedirs("data", exist_ok=True)
    
    con = duckdb.connect(
        "data/f1_data.duckdb"
    )
    con.execute("CREATE TABLE sessions AS SELECT * FROM df")
    con.close()


# %%
data = get_sessions()


# %%

with duckdb.connect("data/f1_data.duckdb") as con:
    df = con.execute("SELECT * FROM f1_data.sessions").pl()
    print(df.head(10))
# %%
