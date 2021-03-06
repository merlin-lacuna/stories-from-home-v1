import os
import pandas as pd
from datetime import datetime
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from statistics import mean

# Define important variables
file = pd.read_csv("../../data/fire_forestfire_nvdi_mendocino.csv")
fn="fire_forestfire_nvdi_mendocino"
entity="forest"
measurement="NDVI"
datacol = "mean_NDVI"
timecol = "Time"

idealmin = 0.33
idealmax = 1.00

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

# Divide data measurements into 5 sentiment zones
increment = (nrmax - nrmin) / 5
print(increment)
segments = [nrmin, nrmin + (increment * 1), nrmin + (increment * 2), nrmin + (increment * 3) , nrmin + (increment * 4), nrmax]
print(segments)

# Assess the mood of a datapoint based on the segment it belongs to
def check_segment(datapoint):
    mood=""
    color="white"
    if segments[0] <= datapoint <= segments[1]:
        mood = "Mood 1"
        color = 'darkred'
        #color = 'turquoise'
    elif segments[1] <= datapoint <= segments[2]:
        mood = "Mood 2"
        color = 'orangered'
        #color = 'olivedrab'
    elif segments[2] <= datapoint <= segments[3]:
        mood = "Mood 3"
        color = 'gold'
    elif segments[3] <= datapoint <= segments[4]:
        mood = "Mood 4"
        #color = 'orangered'
        color = 'olivedrab'
    elif segments[4] <= datapoint <= segments[5]:
        mood = "Mood 5"
        #color = 'darkred'
        color = 'turquoise'
    elif segments[5] <= datapoint <= segments[6]:
        mood = "Mood 6"
        #color = 'darkred'
    print(mood)

    return(mood, color)


# Divide time into 3 acts
tspan = df_interpol.index.max() - df_interpol.index.min()
tinc = tspan / 3
print("Span, Increment: ",tspan, tinc)

# Calculate average values for each act
actavgs = []
print("first act rows: ")
print(df_interpol.loc[df_interpol.index.min():df_interpol.index.min()+tinc])
mean1 = df_interpol.loc[df_interpol.index.min():df_interpol.index.min()+tinc].mean()
mean1=mean1.values.tolist()[0]
actavgs.append(mean1)
print(actavgs[0])

print("second act rows: ")
print(df_interpol.loc[df_interpol.index.min()+tinc:df_interpol.index.max()-tinc])
mean2 = df_interpol.loc[df_interpol.index.min()+tinc:df_interpol.index.max()-tinc].mean()
mean2=mean2.values.tolist()[0]
actavgs.append(mean2)
print(actavgs[1])

print("third act rows: ")
print(df_interpol.loc[df_interpol.index.max()-tinc:df_interpol.index.max()])
mean3 = df_interpol.loc[df_interpol.index.max()-tinc:df_interpol.index.max()].mean()
mean3=mean3.values.tolist()[0]
actavgs.append(mean3)
print(actavgs[2])

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

act1meta = [x.min() + (tinc/2), actavgs[0]]
act2meta = [x.min() + tinc + (tinc/2), actavgs[1]]
act3meta = [x.min() + tinc + tinc + (tinc/2), actavgs[2]]

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