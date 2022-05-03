import dash

from dash import dcc, html
from dash.dependencies import Input, Output

from load_data import read_parquet_from_bucket
from plot_tools import construct_movement_trace, construct_firing_heatmap


# read data and construct static elements

behav = read_parquet_from_bucket("behav").set_index("msec")
movement_trace = construct_movement_trace(behav)
spikes = read_parquet_from_bucket("spikes").set_index("msec")
neurons = spikes["neuron"].sort_values().unique()
neuron_dropdown = dcc.Dropdown(
    id="neuron_dd",
    options=[dict(label=neuron, value=neuron) for neuron in neurons],
    value=neurons[0],
    style=dict(fontsize=20, width=500, marginTop=20),
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
    style=dict(marginTop=50, marginBottom=50, marginLeft=100, marginRight=100),
)

# define callback


@app.callback(Output("fig", "children"), [Input("neuron_dd", "value")])
def show_heatmap(neuron: str) -> dcc.Graph:
    """Shows the firing rate heatmap of the selected neuron."""
    heatmap = construct_firing_heatmap(behav, spikes, neuron)
    return dcc.Graph(figure=heatmap.add_trace(movement_trace))


# run app

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
