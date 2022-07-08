import json

with open('../../source_text/input_prompts.json', 'r') as f:
  data = json.load(f)

# Output: {'name': 'Bob', 'languages': ['English', 'French']}
#print(data[0])

# Define a function to search the item

searchkey = 'desert_temp'


for d in data:
 print("data",type(d))
 for p in d:
     pl = p[1]
     pd = json.dumps(p)
     print("loads",type(pl))
     print("dumps",type(pd))
     print(pl)
     #if searchkey == p["n0"]:
     #  return p["n0"]

