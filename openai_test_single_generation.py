import openai
import os
from dotenv import load_dotenv
from contextlib import redirect_stdout
from datetime import datetime
load_dotenv()

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H_%M_%S")
gentype = ''

oa = openai
oa.api_key = os.getenv("OPENAI_API_KEY")

# DAVID FOSTER WALLACE PROMPT
# gentype = 'fosterwallace'
# completion = oa.Completion.create(
#     engine="text-davinci-001",
#     prompt="Write a story in the style of David Foster Wallace written from the perspective of a volcano.",
#     temperature=1,
#     max_tokens=60,
#     top_p=1,
#     frequency_penalty=0.5,
#     presence_penalty=0.5
# )

# 10 TONES PROMPT
gentype = '10tones'
completion = oa.Completion.create(
  engine="text-davinci-001",
  prompt="EmotionLevel: 1\nKeywords: wail, redemption, sorrow, delight, soul, peak, turmoil\nMicroPoem: A wail of redemption, of sorrow, or delight perhaps? My soul, the ancient peak, stands in turmoil.\n    \nEmotionLevel: 2\nKeywords: magma, deeds, man, gestures, nature, oneness\nMicroPoem: Among magma, the deeds of man and the gestures of nature become oneness.\n\nEmotionLevel: 3\nKeywords: spectrum, knowledge, life, unexpected\nMicroPoem: The spectrum of knowledge blurs by exposing life to the unexpected.\n\nEmotionLevel: 4\nKeywords: fire, past, future, plural, flame, heart\nMicroPoem: I wonder about fire, does it come from the past or the future or plural? Entrusting the flame? I struggle with my heart.\n\nEmotionLevel: 5\nKeywords: melting, earth, cracks\nMicroPoem: The melting will be embracing, earth is whispering in my cracks.\n\nEmotionLevel: 1\nKeywords: love, ocean, wind, ice\nMicroPoem:",
  temperature=0.8,
  max_tokens=120,
  top_p=1,
  frequency_penalty=0.5,
  presence_penalty=0,
  stop=["EmotionLevel:"]
)

# print the completion
story = completion.choices[0].text
print(story)

finalfile = './generations/' + dt_string + '_' + gentype + '.txt'
with open(finalfile, 'w') as f:
    with redirect_stdout(f):
        print(story)