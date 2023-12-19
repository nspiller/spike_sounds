# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: midi
#     language: python
#     name: python3
# ---

# %%
# %load_ext autoreload
# %autoreload 2

from src import data_handling, visualize

# %% [markdown]
# This example shows how to generate a data dictinoary from 
# the matlab data file used in some experiments.
# You can choose a `time_interval` in seconds 
# and only neurons a firing rate within `rate_range` in Hz.

# %%
# load data from matlab file
data = data_handling.load_matlab(
    '../data/matlab/SM117_20220803_g0_JRC_units_probe1_continous.mat',
    rate_range=(0, None),
    time_interval=(3555.7 - 1, 3566.2 + 7 ))

data_handling.write_data(data, '../data/example.pickle')

# %%
# plot data
plot_params = {
    'figsize' : (10, 5),
    'linewidth' : .5,
    'linelengths' : .9,
}

fig, ax = visualize.plot_data(data, key_vlines=['lick', 'onset'], **plot_params)
