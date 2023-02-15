import numpy as np
import pandas as pd

from itertools import product


AXES = ["x", "y", "z"]
POOL_SIZE = {"x": 360, "y": 180, "z": 70}
VOXEL_SIZE = 10
BIN_COLS = [f"{ax}_bin" for ax in AXES]


def to_spatial_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a pivot table containing the number of milliseconds spent in each voxel."""
    return df.pivot_table(
        index=BIN_COLS[0], columns=BIN_COLS[1:], values="msec", aggfunc="count"
    )


def compute_all_voxels(pool_size: dict, voxel_size: float) -> pd.DataFrame:
    """
    Returns an uninformative spatial pivot table containing all voxel boundaries
    as indices. This is necessary, because we have to provide data about all the
    voxels - even empty ones - in order to construct the firing rate heatmap.
    """
    bins_by_ax = [np.arange(0, pool_size[ax], voxel_size) for ax in AXES]
    return (
        pd.DataFrame(product(*bins_by_ax), columns=BIN_COLS)
        .assign(msec=1)
        .pipe(to_spatial_pivot)
    )


def compute_firing_rate_map(
    behav: pd.DataFrame, spikes: pd.DataFrame, neuron: str
) -> pd.DataFrame:
    """Computes the firing rate of the given neuron for all voxels."""
    spikes_per_nonempty_voxel = (
        behav.join(spikes.loc[lambda df: df["neuron"] == neuron], how="inner")
        .reset_index()
        .groupby(BIN_COLS)["msec"]
        .count()
        .reset_index()
        .pipe(to_spatial_pivot)
    )
    all_voxels = compute_all_voxels(POOL_SIZE, VOXEL_SIZE)

    return (
        (spikes_per_nonempty_voxel * all_voxels)
        .fillna(0)
        .pipe(lambda df: df / df.max().max())
    )
