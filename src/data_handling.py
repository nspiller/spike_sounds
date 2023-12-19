import numpy as np
from scipy.io import loadmat
import pickle


def write_data(dictionary, path):
    with open(path, mode="wb") as f:
        pickle.dump(dictionary, f)


def read_data(path):
    with open(path, mode="rb") as f:
        dictionary = pickle.load(f)
    return dictionary


def load_matlab(p_mat, time_interval=(0, 10), rate_range=(0, None), sort_rate=True):
    # unpack thresholds
    t_min, t_max = time_interval
    dt = t_max - t_min  # duration
    r_min, r_max = rate_range
    if r_max is None:
        r_max = np.inf
    n_min, n_max = r_min * dt, r_max * dt  # number of spikes

    # initialize data dict
    data = dict()

    mat = loadmat(p_mat, simplify_cells=True)

    # relevant columns in matlab file
    trial_info = mat["trial_info"]
    t_onset = trial_info["trialOnsetInSec"]
    t_lick = trial_info["First_lick"] + t_onset

    # trial onsets
    m = np.where((t_min < t_onset) & (t_onset < t_max))
    t_onset = t_onset[m]
    data["onset"] = t_onset - t_min

    # first lick per trial
    m = np.where((t_min < t_lick) & (t_lick < t_max))
    t_lick = t_lick[m]
    data["lick"] = t_lick - t_min

    # iterate over units
    units, spikes = [], []
    for i, u in enumerate(mat["unit"]):
        t_spk = u["SpikeTimesInSec"]
        m = (t_spk > t_min) & (t_spk < t_max)
        t_spk = t_spk[m]
        if n_min < len(t_spk) < n_max:
            units.append(f"unit_{i+1}") # units start with 1
            spikes.append(t_spk - t_min)

    if sort_rate: # sort units by firing rate
        n_spikes = [len(s) for s in spikes]
        idx = np.argsort(n_spikes)[::-1]
        units = [units[i] for i in idx]
        spikes = [spikes[i] for i in idx]

    for u, s in zip(units, spikes):
        data[u] = s

    return data
