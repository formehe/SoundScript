from pydub import AudioSegment,silence

def strip_edging_silence(audio:AudioSegment):
    start_end = silence.detect_silence(audio, 500, -40, 1)
    sound_start = 0
    sound_end = len(audio)
    for o in start_end:
        if o[1] == len(audio):
            sound_end = o[0]
        if o[0] == 0:
            sound_start = o[1]
    audio = audio[sound_start:sound_end]
    return audio

#volume:xxdb
def tune_volume(audio:AudioSegment, volume:float):
    return  audio.apply_gain(volume)

#how to solve the smooth of the joint point
def overlay(overlay_audio:AudioSegment, overlayed_audio:AudioSegment):
    num_loops = len(overlayed_audio) // len(overlay_audio) + 1
    audio = overlayed_audio.overlay(overlay_audio * num_loops, position=0)
    return audio

#how to solve the smooth of the joint point
def join(joined_audio:AudioSegment, joining_audio:AudioSegment):
    return joined_audio.append(joining_audio)

#percent:[-1,1]
def tune_sound_track(audio:AudioSegment, percent:float):
    return audio.pan(percent)

def add_fade(audio:AudioSegment, fadeIn:int = 0, fadeout:int = 0):
    fade_audio = audio
    if fadeIn != 0:
        fade_audio = fade_audio.fade_in(fadeIn)
    if fadeout != 0:
        fade_audio = fade_audio.fade_out(fadeIn)
    return fade_audio