import pandas as pd
import os
import openai
import json
from dotenv import load_dotenv

df = pd.read_csv("data/co2_manu_lastdecade_sorted.csv")
counter = 0
months = ['Nothing','January','February','March','April','May','June','July','August','September','October','November', 'December']
avghist = []
tone = "peaceful"
extras = ""
increases = 0
storypromptbase = f"Continue the following story about the earth goddess Gaia. Other characters are: her sister (the air), her husband (the sun), and her children (the mountains, the clouds, and the ocean). The story should be told in the style of Native American folklore. In the story, describe Gaia as a good, loving character. Describe her sister, the air, as an unpredictable character. Write the story with a {tone} tone. Make sure to use at least three sentences."
# storypromptbase = ''.join(storypromptbase)
storypromptextra = ""
wholestory = "\n\nGaia was fast asleep when her sister, the air, came to visit. The air was always unpredictable, and Gaia never knew what she would do next. This time, the air decided to play a trick on Gaia. She blew a gust of wind at her, causing Gaia to awaken.\n\n\"What are you doing?\" Gaia asked her sister.\n\n\"Just playing around,\" the air replied.\n\n\"Be careful, you might wake up my husband, the sun,\" Gaia warned.\n\nThe air just laughed and flew away.",
wholestory = ''.join(wholestory)
completions = [wholestory]
prompt = ""

load_dotenv()
oa = openai
oa.api_key = os.getenv("OPENAI_API_KEY")

print(wholestory.replace("\n"," "))

for index, row in df.iterrows():
    if (counter == 15):
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
            tone = "peaceful"
            storypromptbase = f"Continue the following story about the earth goddess Gaia. Other characters are: her sister (the air), her husband (the sun), and her children (the mountains, the clouds, and the ocean). In the story, describe Gaia as a good, loving character. Describe her sister, the air, as an unpredictable character. Continue the story with a {tone} tone. Continue the story with at least three sentences and describe how everyone was sleeping."
            #storypromptbase = ''.join(storypromptbase)
            increases = 0
        elif (average > avghist[counter-1]):
            state = "Increase"
            increases = increases + 1
            tone = "fearful"
            storypromptbase = f"Continue the following story with a fearful tone and continue the story with at least three sentences that describe some kind of conflict or fight."
            #storypromptbase = ''.join(storypromptbase)
        elif(average < avghist[counter-1]):
            state = "Decrease"
            tone = "happy"
            storypromptbase = f"Continue the following story about the earth goddess Gaia. Other characters are: her sister (the air), her husband (the sun), and her children (the mountains, the clouds, and the ocean). In the story, describe Gaia as a good, loving character. Describe her sister, the air, as an unpredictable character. Continue the story with a {tone} tone and continue the story with at least three sentences that describe some kind of {tone} event."
            #storypromptbase = ''.join(storypromptbase)
            increases = 0

    if (increases > 4):
        state = "5xIncrease"
        tone = "violent"
        storypromptbase = f"Continue the following story with a violent tone and continue the story with at least three sentences that describe some kind of violent struggle."
        #storypromptbase = ''.join(storypromptbase)
        increases = 0

    #print(" \n\nPROMPT BASE:("+storypromptbase+")")
    instructions = storypromptbase + "\n\n" + completions[len(completions)-1]

    #print("INSTRUCTIONS:",instructions)

    completion=oa.Completion.create(
        engine="davinci-instruct-beta-v3",
        prompt=instructions,
        temperature=0.7,
        max_tokens=90,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    # print the completion
    story = completion.choices[0].text
    story = story.replace("\n"," ").replace("  "," ")
    stats = f"[LM:{avghist[counter-1]},CM:{average},INC:{increases},STATUS:{state}]"
    print(stats)
    #print("COMPLETION OBJECT:", completion.choices[0])
    print("COMPLETION:", story)

    #wholestory = wholestory + story
    completions.append(story)
    counter = counter + 1

print("wholestory: \n\n", " ".join(completions).replace("\n"," ").replace("  "," "))