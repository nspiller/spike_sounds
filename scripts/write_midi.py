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
# ## synthetic data
# This example shows the data structure: 
# A dictionary mapping some name to a list of time events.

# %%
# data structure with some data
data = {
    "C4": [0.125, 1.250],
    "E4": [0.250, 1.125],
    "G4": [0.375, 1.000],
    "C5": [0.500, 0.875],
}

# visualization as raster plot
fig, ax = visualize.plot_data(data)

# %% [markdown]
# ## Experimental spike data
# This data set contains spiking activity for multiple neurons,
# as well as the stimulus onset and the first lick of the animal.  

# %%
# load example data
data = data_handling.read_data('../data/example.pickle')

fig, ax = visualize.plot_data(data, key_vlines=['lick', 'onset'])

# %% [markdown]
# # Generate MIDI files
#
# MIDI files store musical information such as notes, tempo, and pitch.
# We can control if we want to send MIDI information on a single channel
# or on multiple channels.
# On a given channel, we can select a different note for each neuron.
# If using multiple channels, we can choose a different instrument for each channel.

# %% [markdown]
# ## Single channel
# Here, we choose only the spike events.
# All data is sent via the same MIDI channel, but each neuron is assigned a different note.
#
# To play a different set of notes, we can change the chord being played with the arguments
# `semitone_sequence` and `root_note` of the `generate_tracks` function.
#
# The `program` argument of the `generate_tracks` function allows us to choose a different instrument, 
# as defined in [instruments_FluidR3_GM](../instruments_FluidR3_GM).
# E.g. `program=46` selects a harp.

# %%
# select only spike data
data_spikes = { k: v for k, v in data.items() if k.startswith("unit") }

# generate MIDI data and write MIDI file
tracks = midi_handling.generate_tracks(
    data_spikes.values(), channel=0, root_note=36, program=25, velocity=127,
)
midi_handling.tracks2midi(tracks, path="../data/example_single.mid")

# %% [markdown]
# ## Multiple channels
# Here, we send spike, lick, and stimulus events on different MIDI channels.
# This allows us to select a different instrument for each event type
# using the `program` argument of the `generate_tracks` function.

# %%
# separate data
onsets = [data["onset"]]
licks = [data["lick"]]
spikes = [v for k, v in data.items() if k.startswith("unit")]

# generate separate tracks
tracks0 = midi_handling.generate_tracks(
    spikes, channel=0, root_note=36, program=46, velocity=64
)
tracks1 = midi_handling.generate_tracks(
    onsets, channel=1, root_note=48, program=47, velocity=127, note_duration=1
)
tracks2 = midi_handling.generate_tracks(
    licks, channel=2, root_note=72, program=68, velocity=127, note_duration=.750
)

# combine tracks and write MIDI file
all_tracks = tracks0 + tracks1 + tracks2
midi_handling.tracks2midi(all_tracks, path="../data/example_multi.mid")

# %% [markdown]
# # Create movie without sound
# We use the same data structure to create an MP4 movie file.
#
# Plots are created with matplotlib, which can be slow when generating many frames.
# Choose, for example, `time_resolution=.5` for testing.

# %%
# plot
plot_params = {
    'figsize' : (10, 5),
    'linewidth' : .5,
    'linelengths' : .9,
    'matplotlib_style': 'dark_background',
}

# generate movie
visualize.generate_movie(
    data,
    key_vlines=['lick', 'onset'],
    time_resolution=0.03,
    plot_params=plot_params,
    path_movie="../data/example_multi.mp4",
)

# %% [markdown]
# # Create movie with sound
#
# ## convert MIDI to audio
# The MIDI file can be converted to a WAV audio file using the `fluidsynth` command line tool,
# which is explained the README.
#
# ## merge MP4 and WAV
# The MP4 and WAV files can be merged using the `ffmpeg` command line tool,
# which is explained the README.
