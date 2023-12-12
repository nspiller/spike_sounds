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

# movie creation

Convert MIDI to wav:

https://www.zamzar.com/
(https://signal.vercel.app drops events)

Combine video and audio track
```
ffmpeg -i example.mp4 -i example.wav -c:v copy -c:a aac combined.mp4
```

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
