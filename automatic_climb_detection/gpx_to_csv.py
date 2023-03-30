import os

import fire
import gpx_converter
import pandas as pd
from geopy.distance import great_circle


def compute_distance(df: pd.DataFrame) -> pd.DataFrame:
    """Compute the great circle distance using the lat/lon columns in the dataframe."""
    distances = [0.0]
    last_point = (df["latitude"][0], df["longitude"][0])
    for _, row in df[1:].iterrows():
        this_point = (row["latitude"], row["longitude"])
        distances.append(distances[-1] + great_circle(last_point, this_point).meters)
        last_point = this_point
    df["distances"] = distances
    return df


def gpx_to_csv(input: str, output: str | None = None) -> None:
    """Convert a gpx file to a csv file, optionally computing the distance field."""
    df = gpx_converter.Converter(input_file=input).gpx_to_dataframe()

    # Compute distance field from lat lon if not in data.
    columns = df.columns
    if "distance" not in columns and "latitude" in columns and "longitude" in columns:
        df = compute_distance(df)

    if output is None:
        output = os.path.splitext(input)[0] + ".csv"

    df.to_csv(output)


if __name__ == "__main__":
    fire.Fire(gpx_to_csv)
