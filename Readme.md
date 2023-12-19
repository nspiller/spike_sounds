# Spike sounds
Convert neuronal activity to music.

This project is a workflow to convert time events,
such as spike times from electrophysiology recordings,
to sound files.

The input can be, for example, spike times for some neurons, 
but can be any time events.
The direct output is a MIDI file, 
that can be used to drive a, for example, a synthesizer
or a virtual instrument, to create an audio file.
MIDI is a standard widely used in music synthesis.
We include instructions on how to convert the MIDI file
to a WAV audio file using a SoundFont.
Furthermore, 
an MP4 video file is created to visualize the time events in the
audio file as temporal raster plots (eventplot).
Finally,
the audio and video files are merged into a single MP4 file. 

<!-- TODO instert link to example -->

# Installation
The code is designed to be installed via a conda environment, 
so you need 
[miniforge](https://github.com/conda-forge/miniforge) or
[anaconda](https://www.anaconda.com/download).
```
git clone https://github.com/nspiller/spike_sounds
cd spike_sounds
conda create -n midi environment.yml
conda activate midi
pip install -e .
```
If [git](https://git-scm.com/) is not available on your system,
you can also manually download this repository.

# How to use
Some examples are given in `scripts/write_midi.py`.
This python script file can be run cell-by-cell with a suitable code editor.
The script file was created with 
[jupytext](https://jupytext.readthedocs.io/en/latest/),
which allows you to convert between script file `.py` and jupyter notebook file `.ipynb`. 
We recommend [this vscode extension](https://github.com/congyiwu/vscode-jupytext)
for the conversion.


## MIDI file
The output is a MIDI file generated with the python library [mido](https://mido.readthedocs.io/).
Those files can be read by, for example, `fluidsynth`,
which will play a sound whenever a spike occurs. 
An online serach for _digital audio workstations_ will yield many options for 
more powerful software that can convert MIDI signals into sounds. 
Note that some online MIDI players, such as [this one](https://signal.vercel.app/),
cannot handle high event densities and merge events that are too close together.

The resulting MIDI file can include the spike times for many neurons.
In this case, the spike times for each neurons will create a different
MIDI note.
It is also possible to include other time events and play them on a different
intrument.

## MIDI to WAV with `fluidsynth`
Here, we give an example how to generate an audio files from a MIDI file
using a sample-based soundfont and `fluidsynth`.
Requirements:
- [fluidsynth](https://www.fluidsynth.org/)
- [SoundFont file](https://member.keymusician.com/Member/FluidR3_GM/index.html)

Since the instructions are written for Linux,
it is recommended to install `fluidsynth` via WSL on Windows.
Soundfont files are available online,
e.g. `FluidR3_GM.sf2`,
or may be already avaible on your machine,
e.g. `/usr/share/sounds/sf2/FluidR3_GM.sf2`.
Note that the path may be different on your system.

The following command converts `example.mid` to `example.wav`
```
fluidsynth -a alsa -m alsa_seq -l -i /path/to/soundfont.sf2 example.mid -F example.wav
```

The example workflow in `scripts/write_midi.py` explains how to select 
different instruments.
As an example, the instruments available in `FluidR3_GM.sf2`
are stored in `instruments_FluidR3_GM`.
Run, for example, `echo "inst 1" |  fluidsynth /usr/share/sounds/sf2/FluidR3_GM.sf2`
to get this list.



## Merge audio and video


To combine video and audio track, run
```
ffmpeg -i example.mp4 -i example.wav -c:v copy -c:a aac combined.mp4
```





