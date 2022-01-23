import openai
import os
from dotenv import load_dotenv
from contextlib import redirect_stdout
from datetime import datetime
load_dotenv()

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H_%M_%S")
gentype = 'fosterwallace'

oa = openai
oa.api_key = os.getenv("OPENAI_API_KEY")
completion = oa.Completion.create(
    engine="text-davinci-001",
    prompt="Write a story in the style of David Foster Wallace written from the perspective of a volcano.",
    temperature=1,
    max_tokens=600,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0.5
)

# print the completion
story = completion.choices[0].text
print(story)

finalfile = './generations/' + dt_string + gentype + '.txt'
with open(finalfile, 'w') as f:
    with redirect_stdout(f):
        print(story)