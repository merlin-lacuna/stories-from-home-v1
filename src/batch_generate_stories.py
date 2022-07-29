import os
import re
import openai
import datetime
from contextlib import redirect_stdout

oa = openai
oa.api_key = os.getenv("OPENAI_API_KEY")

earth = "davinci:ft-personal-2022-05-08-13-37-54"
water = "davinci:ft-personal:water-2022-03-31-23-56-04"
fire = "davinci:ft-personal:fire-2022-07-06-02-12-31"
air = "davinci:ft-personal:air-2022-07-05-23-19-23"

maxlength = 256
selectedmodel = earth

def trim_output(completion):
    try:
        if completion[-1] in ('.', '?', '!'):
            # print("matched end")
            trimmedoutput = completion
        else:
            try:
                # print("matched incomplete")
                re.findall(r'(\.|\?|\!)( [A-Z])', completion)
                indices = [(m.start(0), m.end(0)) for m in re.finditer(r'(\.|\?|\!)( [A-Z])', completion)]
                splittuple = indices[len(indices) - 1]
                trimmedoutput = completion[0:splittuple[0] + 1]
            except:
                trimmedoutput = completion
    except:
        trimmedoutput = completion

    return trimmedoutput


def get_act(myprompt, maxt, element):
    response = openai.Completion.create(
        model=element,
        prompt=myprompt,
        temperature=1,
        max_tokens=maxt,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1,
        stop=["Act "]
    )

    story = response.choices[0].text

    lstory = story.replace("\n", " ")
    lstory = lstory.replace("I'm a forest,", "I am")
    lstory = lstory.replace("I am a forest,", "I am")
    lstory = lstory.replace("I'm just a forest,", "I am")
    lstory = lstory.replace("I am just a forest,", "I am")
    lstory = lstory.replace("Forest: ","")

    return ' '.join(lstory.split())

gentype = "b2w_forest"

intro = "The following play reveals the inner monologue of a lush but pensive forest. It is divided into several acts. Throughout these acts, the forest describes its inner and outer transformation:\n\nThe inner monologue starts like this:\n\n"

act0descr = "Act 0 synopsis: The forest's leaf cover is not yet known. The forest introduces itself and talks about its surroundings...\n\nForest: \"My home is quite pleasant, with warm summers and cool winters. I see a fair amount of rainfall, which helps to keep my vegetation healthy and lush.\n\n"

act1descr = "Act 1 synopsis: The forest can't seem to stop losing leaves...\n\nForest: \"I float in between questions with no answers, wondering to the sky, to the clouds, to the grass if they witnessed anything that I failed to see"

act2descr = "Act 2 synopsis: The forest has lost a dramatically high proportion of its leaves and greenery...\n\nForest: \"I notice that all the living parts that once composed my abundance are dropping to the ground, victims of an ineluctable and merciless force of gravity"

act3descr = "Act 3 synopsis: The forest has lost more leaves than it has ever lost before in its lifetime...\n\nForest: \"I realize that the earth is cravingly swallowing my essence and I whisper whether at least all around my dissipation will rise a fertile micro-universe, or whether my collapse will lead only to sterile hopes"

for x in range(2):
    # GET PROMPT FOR ACT1
    prompt = intro + act0descr + act1descr
    print("\n\n<PROMPT>")
    print(prompt)
    print("</PROMPT>\n\n")
    act1raw = get_act(prompt, maxlength, selectedmodel)
    act1 = trim_output(act1raw)
    # print(act1)
    act1static = act1 + '\n\n'

    # GET PROMPT FOR ACT2
    prompt = intro + act0descr + act1descr +  act1static + act2descr
    print("\n\n<PROMPT>")
    print(prompt)
    print("</PROMPT>\n\n")
    act2raw = get_act(prompt, maxlength, selectedmodel)
    # print(act2raw)
    act2 = trim_output(act2raw)
    # print(act2)
    act2static = act2 + '\n\n'

    # GET PROMPT FOR ACT3
    prompt = intro + act0descr + act1descr + act1static + act2descr + act2static + act3descr
    print("\n\n<PROMPT>")
    print(prompt)
    print("</PROMPT>\n\n")
    act3raw = get_act(prompt, maxlength, selectedmodel)
    act3 = trim_output(act3raw)

    story = '\nAct 1: ' + act1static + 'Act 2: ' + act2static + 'Act 3: ' + act3

    # datetime object containing current date and time
    dt_string = datetime.datetime.now().strftime("%d-%m-%Y_%H_%M_%S")

    print('-----------')
    print('\n\n\nSample #' + dt_string + ":")
    print(story)

    finalfile = '../generations/' + dt_string + '_' + gentype + '.txt'

    try:
        with open(finalfile, 'w', encoding="utf-8") as f:
            with redirect_stdout(f):
                print(story)
    except:
        print("File write error")