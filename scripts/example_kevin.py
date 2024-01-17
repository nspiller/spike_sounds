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

from src import data_handling, visualize, midi_handling

# %%
basename = '../data/testing/for_kevin/example_a'

# load data from matlab file
data = data_handling.load_matlab(
    '../data/matlab/SM117_20220803_g0_JRC_units_probe1_continous.mat',
    rate_range=(0, None),
    time_interval=(3555.7 - 1, 3555.7 - 1 + 20 ))

data_handling.write_data(data, basename + '.pickle')

# %%
# plot data
plot_params = {
    'figsize' : (10, 5),
    'linewidth' : .5,
    'linelengths' : .9,
}

fig, ax = visualize.plot_data(data, key_vlines=['lick', 'onset'], **plot_params)
# fig.savefig('tmp.png')

# %%
# select only spike data
data_spikes = { k: v for k, v in data.items() if k.startswith("unit") }

# generate MIDI data and write MIDI file
tracks = midi_handling.generate_tracks(
    data_spikes.values(), channel=0, root_note=36, program=0, velocity=127,
)
midi_handling.tracks2midi(tracks, path=basename + '.mid')

# %%
# plot
plot_params = {
    'figsize' : (10, 5),
    'linewidth' : .5,
    'linelengths' : .9,
    'matplotlib_style': 'dark_background',
}

# # generate movies
# visualize.generate_movie(
#     data_spikes,
#     time_resolution=0.03,
#     plot_params=plot_params,
#     path_movie=basename + '_dark.mp4',
#     n_jobs=1
# )

plot_params['matplotlib_style'] = 'default'
visualize.generate_movie(
    data_spikes,
    time_resolution=0.03,
    plot_params=plot_params,
    path_movie=basename + '_light.mp4',
    n_jobs=1
)

# %%
