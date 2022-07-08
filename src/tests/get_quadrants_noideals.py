import os
import pandas as pd
from datetime import datetime
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from statistics import mean

# Define important variables
file = pd.read_csv("../../data/fire_volcano_watertemp_ruapehu.csv")
fn="fire_volcano_watertemp_ruapehu"
entity="volcano"
measurement="temp_celsius"
datacol = "Temperature"
timecol = "Year"

# Define important variables
file = pd.read_csv("../../data/fire_volcano_watertemp_kawahIjen.csv")
fn="fire_volcano_watertemp_kawahIjen"
entity="volcano"
measurement="temp_celsius"
datacol = "temp_celsius"
timecol = "time"

# START PREP STORY #####################################################################
sdf = pd.read_csv('../../source_text/input_prompts.csv')
entity = "Volcano"
entityunit = "volcano_temp"
entityadjs = " colossal and simmering"
entitybio = "My home is quite pleasant, with warm summers and cool winters. I see a fair amount of rainfall, which helps to keep my vegetation healthy and lush. Rare species of birds make their homes inside me"

def get_prompt(skey,dmood,nmood):
    descr = "null"
    narr = "null"
    try:
        match = sdf.loc[sdf['0'] == skey]
        descr= match[dmood].tolist()[0]
        narr = match[nmood].tolist()[0]
    except:
        print("prompt not found")

    return(descr,narr)
# END PREP STORY #####################################################################

# Convert time to datetime and set date as index
df = file.copy()
df[timecol] = pd.to_datetime(df[timecol], infer_datetime_format=True)
df.set_index(timecol, inplace=True)
print(df.head(4))

# Interpolate between consistent units
df_interpol = df.resample('M').mean()
df_interpol[datacol] = df_interpol[datacol].interpolate()

nrmax = df_interpol[datacol].max()
nrmin = df_interpol[datacol].min()

idealmin = nrmin
idealmax = nrmax

# Divide data measurements into 5 sentiment zones
increment = (nrmax - nrmin) / 5
print(increment)
segments = [nrmin, nrmin + (increment * 1), nrmin + (increment * 2), nrmin + (increment * 3) , nrmin + (increment * 4), nrmax]
print(segments)

# Assess the mood of a datapoint based on the segment it belongs to
def check_segment(datapoint):
    mood="Unknown"
    color="Black"
    if segments[0] <= datapoint <= segments[1]:
        mood = "Mood 1"
        color = 'darkred'
        #color = 'turquoise'
        mscale = 100
    elif segments[1] <= datapoint <= segments[2]:
        mood = "Mood 2"
        color = 'orangered'
        #color = 'olivedrab'
        mscale = 200
    elif segments[2] <= datapoint <= segments[3]:
        mood = "Mood 3"
        color = 'gold'
        mscale = 300
    elif segments[3] <= datapoint <= segments[4]:
        mood = "Mood 4"
        #color = 'orangered'
        color = 'olivedrab'
        mscale = 400
    elif segments[4] <= datapoint <= segments[5]:
        mood = "Mood 5"
        #color = 'darkred'
        color = 'turquoise'
        mscale = 500
    elif segments[5] <= datapoint <= segments[6]:
        mood = "Mood 6"
        mscale = 500
        #color = 'darkred'
    print(mood)

    return(mood, color, mscale)


# Divide time into 3 acts
tspan = df_interpol.index.max() - df_interpol.index.min()
tinc = tspan / 3
print("Span, Increment: ",tspan, tinc)

# Calculate interesting values for each act
actavgs = []
actmins = []
actmaxs = []
print("first act rows: ")
print(df_interpol.loc[df_interpol.index.min():df_interpol.index.min()+tinc])
mean1 = df_interpol.loc[df_interpol.index.min():df_interpol.index.min()+tinc].mean()
mean1=mean1.values.tolist()[0]
min1 = df_interpol.loc[df_interpol.index.min():df_interpol.index.min()+tinc].min()
min1=min1.values.tolist()[0]
max1 = df_interpol.loc[df_interpol.index.min():df_interpol.index.min()+tinc].max()
max1=max1.values.tolist()[0]
actavgs.append(mean1)
actmins.append(min1)
actmaxs.append(max1)
print(actavgs[0],actmins[0],actmaxs[0])

print("second act rows: ")
print(df_interpol.loc[df_interpol.index.min()+tinc:df_interpol.index.max()-tinc])
mean2 = df_interpol.loc[df_interpol.index.min()+tinc:df_interpol.index.max()-tinc].mean()
mean2=mean2.values.tolist()[0]
min2 = df_interpol.loc[df_interpol.index.min()+tinc:df_interpol.index.max()-tinc].min()
min2=min2.values.tolist()[0]
max2 = df_interpol.loc[df_interpol.index.min()+tinc:df_interpol.index.max()-tinc].max()
max2=max2.values.tolist()[0]
actavgs.append(mean2)
actmins.append(min2)
actmaxs.append(max2)
print(actavgs[1],actmins[1],actmaxs[1])

print("third act rows: ")
print(df_interpol.loc[df_interpol.index.max()-tinc:df_interpol.index.max()])
mean3 = df_interpol.loc[df_interpol.index.max()-tinc:df_interpol.index.max()].mean()
mean3=mean3.values.tolist()[0]
min3 = df_interpol.loc[df_interpol.index.max()-tinc:df_interpol.index.max()].min()
min3=min3.values.tolist()[0]
max3 = df_interpol.loc[df_interpol.index.max()-tinc:df_interpol.index.max()].max()
max3 = max3.values.tolist()[0]
actavgs.append(mean3)
actmins.append(min3)
actmaxs.append(max3)
print(actavgs[2],actmins[2],actmaxs[2])

# Prepare the plot
x = df_interpol.index
y = df_interpol[datacol]

plt.plot(x, y, color='gray', linestyle='--', marker='o')
plt.xlim([x.min(),x.max()])

if idealmin < y.min():
    ymin = idealmin
else:
    ymin= y.min()

if idealmax > y.max():
    ymax = idealmax
else:
    ymax= y.max()

ysmin = ymin-(idealmax-idealmin)
ysmax = ymax+(idealmax-idealmin)
print("o-range: ", ymin, ymax, idealmax-idealmin)
print("n-range: ", ysmin, ysmax )

# plt.ylim([ysmin,ysmax])
plt.axhline(y=idealmin, color='blue', linestyle='-')
#plt.axhline(y=idealmax, color='red', linestyle='-')

plt.axvline(x=x.min() + tinc, color='black', linestyle='-')
plt.axvline(x=x.max() - tinc, color='black', linestyle='-')

plt.axhline(y=segments[1], color='darkred', linestyle='--')
plt.axhline(y=segments[2], color='orangered', linestyle='--')
plt.axhline(y=segments[3], color='gold', linestyle='--')
plt.axhline(y=segments[4], color='olivedrab', linestyle='--')
plt.axhline(y=segments[5], color='turquoise', linestyle='--')

# Use averages
act1meta = [x.min() + (tinc/2), actavgs[0]]
act2meta = [x.min() + tinc + (tinc/2), actavgs[1]]
act3meta = [x.min() + tinc + tinc + (tinc/2), actavgs[2]]

# Use maxes
act1meta = [x.min() + (tinc/2), actmaxs[0]]
act2meta = [x.min() + tinc + (tinc/2), actmaxs[1]]
act3meta = [x.min() + tinc + tinc + (tinc/2), actmaxs[2]]

# Use mins
act1meta = [x.min() + (tinc/2), actmins[0]]
act2meta = [x.min() + tinc + (tinc/2), actmins[1]]
act3meta = [x.min() + tinc + tinc + (tinc/2), actmins[2]]

plt.plot(act1meta[0],act1meta[1], marker="D", markersize=10, markeredgecolor="black", markerfacecolor="yellow")
plt.text(act1meta[0],act1meta[1], check_segment(act1meta[1])[0],color=check_segment(act1meta[1])[1],weight="bold")

plt.plot(act2meta[0],act2meta[1], marker="D", markersize=10, markeredgecolor="black", markerfacecolor="yellow")
plt.text(act2meta[0],act2meta[1], check_segment(act2meta[1])[0],color=check_segment(act2meta[1])[1],weight="bold")

plt.plot(act3meta[0],act3meta[1], marker="D", markersize=10, markeredgecolor="black", markerfacecolor="yellow")
plt.text(act3meta[0],act3meta[1], check_segment(act3meta[1])[0],color=check_segment(act3meta[1])[1],weight="bold")

title = fn + " (" + entity + " + " + measurement + ")"
plt.title(title)
plt.xlabel("Time")
plt.ylabel("Measurement")
plt.show()

# START GENERATE TEXT #####################################################################
mscale1 = check_segment(act1meta[1])[2]
mscale2 = check_segment(act2meta[1])[2]
mscale3 = check_segment(act3meta[1])[2]

prompta1 = get_prompt(entityunit,str(mscale1),str(mscale1+50))
prompta2 = get_prompt(entityunit,str(mscale2),str(mscale2+50))
prompta3 = get_prompt(entityunit,str(mscale3),str(mscale3+50))

completiona1 = "I feel... <placeholder for AI text for Act 1>"
completiona2 = "I feel... <placeholder for AI text for Act 2>"
completiona3 = "I feel... <placeholder for AI text for Act 3>"

wprompt = {
    "introl1": f"The following play reveals the inner monologue of a {entityadjs} {entity.lower()}. It is divided into several acts. Throughout these acts, the {entity.lower()} describes its inner and outer transformation:\n",
    "introl2": "The first act starts like this:\n",
    "act0l1": f"Act 0: The {entity.lower()} introduces itself and describes its surroundings.",
    "act0l2": "---",
    "act0p": entity + ": " + entitybio,
    "act0e": "---",
    "act1l1": "\nAct 1: "  + prompta1[0] + " " + prompta1[1],
    "act1l2": "---",
    "act1p": entity + ": " + completiona1,
    "act1e": "---",
    "act2l1": "\nAct 2: " + prompta2[0] + " " + prompta2[1],
    "act2l2": "---",
    "act2p": entity + ": " + completiona2,
    "act2e": "---",
    "act3l1": "\nAct 3: " + prompta3[0] + " " + prompta3[1],
    "act3l2": "---",
    "act3p": entity + ": " + completiona3,
    "act3e": "---",
}

for w in wprompt:
    print(wprompt[w])
# END GENERATE TEXT #####################################################################