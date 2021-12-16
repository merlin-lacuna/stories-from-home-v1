import pandas as pd
import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
oa = openai
oa.api_key = os.getenv("OPENAI_API_KEY")
df = pd.read_csv("data/co2_manu_lastdecade_sorted.csv")
counter = 0


for index, row in df.iterrows():
    if (counter == 5):
        break
    reducedavg = int(row['average'] / 10)
    print(int(row['year']),int(row['month']),reducedavg )

    # completion=oa.Completion.create(
    #     engine="davinci-instruct-beta",
    #     prompt="Write one sentence only in the style of Norse mythology. Describe how the weather influences our lives. Make sure to end the sentence with a period.",
    #     max_tokens=reducedavg
    #     )
    completion=oa.Completion.create(
        engine="davinci",
        prompt="Topic: Peace\nShortFable: Gaia is sleeping, the mountain, the clouds, and the oceans whisper soothing poems into her ear.  The air is calm . It embraces all of her children  and caresses them gently.\n###\nTopic: Happiness\nShortFable:  Slowly Gaia wakes up, the sun is talking to her. He brings good news: \"The air gave you a gift today\" he says. He shows her a beautify blue sky that the air has painted. Gaia smiles.\n###\nTopic: Fear\nShortFable: Deep in her bed of stone, Gaia is tossing and turning. The sun has forsaken her. The air is angry at Gaia and everyone else. Everyone is afraid of the air's temper.\n###\nTopic: Violence\nShortFable: Suddenly, the air turns violent. She begins to strangle Gaia. The air has been angry for five long months, and Gaia has done nothing to appease her. The air starts to poison her children and hold the sun as her prisoner.\n###\nTopic: Violence\nShortFable:",
        temperature=0.5,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0,
        stop=["###"]
    )

    # print the completion
    print(completion.choices[0].text)
    counter = counter + 1

# Load your API key from an environment variable or secret management service
# openai.api_key = os.getenv("")






