# %%
from cProfile import label
from urllib.request import urlopen
import json
import polars as pl
import altair as alt

# %%
response = urlopen("https://api.openf1.org/v1/sessions")
data = json.loads(response.read().decode("utf-8"))

# Convert the data to a Polars DataFrame
df = pl.DataFrame(data)
df = (
    df.with_columns(pl.col("date_start").str.to_datetime())
    .with_columns(pl.col("date_end").str.to_datetime())
    .with_columns(pl.col("year").cast(pl.Int32))
)
df

# %% md Notes
# There are 217 unique session keys in the sessions data
unique_session_keys = df.n_unique("session_key")
print(f"There are {unique_session_keys} unique sessions keys")


unique_years = df.unique("year")
print(f"There are {unique_years} unique sessions keys")


# %%
(df.plot.bar(x="year", y="session_key"))

# %%
(
    alt.Chart(df)
    .mark_bar(tooltip=True)
    .encode(
        x="country_code",
        y=alt.Y("count(session_key):Q", title="Number of Sessions"),
        color=alt.Color("year:N"),  # Specify year as a nominal (discrete) field
    )    
    .properties(width=500)
    .configure_scale(zero=False)
)

# %%
