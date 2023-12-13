!!! work in progress !!!

# Installation
```
git clone https://github.com/nspiller/spike_sounds
cd spike_sounds
conda create -n midi environment.yml
conda activate midi
pip install -e .
```

# Usage
Run `scripts/write_midi.py` cell by cell (optional: convert to jupyter notebook with jupytext)


# Convert spike times to MIDI
This project is deisgned to convert spikes recorded in
neuroscience experiments to sounds.
However, the code works for any set of time events.


## File format
The output is a MIDI file.
Those files can be read by suitable software,
which will play a sound whenever a spike occurs. 
For example, [this free, online MIDI player](https://signal.vercel.app/) 
that can be used to play the MIDI files with vairous instruments.
An online serach for _digital audio workstations_ will yield many options for 
more powerful software that can convert MIDI signals into sounds. 

The resulting MIDI file can include the spike times for many neurons.
In this case, the spike times for each neurons will create a different
MIDI note.
Some of the things the user can control are:
- which note is played for which neuron
- whether or not to have one track for all neurons or separate tracks
- the MIDI channel for each neuron.


# sound creation
MIDI signals can be converted in a multitude of ways.
For example, they can be used to trigger audio samples or
trigger a synthesizer.

For testing, https://www.zamzar.com/ allows for one free conversion from 
MIDI to WAV per day.
It is not recommended to use https://signal.vercel.app, because it cannot handle
high event densities.

To have more control over the sounds generated,
we are giving an example below
on how to generate an audio files from a MIDI file using a sample-based soundfont and `fluidsynth`.

## MIDI to WAV with `fluidsynth`
Requirements:
- [fluidsynth](https://www.fluidsynth.org/)
- [soundfont file](https://member.keymusician.com/Member/FluidR3_GM/index.html)

Since the instructions are written for Linux,
it is recommended to install `fluidsynth` via WSL on Windows.
Soundfont files are available online,
e.g. `FluidR3_GM.sf2`,
or may be already avaible on your machine,
e.g. `/usr/share/sounds/sf2/FluidR3_GM.sf2`.


The following command converts `example.mid` to `example.wav`
```
fluidsynth -a alsa -m alsa_seq -l -i /path/to/soundfont.sf2 example.mid -F example.wav
```
Note that you have set the correct path to the soundfont file.


To select a different instrument, set `program`  in `times2midi`.
As an example, the instruments available in `FluidR3_GM.sf2`
are stored in `instruments_FluidR3_GM`.
Run, for example, `echo "inst 1" |  fluidsynth /usr/share/sounds/sf2/FluidR3_GM.sf2`
to get this list.



## merge audio and video


To combine video and audio track, run
```
ffmpeg -i example.mp4 -i example.wav -c:v copy -c:a aac combined.mp4
```





