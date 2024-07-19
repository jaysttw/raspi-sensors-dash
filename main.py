from dash import Dash, dcc, html
from data.BME680 import BME680Data

import datetime as dt
import polars as pl
import plotly.express as px

app = Dash()

db = "data.db"

data_obj = BME680Data(db)
df = data_obj.df

last_data_time = df["time"].max()

last_minute_time = df.select(
    pl.col("time").max() - dt.timedelta(minutes=1)
)

last_day_time = df.select(
    pl.col("time").max() - dt.timedelta(days=1)
)

last_minute_df = df.filter(
    pl.col("time") > last_minute_time
)

last_day_df = df.filter(
    pl.col("time") > last_day_time
)

def status_generator(df, metric, display_name, unit):
    child_string = f"Average {display_name} reading for last minute: {last_minute_df[metric].mean():.2f}{unit}"
    return html.Div(
        children=child_string,
        style={
            "textAlign": "center",
        }
    )

def figure_generator(df, metric):
    return px.line(df, x="time", y=metric,)

status_items = [
    ("temperature", "temperature", "ºC"),
    ("relative_humidity", "humidity", "%RH"),
    ("pressure", "pressure", "hPa"),
]

combined_status = html.Div(
    className="row",
    children=[status_generator(df, m, d, u) for (m,d,u) in status_items]
)

# temperature_graph = px.line(
#     last_day_df,
#     x="time",
#     y="temperature",
# )

combined_obj = html.Div(
    children=[
        dcc.Graph(
            figure=figure_generator(
                last_day_df, metric
            )
        ) for (metric, _, _) in status_items
    ],
)

title = html.H1(
    children="BME688 Dashboard",
    style={
        "textAlign": "center",
    }
)

last_updated = html.H2(
    children=f"Data last updated: {last_data_time}",
    style={
        "textAlign": "center",
    }
)

app.layout = [
    title,
    last_updated,
    combined_status,
    # temperature_status,
    # humidity_status,
    # pressure_status,
    combined_obj,
]

if __name__ == '__main__':
    app.run(debug=True)