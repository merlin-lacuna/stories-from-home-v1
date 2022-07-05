import os
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def process_file(time, unit, maxval, minval, filename):
  x = time
  y = unit

  try:
    yhat = savgol_filter(y, len(time), 3)
    plt.plot(x, yhat, color='gray')
  except:
      try:
          yhat = savgol_filter(y, len(time)-1, 3)
          plt.plot(x, yhat, color='gray')
      except:
          print("yhat error")

  upperrange = maxval + (maxval * 0.05)
  lowerrange = minval - (minval * 0.05)

  print(lowerrange,upperrange)
  fig = plt.plot(x, y, color='gray', linestyle='dotted')
  plt.title(filename)
  plt.xlabel("Time")
  plt.ylabel("Measurement")

  plt.savefig("../charts/" + filename + ".png", bbox_inches='tight')
  plt.show(block=False)
  plt.pause(1)
  plt.close()

def reverse_graph(dataframe):
  print("UP = BAD: Reversing Graph Direction")
  pmin = dataframe.min()
  dataframe = dataframe - (dataframe * 2)
  mynmin = dataframe.min()
  print(mynmin)
  anmin = abs(mynmin)
  dataframe = dataframe + (anmin + pmin)

  return dataframe

def distfrom_average(dataframe):
  print("NON-AVG = BAD: Measuring Dist from Avg")
  average = df["C0mean"]
  dfmedian = df['C0mean'].median()
  time = df["C0date"]
  df['C0date'] = pd.to_datetime(df['C0date'], infer_datetime_format=True)
  df.set_index('C0date', inplace=True)
  # print(average)
  # print(time)
  # print(df.index)
  dfmean = df["C0mean"]
  dfroll = dfmean.rolling("30D", center=False).mean()
  dfdist = dfroll - dfmean
  dfmdist = dfmedian - dfmean
  dfdist = dfdist.abs()
  dfmdist = dfmdist.abs()
  print(dfdist)

# rdf = pd.read_csv("/content/stories-from-home-v1/data/water_ocean_phlevel_globalsea.csv")
# print(rdf['sea_ph'])
# nrdf = reverse_graph(rdf['sea_ph'])
# nrmax = nrdf.max()
# nrmin = nrdf.min()
# process_file(rdf['Year'],nrdf,nrmax,nrmin)
#
# process_file(rdf['Year'],rdf['sea_ph'],rdf.max(),rdf.min())

df = pd.read_csv("../data/metadata.csv", encoding="utf-8")
df_file = df["Filename"]

df = df.reset_index()  # make sure indexes pair with number of rows

for index, row in df.iterrows():
    #dfname = "df_" + str(row['Index'])
    print(row['Filename'])
    meaning = row['Gooddirection']
    dftemp = pd.read_csv("../data/"+ row['Filename'])
    time = row['Datecol']
    data = row['Datacol']

    try:
      maxval = dftemp[data].max()
    except:
      print("Error matching maxval: ", data)
      maxval = 100

    try:
      minval = dftemp[data].min()
    except:
      print("Error matching minval: ", data)
      minval = 0

    print(time,data,meaning)
    process_file(dftemp[time],dftemp[data],maxval,minval,row['Filename'])

    #try:
    #  process_file(dftemp[time],dftemp[data],maxval,minval)
    #except Exception as e:
    #  print("Could not process file: ",row['Filename'], e)

    #print(len(dftemp))