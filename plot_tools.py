import numpy as np
import pandas as pd

from plotly import graph_objects as go
from plotly.colors import get_colorscale

from preprocess import compute_firing_rate_map, AXES, POOL_SIZE, VOXEL_SIZE


FIG_LAYOUT = dict(
    width=1200,
    height=500,
    scene=dict(aspectmode="manual", aspectratio=dict(x=2, y=1, z=0.3)),
    scene_xaxis_showticklabels=True,
    scene_yaxis_showticklabels=True,
    scene_zaxis_showticklabels=True,
    margin=dict(t=0, b=0, l=0, r=0),
)
COLORSCALE = [*get_colorscale("Viridis")[:-1], [1.0, "rgba(255, 255, 255, 0)"]]
X, Y, Z = np.mgrid[[slice(None, POOL_SIZE[ax] // VOXEL_SIZE - 1) for ax in AXES]] * 10


def construct_movement_trace(behav: pd.DataFrame, sfreq: int = 1000) -> dict:
    """Downsamples the given behavioral data and constructs a 3D plotly scatter trace."""
    sampling_times = np.arange(0, behav.shape[0], sfreq)
    pos_dict = {ax: behav.loc[sampling_times, f"{ax}_position"].values for ax in AXES}
    line_style = dict(color="black", width=0.5)

    return dict(type="scatter3d", mode="lines", line=line_style, **pos_dict)


def construct_firing_heatmap(
    behav: pd.DataFrame, spikes: pd.DataFrame, neuron: str,
) -> go.Figure:
    """Creates a 3D heatmap based on the firing times of the given neuron."""
    firing_rate_map = compute_firing_rate_map(behav, spikes, neuron)
    return go.Figure(
        data=[
            dict(
                type="volume",
                x=X.flatten(),
                y=Y.flatten(),
                z=Z.flatten(),
                value=firing_rate_map.values.flatten(),
                colorscale=COLORSCALE,
                reversescale=True,
                isomin=0,
                isomax=1,
                surface_count=25,
                opacity=0.5,
                hovertemplate="x: %{x}, y: %{y}, z: %{z}",
            )
        ],
        layout=FIG_LAYOUT,
    )
