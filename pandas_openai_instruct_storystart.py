import pandas as pd
import os
from dotenv import load_dotenv
import openai
import json

df = pd.read_csv("data/co2_manu_lastdecade_sorted.csv")
counter = 0
months = ['Nothing','January','February','March','April','May','June','July','August','September','October','November', 'December']
avghist = []
judgement = "Peace"
extras = ""
increases = 0
storypromptbase = "Write a short story about the earth goddess Gaia. Other characters should as follows: her sister (the air), her husband (the sun), and her children (the mountains, the clouds, and the ocean). The story should be told in the style of Native American folklore. In the story, describe Gaia as a good, loving character. Describe her sister, the air, as an unpredictable character. "
storypromptextra = "The story should start with Gaia asleep."
wholestory = ""

load_dotenv()
oa = openai
oa.api_key = os.getenv("OPENAI_API_KEY")

for index, row in df.iterrows():
    if (counter == 3):
         break
    normavg = int(row['average']/10)
    year = int(row['year'])
    month = int(row['month'])
    average = int(row['average'])
    monthtext = months[month]
    state = "Neutral"
    stats = ""

    avghist.append(average)

    if (counter > 0):
        if (average == avghist[counter-1]):
            state = "Neutral"
            storypromptextra = "The story should start with Gaia asleep and her sister, the air, whispering poems into her ear. The story should have a peaceful tone. The story should end in a complete sentence."
            increases = 0
        elif (average > avghist[counter-1]):
            state = "Increase"
            increases = increases + 1
            storypromptextra = "The story should start with the air waking up Gaia and yelling angrily. The story should have a fearful tone. The story should end in a complete sentence."
        elif(average < avghist[counter-1]):
            state = "Decrease"
            storypromptextra = "The story should start with the air kissing Gaia and gving her a gift. The story should have a happy tone. The story should end in a complete sentence."
            increases = 0

    if (increases > 4):
        state = "5xIncrease"
        storypromptextra = "The story should start with the air trying to poison Gaia and her children. The story should have a violent tone. The story should end in a complete sentence."
        increases = 0

    completion=oa.Completion.create(
        engine="davinci-instruct-beta-v3",
        prompt=storypromptbase + storypromptextra,
        temperature=0.7,
        max_tokens=90,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    # print the completion
    story = completion.choices[0].text
    stats = f"[LM:{avghist[counter-1]},CM:{average},INC:{increases},STATUS:{state}]"
    print(stats,story)
    counter = counter + 1



