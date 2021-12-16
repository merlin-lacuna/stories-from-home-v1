import pandas as pd
import os
import openai
import json
from dotenv import load_dotenv

df = pd.read_csv("data/co2_manu_lastdecade_sorted.csv")
counter = 0
months = ['Nothing','January','February','March','April','May','June','July','August','September','October','November', 'December']
avghist = []
judgement = "Peace"
extras = ""
increases = 0

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
    stats = ""


    avghist.append(average)

    if (counter > 0):
        if (average == avghist[counter-1]):
            judgement = "Peace"
            increases = 0
        elif (average > avghist[counter-1]):
            increases = increases + 1
            judgement = "Fear"
        elif(average < avghist[counter-1]):
            judgement = "Happiness"
            increases = 0

    if (increases > 4):
        judgement = "Violence"
        increases = 0

    completion=oa.Completion.create(
        engine="davinci",
        prompt=f"Topic: Peace\nShortFable: Gaia is sleeping, the mountain, the clouds, and the oceans whisper soothing poems into her ear.  The air is calm . It embraces all of her children  and caresses them gently.\n###\nTopic: Happiness\nShortFable:  Slowly Gaia wakes up, the sun is talking to her. He brings good news: \"The air gave you a gift today\" he says. He shows her a beautify blue sky that the air has painted. Gaia smiles.\n###\nTopic: Fear\nShortFable: Deep in her bed of stone, Gaia is tossing and turning. The sun has forsaken her. The air is angry at Gaia and everyone else. Everyone is afraid of the air's temper.\n###\nTopic: Violence\nShortFable: Suddenly, the air turns violent. She begins to strangle Gaia. The air has been angry for five long months, and Gaia has done nothing to appease her. The air starts to poison her children and hold the sun as her prisoner.\n###\nTopic: {judgement}\nShortFable:",
        temperature=0.7,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0,
        stop=["###"]
    )

    # print the completion
    story = completion.choices[0].text
    stats = f"[LM:{avghist[counter-1]},CM:{average},INC:{increases}, Tone:{judgement}] "
    print(stats,story)
    counter = counter + 1



