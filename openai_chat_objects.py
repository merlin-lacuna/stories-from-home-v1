import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nBob:"
restart_sequence = "\nBarry: "

response = openai.Completion.create(
  engine="davinci",
  prompt="The following is a conversation between two dwarves who are angry about the price of gold.\n\nBob: The price of gold is too damn high! Don't you agree Barry?\nBarry: Totally mate, I can't afford any more gold for my treasury.\nBob: What do you think we should do about it? \nBarry: Let's form a miners guild, we'll get the best miners in our lands and put pressure on the gold merchants.",
  temperature=0.9,
  max_tokens=150,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0.6,
  stop=["\n", "Bob:", "Barry:"]
)

{"prompt":"The following is a conversation between two dwarves who are angry about the price of gold.\n\nBob: The price of gold is too damn high! Don't you agree Barry?\nBarry: Totally mate, I can't afford any more gold for my treasury.\nBob: What do you think we should do about it? \nBarry: Let's form a miners guild, we'll get the best miners in our lands and put pressure on the gold merchants.\nBob:","max_tokens":150,"temperature":0.9,"top_p":1,"frequency_penalty":0,"presence_penalty":0.6,"best_of":1,"echo":true,"logprobs":0,"stop":["\n","Bob:","Barry:"],"stream":true}

print("R:", response.choices)