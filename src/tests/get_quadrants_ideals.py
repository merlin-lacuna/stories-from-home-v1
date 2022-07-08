import os
import pandas as pd
from datetime import datetime
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from statistics import mean

# Define important variables
file = pd.read_csv("../../data/air_atmo_n0_tamuranui.csv")
fn="air_atmo_n0_tamuranui"
entity="forest"
measurement="C0"
datacol = "CO_column_number_density"
timecol = "Time"

idealmin = 0.016
idealmax = 0.025

# START PREP STORY #####################################################################
sdf = pd.read_csv('../../source_text/input_prompts.csv')
entity = "Land"
entityunit = "urbanland_cover"
entityadjs = "large and complex"
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

# Divide data measurements into 5 sentiment zones based on entire data range
increment = (nrmax - nrmin) / 5
print(increment)
possegments = [nrmin, nrmin + (increment * 1), nrmin + (increment * 2), nrmin + (increment * 3) , nrmin + (increment * 4), nrmax]
print(possegments)

# Divide data measurements into 4 sentiment zones based on proximity to ideal
increment = (idealmax - idealmin) / 2
print("increment: ",increment)
possegments = [
    idealmin + (increment * 1),
    idealmin + (increment * 2),
    idealmin + (increment * 3),
    idealmin + (increment * 4),
    idealmin + (increment * 5),
    idealmin + (increment * 6)
]
print("possegments: ", possegments)

negsegments = [
    idealmin + (increment * 1),
    idealmin,
    idealmin - (increment * 1),
    idealmin - (increment * 2),
    idealmin - (increment * 3),
    idealmin - (increment * 4)
]
print("negsegments: ", negsegments)

# Assess the mood of a datapoint based on the segment it belongs to
def check_segment(datapoint):
    mood="Unknown"
    color="black"
    if (possegments[0] <= datapoint <= possegments[1]) or (negsegments[0] >= datapoint >= negsegments[1]):
        mood = "Mood 5"
        color = 'turquoise'
        mscale = 500
    elif possegments[1] <= datapoint <= possegments[2] or (negsegments[1] >= datapoint >= negsegments[2]):
        mood = "Mood 4"
        color = 'olivedrab'
        mscale = 400
    elif possegments[2] <= datapoint <= possegments[3] or (negsegments[2] >= datapoint >= negsegments[3]):
        mood = "Mood 3"
        color = 'gold'
        mscale = 300
    elif possegments[3] <= datapoint <= possegments[4] or (negsegments[3] >= datapoint >= negsegments[4]):
        mood = "Mood 2"
        color = 'orangered'
        mscale = 200
    elif possegments[4] <= datapoint <= possegments[5] or (negsegments[4] >= datapoint >= negsegments[5]):
        mood = "Mood 1"
        color = 'darkred'
        mscale = 100
    elif possegments[5] < datapoint or negsegments[5] > datapoint:
         mood = "Mood 0"
         color = 'darkred'
         mscale = 100
    print("mood: ",mood,"color: ",color,"scale: ",)

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

# adjust chart range to be slightly bigger than value range
ysmin = ymin-(idealmax-idealmin)
ysmax = ymax+(idealmax-idealmin)

plt.ylim([ysmin,ysmax])
# plt.axhline(y=idealmin*0.98, color='hotpink', linestyle='-', linewidth=2)
# plt.axhline(y=idealmax*1.02, color='pink', linestyle='-',linewidth=2)

plt.axvline(x=x.min() + tinc, color='black', linestyle='-')
plt.axvline(x=x.max() - tinc, color='black', linestyle='-')

plt.axhline(y=possegments[4], color='darkred', linestyle='--')
plt.axhline(y=possegments[3], color='orangered', linestyle='--')
plt.axhline(y=possegments[2], color='gold', linestyle='--')
plt.axhline(y=possegments[1], color='olivedrab', linestyle='--')
plt.axhline(y=possegments[0], color='turquoise', linestyle='--')

plt.axhline(y=negsegments[4], color='darkred', linestyle='--')
plt.axhline(y=negsegments[3], color='orangered', linestyle='--')
plt.axhline(y=negsegments[2], color='gold', linestyle='--')
plt.axhline(y=negsegments[1], color='olivedrab', linestyle='--')
plt.axhline(y=negsegments[0], color='turquoise', linestyle='--')

plt.axhspan(idealmin, idealmax, facecolor='g', alpha=0.25)

# Use mins
act1meta = [x.min() + (tinc/2), actmins[0]]
act2meta = [x.min() + tinc + (tinc/2), actmins[1]]
act3meta = [x.min() + tinc + tinc + (tinc/2), actmins[2]]

# Use maxes
act1meta = [x.min() + (tinc/2), actmaxs[0]]
act2meta = [x.min() + tinc + (tinc/2), actmaxs[1]]
act3meta = [x.min() + tinc + tinc + (tinc/2), actmaxs[2]]

# Use averages
act1meta = [x.min() + (tinc/2), actavgs[0]]
act2meta = [x.min() + tinc + (tinc/2), actavgs[1]]
act3meta = [x.min() + tinc + tinc + (tinc/2), actavgs[2]]

print("plotting act 1 info",(act1meta[0],act1meta[1]))
plt.plot(act1meta[0],act1meta[1], marker="D", markersize=10, markeredgecolor="black", markerfacecolor="yellow")
plt.text(act1meta[0],act1meta[1], check_segment(act1meta[1])[0],color=check_segment(act1meta[1])[1],weight="bold")

print("plotting act 2 info",(act2meta[0],act2meta[1]))
plt.plot(act2meta[0],act2meta[1], marker="D", markersize=10, markeredgecolor="black", markerfacecolor="yellow")
plt.text(act2meta[0],act2meta[1], check_segment(act2meta[1])[0],color=check_segment(act2meta[1])[1],weight="bold")

print("plotting act 3 info",(act3meta[0],act3meta[1]))
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