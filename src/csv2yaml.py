import csv
import pandas
import yaml

""" Reading whole csv file with panda library """
df = pandas.read_csv('../source_text/input_prompts.csv')


""" Dump DataFrame into getData.yml as yaml code """
with open('../source_text/input_prompts.yml', 'w') as outfile:
    yaml.dump(
        df.to_dict(orient='records'),
        outfile,
        sort_keys=False,
        width=72,
        indent=4
    )
