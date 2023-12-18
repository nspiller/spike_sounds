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

from src import data_handling, midi_handling, visualize

# %% [markdown]
# # load and visualize data

# %%
# # optional: load data from matlab file
# data = data_handling.load_matlab(
#     '../data/matlab/SM117_20220803_g0_JRC_units_probe1_continous.mat',
#     rate_range=(0, None),
#     time_interval=(3555.7 - 1, 3566.2 + 7 ))
# data_handling.write_data(data, '../data/example.pickle')

# %%
# load example data
data = data_handling.read_data('../data/example.pickle')

# plot
plot_params = {
    'figsize' : (10, 5),
    'linewidth' : .5,
    'linelengths' : .9,
}

fig, ax = visualize.plot_data(data, key_vlines=['lick', 'onset'], **plot_params)

# %% [markdown]
# # Single channel

# %%
# select data
data_spikes = { k: v for k, v in data.items() if k.startswith("unit") }

# generate and save MIDI data
tracks = midi_handling.generate_tracks(
    data_spikes.values(), channel=0, root_note=36, program=25, velocity=127,
)
midi_handling.tracks2midi(tracks, path="../data/example1.mid")

# %%
# generate movie
visualize.generate_movie(
    data_spikes,
    time_resolution=0.03,
    matplotlib_style='dark_background',
    plot_params=plot_params,
    path_movie="../data/example1.mp4",
)

# %% [markdown]
# # Multiple channels

# %%
# spikes, onsets, and licks are send on separate midi channels
onsets = [data["onset"]]
licks = [data["lick"]]
spikes = [v for k, v in data.items() if k.startswith("unit")]

tracks0 = midi_handling.generate_tracks(# play spikes on channel 0 with program 25 ()
    spikes, channel=0, root_note=36, program=25, velocity=64
)
tracks1 = midi_handling.generate_tracks(
    onsets, channel=1, root_note=48, program=47, velocity=127, note_duration=1
)
tracks2 = midi_handling.generate_tracks(
    licks, channel=2, root_note=96, program=46, velocity=127, note_duration=1
)

all_tracks = tracks0 + tracks1 + tracks2
midi_handling.tracks2midi(all_tracks, path="../data/example2.mid")

# %%
# generate movie
visualize.generate_movie(
    spikes + onsets + licks,
    time_resolution=0.03,
    plot_params=plot_params,
    path_movie="../data/example2.mp4",
)
