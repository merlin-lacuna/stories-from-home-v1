import pandas as pd
import sys
from ruamel.yaml import YAML

df = pd.read_csv('../../source_text/input_prompts.csv', encoding="utf-8")
entityunit = "land_precip"

#### LOAD ENTITY CONFIG
yaml=YAML(typ='safe')
yaml.default_flow_style = False
configfile="../../data/earth_land_ndsi_poland.yaml"

with open(configfile, encoding='utf-8') as f:
   econfig = yaml.load(f)
#### END CONFIG

entity = econfig['entitydescr']['type']
entityadjs = econfig['entitydescr']['descriptor']
entitybio = econfig['entitydescr']['bio']

mood1 = econfig['entitydata']['actmoodlevels']['act1'] * 100

mood2 = econfig['entitydata']['actmoodlevels']['act2'] * 100

mood3 = econfig['entitydata']['actmoodlevels']['act3'] * 100


def get_prompt(skey,dmood,nmood):
    descr = "null"
    narr = "null"

    match = df.loc[df['0'] == skey]
    descr = match[dmood].tolist()[0]
    narr = match[nmood].tolist()[0]

    try:
        print("key ",skey)

    except:
        print("prompt not found")

    return(descr,narr)

prompta1 = get_prompt(entityunit,str(mood1),str(mood1+50))
prompta2 = get_prompt(entityunit,str(mood2),str(mood2+50))
prompta3 = get_prompt(entityunit,str(mood3),str(mood3+50))
print(str(mood1),str(mood1+50))
print(str(mood2),str(mood2+50))
print(str(mood3),str(mood3+50))

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
    "act1l1": "\nAct 1: "  + str(prompta1[0]) + " " + str(prompta1[1]),
    "act1l2": "---",
    "act1p": entity + ": " + str(completiona1),
    "act1e": "---",
    "act2l1": "\nAct 2: " + str(prompta2[0]) + " " + str(prompta2[1]),
    "act2l2": "---",
    "act2p": entity + ": " + str(completiona2),
    "act2e": "---",
    "act3l1": "\nAct 3: " + str(prompta3[0]) + " " + str(prompta3[1]),
    "act3l2": "---",
    "act3p": entity + ": " + str(completiona3),
    "act3e": "---",
}

for w in wprompt:
    print(wprompt[w])

act1final = "'"+str(prompta1[0]) + " " + str(prompta1[1])+"'"
print(act1final)
act2final = "'"+str(prompta2[0]) + " " + str(prompta2[1])+"'"
print(act2final)
act3final = "'"+str(prompta3[0]) + " " + str(prompta3[1])+"'"
print(act3final)

econfig['prompt']['act1descr'] = act1final
econfig['prompt']['act2descr'] = act2final
econfig['prompt']['act3descr'] = act3final

yaml.dump(econfig, sys.stdout)