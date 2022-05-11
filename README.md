# place_cell_explorer

<img align="left" width=200 src="https://i.pinimg.com/originals/c1/74/41/c174418986a7ac6636cc9635b56b7cc3.gif">

This repository contains a small dash app for browsing data from an invasive place cell study, in which subjects navigated in a virtual pool, while their neural activity was recorded via surgically implanted microelectrodes.

The dashboard allows the user to choose from a dropdown list of neurons, and displays a 3-dimensional firing rate map of the selected neuron, along with the movement trajectory of the subject during the game. Based on the firing rate heatmap, the user can observe the spatial tuning of individual cells[^*].

## Usage

### Data structure and access

The data originally used in this project is not public. To operate the app using your own data, you need to upload it to an s3 bucket and set the corresponding environment variables:
* `AWS_BUCKET`
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`

The app assumes the following data structure:

* a `behav.parquet` file containing behavioral records

|    |        msec |   x_position |   y_position |   z_position |   x_bin |   y_bin |   z_bin |
|---:|------------:|-------------:|-------------:|-------------:|--------:|--------:|--------:|
|  0 | 1.1391e+06  |      240.629 |      18.6601 |      16.9011 |     240 |      10 |      10 |
|  1 | 1.4897e+06  |      343.76  |      38.9883 |      27.8938 |     340 |      30 |      20 |
|  2 | 1.78567e+06 |      323.788 |      25.6903 |      35.292  |     320 |      20 |      30 |

* a `spikes.parquet` file containing the results of spike sorting

|    | neuron             |    msec |
|---:|:-------------------|--------:|
|  0 | melancholic neuron | 1347444 |
|  1 | cloudy neuron      |  750765 |
|  2 | wicked neuron      | 1293642 |

You may have to modify additional global variables in `preprocess.py` and `plot_tools.py` to accomodate the app to the specifics of your data.

### Running the app

`pip install -r requirements.txt`

`python app.py`


[^*]: In order not to convey too much information - as this is part of an ongoing research - neurons are identified with randomly assigned adjectives, and their firing rates are normalized to 1.
