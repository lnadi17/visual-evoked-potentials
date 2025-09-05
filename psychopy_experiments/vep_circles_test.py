# Oddball (Standard vs. Oddball) with PsychoPy + LSL
from psychopy import visual, core, event, logging
from psychopy.visual import Window
from pylsl import StreamInfo, StreamOutlet
import random

# ---------------- Config ----------------
total_trials       = 20            # total number of trials
target_prob        = 0.20           # proportion of oddballs (red)
total_trial_len    = 1.00           # seconds
prestimulus_time   = 0.20           # seconds (blank)
stimulus_time      = 0.20           # seconds (circle on)
iti_jitter_range   = (0.00, 0.10)   # optional: random extra ITI (min,max), set both to 0 to disable

fullscr            = False
win_size           = [800, 600]
bg_color           = [-1, -1, -1]   # black
circle_radius_px   = 100            # radius of circle (in pix when units="pix")

# LSL markers
MARK_STANDARD = 1
MARK_ODDBALL  = 2

# ------------- LSL stream --------------
info = StreamInfo(name='PsychopyMarkerStream', type='Markers',
                  channel_count=1, channel_format='int32',
                  source_id='uniqueid12345')
outlet = StreamOutlet(info)

# ------------- Window ------------------
win = Window(size=win_size, units="pix", fullscr=fullscr, color=bg_color)

# ------------- Stimuli -----------------
standard_circle = visual.Circle(win, radius=circle_radius_px,
                                fillColor=[-0.25, -0.25, 1.0],  # blue-ish
                                lineColor=[-0.25, -0.25, 1.0])
oddball_circle  = visual.Circle(win, radius=circle_radius_px,
                                fillColor=[1.0, -1.0, -1.0],     # red
                                lineColor=[1.0, -1.0, -1.0])

# ------------- Sequence ----------------
# Build an exact-length sequence with the desired oddball proportion
n_oddballs  = int(round(total_trials * target_prob))
n_standards = total_trials - n_oddballs
sequence = ([MARK_ODDBALL] * n_oddballs) + ([MARK_STANDARD] * n_standards)
random.shuffle(sequence)

# ------------- Intro screen ------------
start_message = visual.TextStim(win,
                                text="Oddball task\n\nBlue = standard, Red = oddball\n\nPress Enter to start\n(Press Esc anytime to quit)",
                                color="white", height=24)
start_message.draw()
win.flip()
event.waitKeys(keyList=["return"])

# ------------- Run ---------------------
clock = core.Clock()
logging.console.setLevel(logging.INFO)

for i, code in enumerate(sequence, start=1):
    # Allow early exit
    if event.getKeys(keyList=["escape", "esc"]):
        break

    logging.info(f"Trial {i}/{total_trials} - {'ODDBALL' if code == MARK_ODDBALL else 'STANDARD'}")

    # Pre-stimulus (blank)
    win.flip()
    core.wait(prestimulus_time)

    # Draw stimulus for stimulus_time and send marker exactly on flip
    if code == MARK_ODDBALL:
        oddball_circle.draw()
    else:
        standard_circle.draw()

    win.callOnFlip(outlet.push_sample, [code])
    win.flip()
    core.wait(stimulus_time)

    # Inter-trial interval (blank), with optional jitter
    jitter = 0.0
    if iti_jitter_range[1] > 0:
        jitter = random.uniform(iti_jitter_range[0], iti_jitter_range[1])

    remaining = total_trial_len - prestimulus_time - stimulus_time + jitter
    if remaining > 0:
        win.flip()
        core.wait(remaining)
    else:
        # If timing is too tight, at least ensure a flip
        win.flip()

# ------------- Cleanup -----------------
win.close()
core.quit()
