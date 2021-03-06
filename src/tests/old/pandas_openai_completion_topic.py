import pandas as pd
import os
import openai
import json
from dotenv import load_dotenv
from contextlib import redirect_stdout
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H_%M_%S")

df = pd.read_csv("data/co2_manu_lastdecade_sorted.csv")
counter = 0
months = ['Nothing','January','February','March','April','May','June','July','August','September','October','November', 'December']
avghist = []
judgement = "Peace"
state = ""
extras = ""
increases = 0
generations = []
poems = "ELEMENT: AIR\nElementalPoem:a whisper, a flutter, a gust from the unknown. i shatter while giving rise to forms of existence. infiltrating the pulse of all that lives. unexpected collision of eternal dust. swirling fragments of a plot in the making. heralds from the universe. my touch settles gently sometimes. once fertile expectation, now sterile hope. the cycle of ruthless resistance. i'm an alien substance. a reversible source of gestation. caressing the ground through the touch of this sky. unfolding naked in the shape of the invisible. i don't know who taught me to pervade this land. my reason is pure movement. and gravity, my lover.\n###\nELEMENT: EARTH\nElementalPoem:flowing lymph and resting soil. i cover to protect. i unveil to embrace. layers of sedimented history. stratification of the present. my soul is a rocky concretion, unbreakable in its essence. the past arises upon a future in transition. irrigated by generous drops, blissful sources from the celestial sphere. roots pierce me deeply. and like a howl in the night branches unfold incautiously towards the ether. leaves, meadows, deserts, peaks. vital extensions of an all-encompassing system. sometimes i tremble with fear at an unforeseen shift. contaminated by longing agents. regenerating, endlessly, wounded but alive. it is the nucleus of time.\n###\nELEMENT: FIRE\nElementalPoem:energy as nourishment. i generate the loss of proximity. what is touched by my projections, dissolve and lacerate. a thunder invokes me. a fluorescent effluvium as the response. magmatic dispersions of irrepressible ardour. shades that glow in the dark. my streams streak the contours of the world. i am latent love. an unpredicted yet coveted cataclysm. in my unfolding, i pursue indissoluble alliances. while transcending states, metamorphosis is my vocation. i radiate into the void, a star that burns from eternity. the ancestor of infinite memories. i collapse against the atmosphere by inevitable prescription. but the magic of an eclipse is my confession.\n###\nELEMENT: WATER\nElementalPoem:tides as glimpses of the cosmos. i breathe with liquid oscillations. waves, floods and droughts depict the passage of seasons. i exist in abundance and scarcity. currents tickle my limbs. and flows intertwine wildly. vital beings in perpetual unrest. mating with the whole. yet transparency is my recognition. i reach the bottom of the visible. drenched in the mystery of my composition. providing wetness as a gift and trace. when reality absorbs me. permeable to the stroke of the present. i come from the origin of the world. and from the sky, i let myself befall in languid surrender.\n###"
poemvariant = "\nELEMENT: FIRE\nElementalPoem:"

oa = openai
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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
            state = "nochange"
            poemvariant = "\nELEMENT: AIR\nElementalPoem:"
            increases = 0
        elif (average > avghist[counter-1]):
            state = "increase"
            increases = increases + 1
            poemvariant = "\nELEMENT: EARTH\nElementalPoem:"
        elif(average < avghist[counter-1]):
            state = "decrease"
            poemvariant = "\nELEMENT: WATER\nElementalPoem:"
            increases = 0

    if (increases > 4):
        state = "constant-increase"
        poemvariant = "\nELEMENT: FIRE\nElementalPoem:"
        increases = 0

    finalprompt = poems + poemvariant
    completion=oa.Completion.create(
        engine="davinci",
        prompt=finalprompt,
        temperature=0.7,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0,
        stop=["###"]
    )

    # print the completion
    story = completion.choices[0].text
    shortvariant = poemvariant.replace("\n", " ").replace("ELEMENT: ","").replace("ElementalPoem:","")
    stats = f"[LM:{avghist[counter-1]},CM:{average},INC:{increases},ST:{state}, Element:{shortvariant}] "
    generations.append(stats + story)

    print(stats,story)
    counter = counter + 1

data = '\n'.join(generations)
finalfile = './generations/' + dt_string + '.txt'
with open(finalfile, 'w') as f:
    with redirect_stdout(f):
        print(data)

