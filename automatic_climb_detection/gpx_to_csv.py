import glob
import os

import fire
import gpx_converter
import pandas as pd
from geopy.distance import great_circle

from automatic_climb_detection import logger


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


def gpx_to_csv_file(input: str, output: str | None = None) -> None:
    """Convert a gpx file to a csv file, optionally computing the distance field."""
    # Parse using gpx_converter
    try:
        df = gpx_converter.Converter(input_file=input).gpx_to_dataframe()
    except Exception as e:
        logger.error(f"Could not convert gpx file {input} to dataframe: {e}")
        return

    # Compute distance field from lat lon if not in data.
    try:
        columns = df.columns
        if (
            "distance" not in columns
            and "latitude" in columns
            and "longitude" in columns
        ):
            df = compute_distance(df)
    except Exception as e:
        logger.warning(f"Could not compute distance field for gpx file {input}: {e}")

    # Save
    if output is None:
        output = os.path.splitext(input)[0] + ".csv"
    df.to_csv(output)


def gpx_to_csv(input: str, output: str | None = None) -> None:
    if os.path.isfile(input):
        gpx_to_csv_file(input, output)
    elif os.path.isdir(input) and output is None:
        gpx_files = glob.glob(os.path.join(input, "*.gpx"))
        for gpx_file in gpx_files:
            gpx_to_csv_file(input=gpx_file)
    else:
        logger.warning("Did not provide filename or foldername.")


if __name__ == "__main__":
    fire.Fire(gpx_to_csv)
