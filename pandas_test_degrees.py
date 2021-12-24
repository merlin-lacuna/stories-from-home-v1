import pandas as pd
df = pd.read_csv("data/co2_manu_lastdecade_sorted.csv")
counter = 0
months = ['Nothing','January','February','March','April','May','June','July','August','September','October','November', 'December']
avghist = []
judgement = ""
extras = ""
increases = 0
reldegree = 0
totaldegree = 0
state = "didn't change"

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
            state = "didn't change"
            reldegree = 0
            totaldegree = round((1 -(avghist[0] / average)) * 100, 2)
            judgement = "We had the same level of Co2 as last month. It's still"
            increases = 0
        elif (average > avghist[counter-1]):
            state = "increased"
            reldegree = round((1 -(avghist[counter-1] / average)) * 100, 2)
            totaldegree = round((1 -(avghist[0] / average)) * 100, 2)
            increases = increases + 1
            judgement = f"There was a {reldegree}% increase in Co2 compared to last month. It has increased by {totaldegree}% since the start of this data."
        elif(average < avghist[counter-1]):
            state = "decreased"
            reldegree =  round((1 -(average / avghist[counter-1])) * 100, 2)
            totaldegree = round((1 - (avghist[0] / average)) * 100, 2)
            judgement = f"There was a {reldegree}% decrease in Co2 compared to last month, but it has increased by {totaldegree}% since the start of this data."
            increases = 0

    if (increases > 4):
        state = "steady increase"
        extras = ". Holy shit, the Co2 levels increased 5 months in a row."
        increases = 0

    print(f"In the year {year}, the {monthtext} Co2 levels at Manu Loa were {average} units on average. {judgement}{extras}")
    extras=""
    counter = counter + 1



