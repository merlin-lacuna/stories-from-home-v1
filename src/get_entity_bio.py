import os
import re
import openai
import datetime
from contextlib import redirect_stdout

oa = openai
oa.api_key = os.getenv("OPENAI_API_KEY")

earth = "davinci:ft-personal-2022-05-08-13-37-54"
water = "davinci:ft-personal:water-2022-03-31-23-56-04"
fire = "davinci:ft-personal:fire-2022-07-06-02-12-31"
air = "davinci:ft-personal:air-2022-07-05-23-19-23"
davinci = "text-davinci-003"

maxlength = 256
selectedmodel = davinci

def trim_output(completion):
    try:
        if completion[-1] in ('.', '?', '!'):
            # print("matched end")
            trimmedoutput = completion
        else:
            try:
                # print("matched incomplete")
                re.findall(r'(\.|\?|\!)( [A-Z])', completion)
                indices = [(m.start(0), m.end(0)) for m in re.finditer(r'(\.|\?|\!)( [A-Z])', completion)]
                splittuple = indices[len(indices) - 1]
                trimmedoutput = completion[0:splittuple[0] + 1]
            except:
                trimmedoutput = completion
    except:
        trimmedoutput = completion

    return trimmedoutput


def get_bio(myprompt, maxt, element):
    response = openai.Completion.create(
        model=element,
        prompt=myprompt,
        temperature=1,
        max_tokens=maxt,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1,
        stop=["XXX "]
    )
    return response.choices[0].text

entity = "the Nairobi region"
prompt=f"Write a text from the perspective of {entity} describing its own climate and ecology and write it in the first-person tense."

bio = get_bio(prompt, maxlength, selectedmodel)
ft = f"Write the following text in the singular first-person tense:\n" + bio
ftense = get_bio(ft, maxlength, selectedmodel)
#bio2 = get_bio(prompt2, maxlength, selectedmodel)
#bio3 = get_bio(prompt3, maxlength, selectedmodel)
#prompt2=f"Generate an interesting fact about the climate of {entity}."

# prompt3=f"Write a list of ten adjectives that describe {entity}.\n1."
#
# nounsadjinstr = "Extract the nouns and adjectives from the following text:\n" + ftense
# nounsadj = get_bio(nounsadjinstr, maxlength, selectedmodel)
#
# samplepoem = """
# Season of mists and mellow fruitfulness,
# Close bosom-friend of the maturing sun;
# Conspiring with him how to load and bless
# With fruit the vines that round the thatch-eves run;
# To bend with apples the moss’d cottage-trees,
# And fill all fruit with ripeness to the core;
# To swell the gourd, and plump the hazel shells
# With a sweet kernel; to set budding more,
# And still more, later flowers for the bees,
# Until they think warm days will never cease,
# For summer has o’er-brimm’d their clammy cells.
# """
#
poeticinstr = f"Rewrite the following text the in poetic style of Allen Ginsberg:\n###\n{ftense}\n###\n"
poetic = get_bio(poeticinstr, maxlength, selectedmodel)

# poemprompt2 = "Write a poem by Rumi"
# poetic2 = get_bio(poemprompt2, maxlength, selectedmodel)

print("-----BIO RAW-----")
print(bio)
print("-----FIRST PERSON-----")
print(ftense)
print("-----POETIC-----")
print(poetic)
# print("-----POETIC #2-----")
# print(poetic2)