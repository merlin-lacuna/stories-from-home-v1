import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

oa = openai

start_sequence = "\nEntityA:"
restart_sequence = "\nEntityB:"
x = 0
entitya_answer = ""
entityb_answer = ""
theanswer = ""
nextspeaker = "entity-a"

scenario = "The following is a conversation the EntityA and the EntityB. The EntityB feels sick and the EntityA is trying to find out what is wrong.\n"

conversation = [
                "\nEntityA: The price of gold is too damn high! Don't you agree EntityB?",
                "\nEntityB: Totally mate, I can't afford any more gold for my treasury.",
                "\nEntityA: What do you think we should do about it?"
                "\nEntityB: Let's form a miners guild, we'll get the best miners in our lands and put pressure on the gold merchants.",
                ]


while x < 11:
    if(nextspeaker == "entity-a"):
        start_sequence = "\nEntityB:"
        restart_sequence = "\nEntityA:"
        nextspeaker= "entity-b"
    elif(nextspeaker == "entity-b"):
        start_sequence = "\nEntityA:"
        restart_sequence = "\nEntityB:"
        nextspeaker= "entity-a"
    else:
        start_sequence = "\nGarry:"
        restart_sequence = "\Murray:"

    theprompt = scenario + "".join(conversation) + start_sequence

    completion=oa.Completion.create(
      engine="davinci",
      prompt=theprompt,
      temperature=0.9,
      max_tokens=150,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0.6,
      stop=["\n", "EntityA:", "EntityB:"]
    )

    theanswer = completion.choices[0].text
    print(theanswer)

    conversation.append(start_sequence + "" + theanswer)
    x = x + 1

print("------------------------------")
for c in conversation:
    print(c.strip())


##

# start_sequence = "\nEntityB:"
# restart_sequence = "\nEntityA:"
#
# completion=oa.Completion.create(
#   engine="davinci",
#   prompt="The following is a conversation between two dwarves who are angry about the price of gold.\n\nEntityA: The price of gold is too damn high! Don't you agree EntityB?\nEntityB: Totally mate, I can't afford any more gold for my treasury.\nEntityA: What do you think we should do about it?\nEntityB: Let's form a miners guild, we'll get the best miners in our lands and put pressure on the gold merchants." + restart_sequence + entity-asanswer + start_sequence,
#   temperature=0.9,
#   max_tokens=150,
#   top_p=1,
#   frequency_penalty=0,
#   presence_penalty=0.6,
#   stop=["\n", "EntityA:", "EntityB:"]
# )
#
# entity-bsanswer = completion.choices[0].text
# print("EntityB:", entity-bsanswer)

# while x < 11:
#   x = x+1
#   completion = oa.Completion.create(
#     engine="davinci",
#     prompt="The following is a conversation between two dwarves who are angry about the price of gold.\n\nEntityA: The price of gold is too damn high! Don't you agree EntityB?\nEntityB: Totally mate, I can't afford any more gold for my treasury.\nEntityA: What do you think we should do about it? \nEntityB: Let's form a miners guild, we'll get the best miners in our lands and put pressure on the gold merchants.\nEntityA:" + entity-asanswer,
#     temperature=0.9,
#     max_tokens=150,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0.6,
#     stop=["\n", "EntityA:", "EntityB:"]
#   )
#
#   utterance = completion.choices[0].text
#   print("EntityA:", utterance)
#
#   ##
#
#   start_sequence = "\nEntityB:"
#   restart_sequence = "\nEntityA: "
#
#   completion = oa.Completion.create(
#     engine="davinci",
#     prompt="The following is a conversation between two dwarves who are angry about the price of gold.\n\nEntityA: The price of gold is too damn high! Don't you agree EntityB?\nEntityB: Totally mate, I can't afford any more gold for my treasury.\nEntityA: What do you think we should do about it?\nEntityB:" + entity-bsanswer,
#     temperature=0.9,
#     max_tokens=150,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0.6,
#     stop=["\n", "EntityA:", "EntityB:"]
#   )