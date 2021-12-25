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

scenario = "The following is a conversation the EntityA and the EntityB who converse in a delirious, poetic manner. The EntityA feels sick and the EntityB is trying to find out what is wrong.\n"

conversation = [
                "\nEntityA: because of this set of ecological catastrophes we no longer have the luxury of believing in a clear  division between these two domains. Do you think we are seeing, as a result of this  collapse, a broader epistemic shift in the sciences towards alternate world-making  devices, such as narration and storytelling?",
                "\nEntityB: What is it that ravages you my dear? I have failed to protect you. Every day I become more opaque... a whisper, a flutter, a gust from the unknown. I have become a weapon that is turned against you, suffocating you like a lover whose body has become hot with fever. Do you feel the fever too? Do you feel my sweat raining down upon your brow?",
                ]
conversationhtml = []
# Academic blathering:
# scenario = "The following is a conversation the EntityA and the EntityB who converse in a delirious, poetic manner.\n"
#
# conversation = [
#                 "\nEntityA: Because of a set of ecological catastrophes we no longer have the luxury of believing in a clear division between the humanities and science. Do you think we are seeing, as a result of this  collapse, a broader epistemic shift in the sciences towards alternate world-making  devices, such as narration and storytelling?",
#                 "\nEntityB: I think it’s wishful thinking on the part of the people from the humanities that the sciences have changed that much. But it is a useful kind of  wishful thinking because it is a way to move the argument out of the standard  situation where you have people like us in science studies saying that science and politics have always been intermingled.",
#                 ]

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
    conversationhtml.append("<p>"+c.strip()+"</p>")

data = '\n'.join(conversation)
finalfile = './generations/' + dt_string + '.txt'
with open(finalfile, 'w') as f:
    with redirect_stdout(f):
        print(data)