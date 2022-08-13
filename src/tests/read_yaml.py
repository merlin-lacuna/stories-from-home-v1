import yaml

with open("../../data/fire_forestfire_nvdi_mendocino.yml", mode="rt", encoding="utf-8") as file:
   data = yaml.safe_load(file)
   print(data['idealranges'])