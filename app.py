import dash
import numpy as np
import pandas as pd

from dash import dcc, html
from dash.dependencies import Input, Output
from itertools import product
from plotly import graph_objects as go
from plotly.colors import get_colorscale


# read behavioral data and construct movement trace

axes = ["x", "y", "z"]
behav = pd.read_parquet("app_data/behav_sim.parquet").set_index("msec")
sampling_times = np.arange(0, behav.shape[0], 1000)
pos_dict = {ax: behav.loc[sampling_times, f"{ax}_position"].values for ax in axes}
line_style = dict(color="black", width=0.5)
movement_trace = dict(type="scatter3d", mode="lines", line=line_style, **pos_dict)


# read neural data and create dropdown

spikes = pd.read_parquet("app_data/spikes_sim.parquet").set_index("msec")
neurons = spikes["neuron"].value_counts().index.tolist()
neuron_dropdown = dcc.Dropdown(
    id="neuron_dd",
    options=[dict(label=neuron, value=neuron) for neuron in neurons],
    value=neurons[0],
    style=dict(fontsize=20, width=500, marginTop=20),
)


# compute firing rate map


def spatial_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Constructs a pivot table containing the number of milliseconds in each voxel."""
    return df.pivot_table(
        index=bin_cols[0], columns=bin_cols[1:], values="msec", aggfunc="count"
    )


bin_cols = [f"{ax}_bin" for ax in axes]
pool_size = {"x": 360, "y": 180, "z": 70}
voxel_size = 10
bins_by_ax = [np.arange(0, pool_size[ax], voxel_size) for ax in axes]
voxels = (
    pd.DataFrame(product(*bins_by_ax), columns=bin_cols)
    .assign(msec=1)
    .pipe(spatial_pivot)
)
X, Y, Z = np.mgrid[[slice(None, pool_size[ax] // voxel_size - 1) for ax in axes]] * 10


def compute_firing_rate_map(neuron: str) -> pd.DataFrame:
    """Computes the firing rate of the given neuron for all voxels."""
    spikes_per_nonempy_voxel = (
        behav.join(spikes.loc[lambda df: df["neuron"] == neuron], how="inner")
        .reset_index()
        .groupby(bin_cols)["msec"]
        .count()
        .reset_index()
        .pipe(spatial_pivot)
    )

    return (
        (spikes_per_nonempy_voxel * voxels)
        .fillna(0)
        .pipe(lambda df: df / df.max().max())
    )


# define heatmap

fig_layout = dict(
    width=1200,
    height=500,
    scene=dict(aspectmode="manual", aspectratio=dict(x=2, y=1, z=0.3)),
    scene_xaxis_showticklabels=True,
    scene_yaxis_showticklabels=True,
    scene_zaxis_showticklabels=True,
    margin=dict(t=0, b=0, l=0, r=0),
)

colorscale = get_colorscale("Viridis")[:-1] + [[1.0, "rgba(255, 255, 255, 0)"]]


def firing_heatmap(neuron: str) -> go.Figure:
    """Creates a 3D heatmap based on the firing times of the given neuron."""
    firing_rate_map = compute_firing_rate_map(neuron)
    return go.Figure(
        data=[
            dict(
                type="volume",
                x=X.flatten(),
                y=Y.flatten(),
                z=Z.flatten(),
                value=firing_rate_map.values.flatten(),
                colorscale=colorscale,
                reversescale=True,
                isomin=0,
                isomax=1,
                surface_count=25,
                opacity=0.5,
                hovertemplate="x: %{x}, y: %{y}, z: %{z}",
            ),
            movement_trace,
        ],
        layout=fig_layout,
    )


# define app layout

app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://codepen.io/chriddyp/pen/bWLwgP.css",
        "https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css",
    ],
    external_scripts=[
        "https://code.jquery.com/jquery-3.5.1.slim.min.js",
        "https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js",
    ],
    suppress_callback_exceptions=True,
)

app.layout = html.Div(
    children=[
        html.H1("Firing rate heatmap"),
        html.Div(
            children=[html.H3("select neuron below"), neuron_dropdown],
            style=dict(marginTop=20),
        ),
        html.Div(id="fig"),
    ],
    style=dict(marginTop=50, marginLeft=100, marginRight=100, marginBottom=50),
)

# define callback


@app.callback(Output("fig", "children"), [Input("neuron_dd", "value")])
def show_heatmap(neuron: str) -> dcc.Graph:
    """Shows the firing rate heatmap of the selected neuron."""
    return dcc.Graph(figure=firing_heatmap(neuron))


# run app

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
