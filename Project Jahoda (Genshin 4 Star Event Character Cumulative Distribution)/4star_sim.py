### Sources:
# https://www.hoyolab.com/article/31323555
# https://genshin-impact.fandom.com/wiki/Wish

# HOW TO USE
# Run "pip install numpy"
# Run "pip install matplotlib"
# 
# Run "py .\4star_sim.py"

import numpy as np
from numpy import random
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Simulation params
N = 1000000 # How many pull periods
RUN_CAP = 150 # How may pulls before giving up

# Probabilities
P_4STAR_BASE = 0.051 # Base 
P_EVENT_4STAR = 0.5 # 50% of event char, 50% of regular 4 star or weapon
P_GUARANTEE_4STAR = 0.994 # 99.4% 4 star, 0.6% 5 star
P_SPECIFIC_EVENT_4STAR = 1/3 # After winnning specific 4 star char, 1/3

GUARANTEE_4STAR = 10 # Guaranteed to win 4/5 star if no 10 in a row
# 2x10 pulls guarantee event character

# Determines if win or loss given a probability
def draw(probability):
    x = random.rand()
    return x < probability # ex: 50% -> middle is 500. 0-499 lose, 500-999 win

# returns necessary data for if drawing an event char was 4 star or 5 star
def draw_evenchar():
    # Won specific event 4 star
    if draw(P_GUARANTEE_4STAR) and draw(P_SPECIFIC_EVENT_4STAR): return [0, False, True]
    return [0, False, False] # Otherwise, won someone else (not specific 4 star, or 5 star)

# In charge of simulating each pull
# Requires and updates number of pulls without win, and if an event character is guaranteed
def run_pull(pulls_without_win, lost_event_char):
    pulls_without_win += 1
    if pulls_without_win == GUARANTEE_4STAR:
        # Guarantee 4/5 star
        if lost_event_char:
            # guarantee event character (20 pulls)
            return draw_evenchar()
        else:
            # Won character (normal 10 pull)
            if draw(P_EVENT_4STAR):
                # Won event 4 star character
                return draw_evenchar()
            else:
                # Won regular 4 star character
                return [0, True, False]
    else:
        # normal pull
        if draw(P_4STAR_BASE):
            # Win 4 star
            if lost_event_char or draw(P_EVENT_4STAR):
                # Won event 4 star character
                return draw_evenchar()
            else:
                # Won regular 4 star character
                return [0, True, False]
        else:
            # No win
            return [pulls_without_win, lost_event_char, False]


### Main
raw_data = [0] * RUN_CAP
p_data = [0] * RUN_CAP
y_data = [0] * RUN_CAP
x_data = list(range(1, RUN_CAP+1))
total = 0

N_counter = 0 # how many pull periods
print("Running")
while (N_counter < N):
    # Reset
    i = 0 # how many pulls
    pulls_without_win=0
    lost_event_char = False
    got_4star = False

    while(i < RUN_CAP):
        pulls_without_win, lost_event_char, got_4star = run_pull(pulls_without_win, lost_event_char)
        # print(str(pulls_without_win) + str(lost_event_char) + str(got_4star))
        if got_4star:
            raw_data[i] += 1
            i = RUN_CAP # Trigger Reset
        i += 1

    # Iterate
    N_counter += 1
    if N_counter % (N/10) == 0: print(str(100 * (N_counter/N)) + "%")

# Post processing to percent
y_data[0] = (raw_data[0]/N)
for j in range(1, RUN_CAP):
    y_data[j] = y_data[j-1] + (raw_data[j]/N)
    assert(y_data[j] > y_data[j-1])
    
# Can plot cumulative distribution with "data" here
print (x_data)
print (y_data)
plt.plot(x_data, y_data)
plt.xlabel("Pulls required")
plt.ylabel("Cumulative probability")
plt.title("Cumulative Distribution of Specific 4 Star (Jahoda)")
plt.grid()
plt.fill_between(x_data, y_data, color='skyblue', alpha=0.4)
plt.gca().xaxis.set_major_locator(MultipleLocator(10))   # every 5 pulls
plt.gca().yaxis.set_major_locator(MultipleLocator(0.05)) # every 0.1 probability
plt.show()
