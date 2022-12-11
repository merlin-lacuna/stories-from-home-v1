from ruamel.yaml import YAML

searchkey = 'land_cover'
moodrange = (4,3,2)

#### LOAD ENTITY CONFIG
yaml=YAML(typ='safe')
yaml.default_flow_style = False

promptfile="../source_text/input_prompts.yml"
configfile=r"..\data\earth_land_landcover_seoul.yaml"

with open(promptfile, encoding='utf-8') as f:
   promptyaml = yaml.load(f)

with open(configfile, encoding='utf-8') as g:
   econfig = yaml.load(g)

#print(promptyaml)
for m in range(3):
    md = moodrange[m]
    for p in range(len(promptyaml)):
        pr = promptyaml[p]
        ind = str(pr['index'])
        # print(ind[1:2])
        fi = int(ind[1:2])
        if fi == 0:
           fii =  pr['index'] / 100
           if md == fii:
              pre = promptyaml[p + 1]
              print(pr[searchkey]+pre[searchkey])
              actind = m+1
              actlb = 'act0descr'
              actlb = actlb.replace('0',str(actind))
              # Need add to act 'ACTx: ' prompt
              print(actlb)
              econfig['prompt'][actlb] = pr[searchkey]+pre[searchkey]
        # listOfKeys = [key for (key, value) in p.items() if value == 100]
        # try:
        #     lk = listOfKeys[0]
        #     print(p[lk])
        # except:
        #     continue
with open(configfile, 'w', encoding='utf-8') as g:
    yaml.dump(econfig, g)

