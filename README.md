# place_cell_explorer

<img align="left" width=200 src="https://i.pinimg.com/originals/c1/74/41/c174418986a7ac6636cc9635b56b7cc3.gif">

This repository contains a small dash app for browsing data from an invasive place cell study, in which subjects navigated in a virtual pool, while their neural activity was recorded via surgically implanted microelectrodes.

The dashboard allows the user to choose from a dropdown list of neurons, and displays a 3-dimensional firing rate map of the selected neuron, along with the movement trajectory of the subject during the game. Based on the firing rate heatmap, the user can observe the spatial tuning of individual cells[^*].

## Usage

### Data

The data originally used in this project is not public. To operate the app using your own data, you need to upload it to an s3 bucket and set the corresponding environment variables:
* `AWS_BUCKET`
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`

The app assumes the following data structure:

* a `behav.parquet` file containing behavioral records

'|    |   msec |   x_position |   y_position |   z_position |   x_bin |   y_bin |   z_bin |\n|---:|-------:|-------------:|-------------:|-------------:|--------:|--------:|--------:|\n|  0 |      0 |          168 |      25.1336 |      51.9393 |     160 |      20 |      50 |\n|  1 |      1 |          168 |      25.1527 |      51.9307 |     160 |      20 |      50 |\n|  2 |      2 |          168 |      25.1718 |      51.922  |     160 |      20 |      50 |'

* a `spikes.parquet` file containing the results of spike sorting

'|    | neuron           |    msec |\n|---:|:-----------------|--------:|\n|  0 | vibrant neuron   | 1156811 |\n|  1 | cloudy neuron    |  357242 |\n|  2 | ambitious neuron | 1613955 |'

### Running the app

`pip install -r requirements.txt`

`python app.py`


[^*]: In order not to convey too much information - as this is part of an ongoing research - neurons are identified with randomly assigned adjectives, and their firing rates are normalized to 1.
