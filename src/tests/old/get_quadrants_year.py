import os
import pandas as pd
from datetime import datetime
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from statistics import mean


rdf = pd.read_csv("../../data/water_ocean_phlevel_globalsea.csv")
sph = rdf['sea_ph']
tl = len(rdf['Year'])

df = rdf.copy()
df['Year'] = pd.to_datetime(df['Year'], format='%Y')
df.set_index('Year', inplace=True)
print(df.head(4))

print("INTERPOL")
df_interpol = df.resample('Y').mean()
df_interpol['sea_ph'] = df_interpol['sea_ph'].interpolate()
print(df_interpol.head(4))

if tl % 3 == 0:
    print("Divisble by 3")
    print("Len: ", tl, " Act increment: ", tl / 3)
else:
    print("Not divisble by 3")
    print("Len: ", tl, " Act increment: ", int(tl / 3))
    print("Test 2.8: ", tl, " Act increment: ", round(2.8))


print(sph)
nrmax = sph.max()
nrmin = sph.min()
print("max: ", nrmax,"min: ", nrmin)

increment = (nrmax - nrmin) / 5
print(increment)
segments = [nrmin, nrmin + (increment * 1), nrmin + (increment * 2), nrmin + (increment * 3) , nrmin + (increment * 4), nrmax]
print(segments)
seg = round(tl / 3)

tspan = df_interpol.index.max() - df_interpol.index.min()
tinc = tspan / 3

print("MaxY-min: ",tspan, tinc)

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


x = df_interpol.index
y = df_interpol['sea_ph']

idealmin = 8.18
idealmax = 8.20

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
plt.ylim([ysmin,ysmax])

plt.axvline(x=x.min() + tinc, color='black', linestyle='-')
plt.axvline(x=x.max() - tinc, color='black', linestyle='-')

plt.axhline(y=idealmin, color='blue', linestyle='-')
plt.axhline(y=idealmax, color='red', linestyle='-')

plt.axhline(y=segments[1], color='darkred', linestyle='--')
plt.axhline(y=segments[2], color='orangered', linestyle='--')
plt.axhline(y=segments[3], color='gold', linestyle='--')
plt.axhline(y=segments[4], color='olivedrab', linestyle='--')
plt.axhline(y=segments[5], color='turquoise', linestyle='--')

plt.plot(x.min() + (tinc/2), actavgs[0], marker="D", markersize=10, markeredgecolor="white", markerfacecolor="black")
plt.plot(x.min() + tinc + (tinc/2), actavgs[1], marker="D", markersize=10, markeredgecolor="white", markerfacecolor="black")
plt.plot(x.min() + tinc + tinc + (tinc/2), actavgs[2], marker="D", markersize=10, markeredgecolor="white", markerfacecolor="black")

plt.title("ocean_phlevel_globalsea")
plt.xlabel("Time")
plt.ylabel("Measurement")
plt.show()




# if segments[0] <= a <= segments[1]:
#     print("Mood 5")
# elif segments[1] <= a <= segments[2]:
#     print("Mood 4")
# elif segments[2] <= a <= segments[3]:
#     print("Mood 3")
# elif segments[3] <= a <= segments[4]:
#     print("Mood 2")
# elif segments[4] <= a <= segments[5]:
#     print("Mood 1")