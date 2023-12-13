import mido
import numpy as np


def get_deltas(ts_on, dt):

    ts_on = np.sort(ts_on) # make sure that order increases
    ts_off = ts_on + dt
    ts_on_off = np.stack([ts_on, ts_off], axis=1).flatten()
    delta_on_off = np.diff(ts_on_off)

    # ensure that no negative deltas
    m = np.flatnonzero(delta_on_off < 0) # find negative deltas
    ts_on_off[ m+1 ] = ts_on_off[ m+2 ] # replace negative deltas with next time
    delta_on_off = np.diff(ts_on_off)
    delta_on_off = np.insert(delta_on_off, 0, ts_on_off[0])

    return delta_on_off

def generate_note_sequence(root_note, semitone_sequence, number):

    notes = []
    
    for i in range(number):

        step = semitone_sequence[i % len(semitone_sequence)]
        octave = 12 * np.floor_divide(i, len(semitone_sequence))
        note = root_note + step + octave

        assert type(note) == np.int64, 'MIDI note must be integer'
        assert note <= 127, 'MIDI notes must not exceed 127, adjust `root_note` and `semitone_sequence` accordingly'
        
        notes.append(note)

    return notes

def times2midi(l_times,
               ticks_per_beat=4800, bpm=120, time_signature=(4, 4), program=0, channel=0,
               velocity=64, root_note=60, note_duration=.1,
               semitone_sequence=[0, 4, 7],
               merge_tracks=True, path=''):
    
    notes = generate_note_sequence(root_note, semitone_sequence, len(l_times))

    tempo = mido.bpm2tempo(bpm=bpm, time_signature=time_signature)
    time2tick = lambda i: mido.second2tick(i, ticks_per_beat=ticks_per_beat, tempo=tempo)
    
    duration = time2tick(note_duration) # note duration in ticks
    
    l_track = []
    for note, times in zip(notes, l_times):
        track = mido.MidiTrack()
        track.append(mido.Message('program_change', program=program, time=0, channel=channel))


        ticks = [ time2tick(i) for i in times ] # list of time events in ticks
        delta_ticks = get_deltas(ticks, duration)

        for dt_on, dt_off in zip(delta_ticks[::2], delta_ticks[1::2]):
            track.append(mido.Message('note_on',  note=note, velocity=velocity, time=dt_on,  channel=channel))
            track.append(mido.Message('note_off', note=note, velocity=velocity, time=dt_off, channel=channel))
        
        l_track.append(track)

    # construct file
    mid = mido.MidiFile(type=1, ticks_per_beat=ticks_per_beat) # type 1: multiple tracks, same start
    
    if merge_tracks:
        merged_tracks = mido.merge_tracks(l_track)
        mid.tracks.append(merged_tracks)
    
    else:
        for track in l_track:
            mid.tracks.append(track)

    if path:
        mid.save(path)
    else:
        return mid