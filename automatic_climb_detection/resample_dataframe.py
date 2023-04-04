import numpy as np
import polars as pl


def resample_dataframe(
    df: pl.DataFrame,
    interpolation_column: str,
    interpolation_step: float,
) -> pl.DataFrame:
    """Resamples a dataframe to obtain data at interpolation points.

    Parameters
    ----------
    df : pl.DataFrame
        The dataframe to interpolate.
    interpolation_column : str
        Which numeric column to use for the interpolation points.
    interpolation_step : float
        Steps for the newly create interpolation points

    Returns
    -------
    pl.DataFrame
        A dataframe with the same columns as the input dataframe and where
        `interpolation_column` is spaced as `interpolation_step` and all other
        data is interpolated onto that timeline.
    """
    interpolation_points = pl.DataFrame(
        {
            interpolation_column: np.arange(
                df.min()[0, interpolation_column],
                df.max()[0, interpolation_column],
                step=interpolation_step,
            )
        }
    )

    interpolated_df = interpolation_points.join(
        interpolation_points.join(df, on=[interpolation_column], how="outer")
        .sort(interpolation_column)
        .interpolate(),
        on=[interpolation_column],
        how="left",
    ).sort(interpolation_column)

    return interpolated_df


def resample_dataframe_grouped(
    df: pl.DataFrame,
    interpolation_column: str,
    interpolation_step: float,
    group_column: str,
) -> pl.DataFrame:
    """Groupwise resamples a dataframe to obtain data at interpolation points.

    Parameters
    ----------
    df : pl.DataFrame
        The dataframe to interpolate.
    interpolation_column : str
        Which numeric column to use for the interpolation points.
    interpolation_step : float
        Steps for the newly create interpolation points
    group_column:str
        The column over which to group

    Returns
    -------
    pl.DataFrame
        A dataframe with the same columns as the input dataframe and where
        `interpolation_column` is spaced as `interpolation_step` and all other
        data is interpolated onto that timeline.
    """
    return pl.concat(
        [
            resample_dataframe(
                groupdf,
                interpolation_column=interpolation_column,
                interpolation_step=interpolation_step,
            )
            for _, groupdf in df.groupby(group_column, maintain_order=True)
        ]
    )
