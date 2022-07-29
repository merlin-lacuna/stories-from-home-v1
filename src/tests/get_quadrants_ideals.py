import os
import pandas as pd
from datetime import datetime
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from statistics import mean

# Define important variables
filebase = "../../data/"
files = [
    ("earth_land_ndsi_thwaites.csv", "Glacier", "ndsi", "ice mass","howling"), #0
    ("earth_land_lai_atismo.csv", "Forest", "lai", "leaf cover","lush and pensive"), #1
    ("air_atmo_airtemp_sahel.csv", "Land", "airtemp", "temperature","vast and complex"), #2
    ("fire_volcano_watertemp_ruapehu.csv", "Volcano", "temp", "temperature", "colossal and simmering"), #3
    ("fire_forestfire_nvdi_mendocino.csv", "Forest", "nvdi", "burning fire", "dry smouldering"), #4
    ("fire_volcano_watertemp_kawahIjen.csv", "Volcano", "temp", "temperature","colossal and simmering"), #5
    ("water_ocean_sealevel_balticsea.csv", "Ocean", "level", "sea level","iridescent rippled"), #6
    ("water_ocean_sealevel_biscay.csv", "Ocean", "level", "sea level","iridescent rippled"), #7
    ("air_atmo_precip_toliara.csv", "Land", "precip", "rainfall","vast and complex"), #8
    ("air_atmo_precip_timbuktu.csv", "Land", "precip", "rainfall","vast and complex"), #9
    ("earth_forest_lai_norr.csv", "Forest", "lai", "leaf cover","lush and pensive"), #10
    ("earth_valley_lcover_hainan.csv", "Island", "area","mass","fertile sultry"), #11
    ("earth_island_lcover_venice.csv", "Island", "area","mass","fertile sultry"), #12
    ("earth_glacier_ndsi_greenland.csv", "Glacier", "ndsi", "ice mass","howling"), #13
    ("air_atmo_C02_manuloa.csv", "Land", "C02", "carbon dioxide levels","clear and pristine"), #14
    ("earth_land_lai_taipokau.csv", "Forest", "lai", "leaf cover","lush and pensive") #15

]# START CUSTOM PARAMS #####################################################################
fileno = 5
idealmin = 36.3
idealmax = 42.2
entitybio = "I am an indonesian volcano."
# END CUSTOM PARAMS #####################################################################

myfile = files[fileno][0]
file = pd.read_csv(filebase + myfile)
fn=myfile.replace(".csv","")
measurement = files[fileno][2]
measuredescr = files[fileno][3]
datacol = "Data"
timecol = "Time"

# START PREP STORY #####################################################################
sdf = pd.read_csv('../../source_text/input_prompts.csv')
entity = files[fileno][1]
entityunit = entity.lower() + "_" + measurement
print("entityunit: ",entityunit)
entityadjs =  files[fileno][4]


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

# Interpolate between consistent HOURLY units if Daily
# df_interpol = df.resample('1H').mean()
# df_interpol[datacol] = df_interpol[datacol].interpolate()

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

# ACT1  - Use averages
act1meta = [x.min() + (tinc / 2), actavgs[0]]
if actmaxs[0] > (actavgs[0] * 1.15) or actmins[0] - (actavgs[0] * 0.85) :
    maxdiff = actmaxs[0] - actavgs[0]
    mindiff = actavgs[0] - actmins[0]

    if (abs(maxdiff)) > (abs(mindiff)):
        # Use maxes
        act1meta = [x.min() + (tinc / 2), actmaxs[0]]

    else:
        if (abs(maxdiff)) < (abs(mindiff)):
            # Use mins
            act1meta = [x.min() + (tinc / 2), actmins[0]]

# ACT2  - Use averages
act2meta = [x.min() + tinc + (tinc/2), actavgs[1]]
if actmaxs[1] > (actavgs[1] * 1.15) or actmins[1] - (actavgs[1] * 0.85) :
    maxdiff = actmaxs[1] - actavgs[1]
    mindiff = actavgs[1] - actmins[1]

    if (abs(maxdiff)) > (abs(mindiff)):
        # Use maxes
        act2meta = [x.min() + tinc + (tinc / 2), actmaxs[1]]

    if (abs(maxdiff)) < (abs(mindiff)):
        # Use mins
        act2meta = [x.min() + tinc + (tinc / 2), actmins[1]]

# ACT3  - Use averages
act3meta = [x.min() + tinc + tinc + (tinc/2), actavgs[2]]
if actmaxs[2] > (actavgs[2] * 1.15) or actmins[2] - (actavgs[2] * 0.85) :
    maxdiff = actmaxs[2] - actavgs[2]
    mindiff = actavgs[2] - actmins[2]
    if (abs(maxdiff)) > (abs(mindiff)):
        # Use maxes
        act3meta = [x.min() + tinc + tinc + (tinc/2), actmaxs[2]]
    if (abs(maxdiff)) < (abs(mindiff)):
        # Use mins
        act3meta = [x.min() + tinc + tinc + (tinc/2), actmins[2]]
        
# MOOD OVERRIDES
# act1meta = [x.min() + (tinc/2), 0.5]
# act2meta = [x.min() + tinc + (tinc/2), 0.6]
# act3meta = [x.min() + tinc + tinc + (tinc/2), 0.7]

# Use averages
# act1meta = [x.min() + (tinc/2), actavgs[0]]
# act2meta = [x.min() + tinc + (tinc/2), actavgs[1]]
# act3meta = [x.min() + tinc + tinc + (tinc/2), actavgs[2]]

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
print(mscale1)
prompta1 = get_prompt(entityunit,str(mscale1),str(mscale1+50))
prompta2 = get_prompt(entityunit,str(mscale2),str(mscale2+50))
prompta3 = get_prompt(entityunit,str(mscale3),str(mscale3+50))

completiona1 = "I feel... <placeholder for AI text for Act 1>"
completiona2 = "I feel... <placeholder for AI text for Act 2>"
completiona3 = "I feel... <placeholder for AI text for Act 3>"

completiona1 = ""
completiona2 = ""
completiona3 = ""

wprompt = {
    "introl1": f"intro = \"The following play reveals the inner monologue of a {entityadjs} {entity.lower()}. It is divided into several acts. Throughout these acts, the {entity.lower()} describes its inner and outer transformation:\\n\\nThe first act starts like this:\\n\"",
    "spacer0": "  ",
    "act0l1": f"act0descr = \"Act 0 description: The {entity.lower()}'s {measuredescr} is not yet known. The {entity.lower()} introduces itself and describes its surroundings.\\n----\\n{entity}: " + entitybio + "\\n\\n\"",
    "spacer1": "  ",
    "act1l1": f"act1descr = \"Act 1: " + str(prompta1[0]) + " " + str(prompta1[1] + f"\\n----\\n{entity}: " + completiona1 + "\""),
    "spacer2": "  ",
    "act1l2": f"act2descr = \"Act 2: " + str(prompta2[0]) + " " + str(prompta2[1] + f"\\n----\\n{entity}: " + completiona2 + "\""),
    "spacer3": "  ",
    "act1l3": f"act3descr = \"Act 3: " + str(prompta3[0]) + " " + str(prompta3[1] + f"\\n----\\n{entity}: " + completiona3 + "\""),
}

for w in wprompt:
    print(wprompt[w])
# END GENERATE TEXT #####################################################################
