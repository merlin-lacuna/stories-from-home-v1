import pandas as pd
df = pd.read_csv("data/co2_manu_lastdecade_sorted.csv")
counter = 0
months = ['Nothing','January','February','March','April','May','June','July','August','September','October','November', 'December']
avghist = []
judgement = ""
extras = ""
increases = 0

for index, row in df.iterrows():
    # if (counter == 5):
    #     break
    normavg = int(row['average']/10)
    year = int(row['year'])
    month = int(row['month'])
    average = int(row['average'])
    monthtext = months[month]


    avghist.append(average)

    if (counter > 0):
        if (average == avghist[counter-1]):
            judgement = "We had the same level of Co2 as last month"
            increases = 0
        elif (average > avghist[counter-1]):
            increases = increases + 1
            judgement = f"There was more Co2 than last month"
        elif(average < avghist[counter-1]):
            judgement = "The average is actually lower than last month"
            increases = 0

    if (increases > 4):
        extras = ". Holy shit, the Co2 levels increased 5 months in a row."
        increases = 0

    print(f"In the year {year}, the {monthtext} Co2 levels at Manu Loa were {average} units on average. {judgement}{extras}")
    extras=""
    counter = counter + 1



