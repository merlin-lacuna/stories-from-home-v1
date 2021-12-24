import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

oa = openai

start_sequence = "\nBob:"
restart_sequence = "\nBarry:"
x = 0
bobsanswer = ""
barrysanswer = ""
theanswer = ""
turns = ["bob","barry","bob","barry"]

conversation = ["The following is a conversation between two dwarves who are angry about the price of gold.\n",
                "\nBob: The price of gold is too damn high! Don't you agree Barry?",
                "\nBarry: Totally mate, I can't afford any more gold for my treasury.",
                "\nBob: What do you think we should do about it?"
                "\nBarry: Let's form a miners guild, we'll get the best miners in our lands and put pressure on the gold merchants.",
                ]

while x < 11:
    if(len(turns) - 1) == "bob":
        start_sequence = "\nBarry:"
        restart_sequence = "\nBob:"
        turns.append("barry")
    elif(len(turns) - 1) == "barry":
        start_sequence = "\nBarry:"
        restart_sequence = "\nBob:"
        turns.append("bob")
    else:
        start_sequence = "\nGarry:"
        restart_sequence = "\Murray:"

    theprompt = "".join(conversation) + start_sequence

    completion=oa.Completion.create(
      engine="davinci",
      prompt=theprompt,
      temperature=0.9,
      max_tokens=150,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0.6,
      stop=["\n", "Bob:", "Barry:"]
    )

    theanswer = completion.choices[0].text
    print(theanswer)

    conversation.append(theanswer + restart_sequence)
    x = x + 1

for c in conversation
    print(c)



##

# start_sequence = "\nBarry:"
# restart_sequence = "\nBob:"
#
# completion=oa.Completion.create(
#   engine="davinci",
#   prompt="The following is a conversation between two dwarves who are angry about the price of gold.\n\nBob: The price of gold is too damn high! Don't you agree Barry?\nBarry: Totally mate, I can't afford any more gold for my treasury.\nBob: What do you think we should do about it?\nBarry: Let's form a miners guild, we'll get the best miners in our lands and put pressure on the gold merchants." + restart_sequence + bobsanswer + start_sequence,
#   temperature=0.9,
#   max_tokens=150,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0.6,
#   stop=["\n", "Bob:", "Barry:"]
# )
#
# barrysanswer = completion.choices[0].text
# print("Barry:", barrysanswer)

# while x < 11:
#   x = x+1
#   completion = oa.Completion.create(
#     engine="davinci",
#     prompt="The following is a conversation between two dwarves who are angry about the price of gold.\n\nBob: The price of gold is too damn high! Don't you agree Barry?\nBarry: Totally mate, I can't afford any more gold for my treasury.\nBob: What do you think we should do about it? \nBarry: Let's form a miners guild, we'll get the best miners in our lands and put pressure on the gold merchants.\nBob:" + bobsanswer,
#     temperature=0.9,
#     max_tokens=150,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0.6,
#     stop=["\n", "Bob:", "Barry:"]
#   )
#
#   utterance = completion.choices[0].text
#   print("Bob:", utterance)
#
#   ##
#
#   start_sequence = "\nBarry:"
#   restart_sequence = "\nBob: "
#
#   completion = oa.Completion.create(
#     engine="davinci",
#     prompt="The following is a conversation between two dwarves who are angry about the price of gold.\n\nBob: The price of gold is too damn high! Don't you agree Barry?\nBarry: Totally mate, I can't afford any more gold for my treasury.\nBob: What do you think we should do about it?\nBarry:" + barrysanswer,
#     temperature=0.9,
#     max_tokens=150,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0.6,
#     stop=["\n", "Bob:", "Barry:"]
#   )