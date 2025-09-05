"""
A simple visually evoked potential task.
(c) Syntrogi Inc dba Intheon. All Rights Reserved.
# Tag: Open
"""

import random
import inspect

from src.snap.latentmodule import LatentModule

class Main(LatentModule):

    def __init__(self):
        LatentModule.__init__(self)
        self.title = 'Visual Evoked Potentials'
        # probability of showing oddball
        self.probability_odd = 0.2
        self.num_trials = 12
        self.len_block = 5                 # how many trials before prompt
        # self.iti_wait = 1                # seconds between trials (not used)
        self.oddball = {'code': 'o', 'marker': 'oddball', 'path': '../media/red_circle.png'}   # Red
        self.standard = {'code': 's', 'marker': 'standard', 'path': '../media/blue_circle.png'} # Blue
        self.white = {'path': '../media/left_arrow_white.png'}
        self.black = {'path': '../media/diamond.png'}
        self.pretrial_time = 0.5         # seconds before stimulus
        self.stim_display_time = 0.5     # seconds stimulus is shown
        self.trial_len_min = 1.0         # minimum total trial length (seconds)
        self.trial_len_max = 2.0         # maximum total trial length (seconds)

    def run(self):
        
        # create random distribution of odds/standards
        odds = [self.oddball['code']] * int(self.num_trials * self.probability_odd)
        standards = [self.standard['code']] * (self.num_trials - len(odds))
        circles = odds + standards

        random.shuffle(circles)
        # 2 / 0
        # shuffle until there are no consecutive odds
        # while (self.oddball['code']*2) in ''.join(circles):
        #     random.shuffle(circles)
        
        base.win.setClearColor((0.5, 0.5, 0.5, 1))
        self.write(self.title,
                duration=3.0, align='center', pos=(0, 0), scale=0.16)
       
        instructions = inspect.cleandoc("""\
            Instructions

            Simply look at the crosshair on the screen, and pay attention 
            to the colored circles that will be shown repeatedly. 

            There are two types of circles: a "standard" blue circle 
            and a "high" red circle. 
            
            As the task progresses, in your head, 
            count the number of "high" (red) circles you see. 
            Every so often you will be asked how many "high" circles 
            were shown since you were last asked. Start to 
            count them again from zero from that point on. 

            Press space bar to continue.""")
        self.write(instructions, 'space', wordwrap=30, pos=[0, 0.6])

        line1 = self.write('Here is a "standard" blue circle', duration=0, pos=[0, 0.6])
        self.picture(self.standard['path'], duration=2, scale=0.3, pos=(0, 0))
        line2 = self.write('Here it is again:', duration=0, pos=[0, 0.4])
        self.sleep(1)
        self.picture(self.standard['path'], duration=2, scale=0.3, pos=(0, 0))
        self.write('Press space bar to continue.', duration='space', pos=(0, -0.8))
        line1.destroy()
        line2.destroy()

        line1 = self.write('Here is a "high" red circle', duration=0, pos=[0, 0.6])
        self.picture(self.oddball['path'], duration=2, scale=0.3, pos=(0, 0))
        line2 = self.write('Here it is again:', duration=0, pos=[0, 0.4])
        self.sleep(1)
        self.picture(self.oddball['path'], duration=2, scale=0.3, pos=(0, 0))
        self.write('Press space bar to begin task.', duration='space', pos=(0, -0.8))
        line1.destroy()
        line2.destroy()

        self.marker('task-begin-vep')

        cross = self.crosshair(duration=0, block=False, size=0.05, width=0.005,
                       color=(0, 0, 0, 1))
        black = self.picture(self.black['path'], scale=0.2, pos=(1.5, -0.8), duration=0)

        counter = 0
        for circle in circles:
            self.marker('trial-begin')

            self.sleep(self.pretrial_time)

            if circle == self.oddball['code']:
                self.marker(self.oddball['marker'])
                self.picture(self.white['path'], scale=0.2, pos=(1.5, -0.8), duration=self.stim_display_time)
             #   self.picture(self.oddball['path'], scale=0.3, duration=self.stim_display_time, pos=(0, 0))
            else:
                self.marker(self.standard['marker'])
                self.picture(self.white['path'], scale=0.2, pos=(1.5, -0.8), duration=self.stim_display_time)
              #  self.picture(self.standard['path'], scale=0.3, duration=self.stim_display_time, pos=(0, 0))

            # Randomize total trial length
            total_trial_len = random.uniform(self.trial_len_min, self.trial_len_max)
            remaining_time = max(0, total_trial_len - self.pretrial_time - self.stim_display_time)
            self.sleep(remaining_time)

            if counter == self.len_block:
                cross.destroy()
                instructions2 = inspect.cleandoc("""\
                    Type the number of "high" (red) circles
                    you saw since the last time you were prompted, 
                    and press the enter key. 
                    """)
                self.write(instructions2,'enter', wordwrap=30, pos=[0, 0.2])
                counter = 0
                cross = self.crosshair(duration=0, block=False, size=0.05, width=0.005,
                                       color=(0, 0, 0, 1))
            counter += 1

            self.marker('trial-end')

        self.marker('task-end-vep')

        cross.destroy()
        self.write('Task complete! \n\nPress Enter to exit.', duration='enter', align='center', scale=0.1)

        self.sleep(0.5)