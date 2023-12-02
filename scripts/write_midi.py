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
#     rate_range=(1, 100),
#     time_interval=(500, 520))
# data_handling.write_data(data, '../data/example.pickle')

# %%
# load example data
data = data_handling.read_data('../data/example.pickle')

# plot
visualize.plot_data(data, vline_keys=['lick', 'onset'])

# %%
# convert dictionary to list of lists of time events (order is reflected in MIDI file)
print('Data data to be written to MIDI file:')
print(*data.keys())
l_time_events = [ *data.values() ]

# %% [markdown]
# # create MIDI file

# %%
# write to file
midi_handling.times2midi(
    l_time_events,                      # actual data
    bpm=120, ticks_per_beat=4800,       # time resolution settings
    note_duration=0.1,                  # in seconds
    root_note=36,                       # 60 is C4
    semitone_sequence=[0, 4, 7],        # 0-4-7 is a major chord, octaves (+12) are added automatically
                                        # note: max note is 127
    merge_tracks=True,                  # merge if you want to use multiple instruments
    path='../data/example.mid'          # if not set, return mido.MidiFile object
    )

# %% [markdown]
# # create video file

# %%
visualize.generate_movie(l_time_events, time_interval=(0, 20), time_resolution=.03, path_movie='../data/example.mp4')

# %%
