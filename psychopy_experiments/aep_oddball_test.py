# PsychoPy Auditory MMN (Standard vs Deviant) + LSL markers
# 1 = standard (1000 Hz), 2 = deviant (1200 Hz)

from psychopy import prefs
# Prefer PTB for precise audio timing; falls back if unavailable
prefs.hardware['audioLib'] = ['ptb', 'sounddevice', 'pyo']

from psychopy import sound, visual, core, event, logging
from psychopy.visual import Window
from pylsl import StreamInfo, StreamOutlet
import random

# ------------ Config ------------
total_trials       = 20           # total number of tones
target_prob        = 0.20          # proportion of deviants
stimulus_time      = 0.100         # tone duration (s)
prestimulus_silence= 0.000         # optional silence before each tone (s)
iti_time           = 0.400         # inter-tone interval after tone offset (s)
# SOA ~= prestimulus_silence + stimulus_time + iti_time

standard_freq_hz   = 1000
deviant_freq_hz    = 1200
volume             = 0.8           # 0..1

# Optional slight SOA jitter to reduce predictability (set both to 0 to disable)
iti_jitter_range   = (0.0, 0.0)    # seconds; e.g., (0.0, 0.05)

fullscr            = False
win_size           = [640, 480]
bg_color           = [-1, -1, -1]

MARK_STANDARD = 1
MARK_DEVIANT  = 2

# ------------ LSL ------------
info = StreamInfo(name='PsychopyMarkerStream', type='Markers',
                  channel_count=1, channel_format='int32',
                  source_id='mmn_uniqueid12345')
outlet = StreamOutlet(info)

# ------------ Visual (minimal) ------------
# We keep a window to use win.getFutureFlipTime + callOnFlip for tight sync
win = Window(size=win_size, units="pix", fullscr=fullscr, color=bg_color)
instr = visual.TextStim(
    win,
    text=(
        "Auditory MMN task\n\n"
        "Listen passively.\n"
        "Standard tone = 1000 Hz, Deviant = 1200 Hz\n\n"
        "Press Enter to start.\n(Press Esc anytime to quit.)"
    ),
    color="white", height=24
)
instr.draw()
win.flip()
event.waitKeys(keyList=["return"])

# ------------ Sounds ------------
# Hamming ramp is applied by PsychoPy to reduce clicks
standard_tone = sound.Sound(value=standard_freq_hz, secs=stimulus_time,
                            stereo=False, hamming=True, volume=volume)
deviant_tone  = sound.Sound(value=deviant_freq_hz, secs=stimulus_time,
                            stereo=False, hamming=True, volume=volume)

# ------------ Sequence ------------
n_deviants  = int(round(total_trials * target_prob))
n_standards = total_trials - n_deviants
sequence = ([MARK_DEVIANT] * n_deviants) + ([MARK_STANDARD] * n_standards)
random.shuffle(sequence)

logging.console.setLevel(logging.INFO)

# ------------ Run ------------
for i, code in enumerate(sequence, start=1):
    # Early exit
    if event.getKeys(keyList=["escape", "esc"]):
        break

    is_dev = (code == MARK_DEVIANT)
    logging.info(f"Trial {i}/{total_trials} - {'DEVIANT' if is_dev else 'STANDARD'}")

    # Optional pre-stimulus silence
    if prestimulus_silence > 0:
        win.flip()
        core.wait(prestimulus_silence)

    # Prepare the tone for synchronized onset:
    #   - schedule audio to start exactly on the next flip time
    #   - schedule LSL marker on the same flip
    target_time = win.getFutureFlipTime(clock='ptb')  # PTB clock for audio sync

    if is_dev:
        deviant_tone.play(when=target_time)
    else:
        standard_tone.play(when=target_time)

    win.callOnFlip(outlet.push_sample, [code])  # send marker exactly at sound onset
    win.flip()  # triggers both the audio onset and the marker

    # Hold until tone finishes
    core.wait(stimulus_time)

    # Inter-tone interval (silence), with optional jitter
    jitter = 0.0
    if iti_jitter_range[1] > 0:
        jitter = random.uniform(iti_jitter_range[0], iti_jitter_range[1])
    iti = iti_time + jitter

    if iti > 0:
        win.flip()  # keep screen blank
        core.wait(iti)

# ------------ Cleanup ------------
win.close()
core.quit()
