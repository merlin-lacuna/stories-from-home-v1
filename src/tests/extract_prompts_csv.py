import pandas as pd

df = pd.read_csv('../../source_text/input_prompts.csv', encoding="utf-8")
entity = "Land"
entityunit = "forest_lai"
entityadjs = "large and complex"
entitybio = "My home is quite pleasant, with warm summers and cool winters. I see a fair amount of rainfall, which helps to keep my vegetation healthy and lush. Rare species of birds make their homes inside me"

def get_prompt(skey,dmood,nmood):
    descr = "null"
    narr = "null"
    try:
        print("key ",skey)
        match = df.loc[df['0'] == skey]
        descr= match[dmood].tolist()[0]
        narr = match[nmood].tolist()[0]
    except:
        print("prompt not found")

    return(descr,narr)

prompta1 = get_prompt(entityunit,'100','150')
prompta2 = get_prompt(entityunit,'300','350')
prompta3 = get_prompt(entityunit,'200','250')

completiona1 = "I feel... <placeholder for AI text for Act 1>"
completiona2 = "I feel... <placeholder for AI text for Act 2>"
completiona3 = "I feel... <placeholder for AI text for Act 3>"

wprompt = {
    "introl1": f"The following play reveals the inner monologue of a {entityadjs} {entity.lower()}. It is divided into several acts. Throughout these acts, the {entity.lower()} describes its inner and outer transformation:\n",
    "introl2": "The first act starts like this:\n",
    "act0l1": f"Act 0: The {entity.lower()} introduces itself and describes its surroundings.",
    "act0l2": "---",
    "act0p": entity + ": " + entitybio,
    "act0e": "---",
    "act1l1": "\nAct 1: "  + prompta1[0] + " " + prompta1[1],
    "act1l2": "---",
    "act1p": entity + ": " + completiona1,
    "act1e": "---",
    "act2l1": "\nAct 2: " + prompta2[0] + " " + prompta2[1],
    "act2l2": "---",
    "act2p": entity + ": " + completiona2,
    "act2e": "---",
    "act3l1": "\nAct 3: " + prompta3[0] + " " + prompta3[1],
    "act3l2": "---",
    "act3p": entity + ": " + completiona3,
    "act3e": "---",
}

for w in wprompt:
    print(wprompt[w])