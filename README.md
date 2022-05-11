# place_cell_explorer

<img src="https://i.pinimg.com/originals/c1/74/41/c174418986a7ac6636cc9635b56b7cc3.gif" width=200>

This repository contains a small dash app for browsing data from an invasive place cell study, in which subjects navigated in a virtual pool, while their neural activity was recorded via surgically implanted microelectrodes.

The dashboard allows the user to choose from a dropdown list of neurons, and displays a 3-dimensional firing rate map of the selected neuron, along with the movement trajectory of the subject during the game. Based on the firing rate heatmap, the user can observe the spatial tuning of individual cells. (In order not to convey too much information - as this is part of an ongoing research - neurons are identified with randomly assigned adjectives, and their firing rates are normalized to 1.)

Usage:

`pip install -r requirements.txt`

`python app.py`
