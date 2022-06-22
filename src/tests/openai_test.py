import openai
import os
from dotenv import load_dotenv
load_dotenv()

oa = openai
oa.api_key = os.getenv("OPENAI_API_KEY")
completion = oa.Completion.create(
    engine="davinci-instruct-beta-v3",
    prompt=storypromptbase + storypromptextra,
    temperature=0.7,
    max_tokens=90,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0
)

# print the completion
story = completion.choices[0].text