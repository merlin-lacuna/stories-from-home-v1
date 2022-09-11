import openai
import streamlit as st
import os
import re

class ml_backend:

    #openai.api_key = st.secrets["OPENAI_API_KEY"]
    openai.api_key = os.getenv("OPENAI_API_KEY")

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

    def generate_text1(self, userPrompt ="Write me a professionally sounding email", start="Dear"):
        """Returns a generated an email using GPT3 with a certain prompt and starting sentence"""

        response = openai.Completion.create(
        engine="davinci",
        prompt=userPrompt + "\n\n" + start,
        temperature=0.71,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.36,
        presence_penalty=0.75
        )
        return response.get("choices")[0]['text']

    def generate_text(self,myprompt, maxt, element):
        response = openai.Completion.create(
            model=element,
            prompt=myprompt,
            temperature=1,
            max_tokens=maxt,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1,
            stop=["ACT1", "ACT2", "ACT3", "ACT4"]
        )
        story = response.choices[0].text

        # START TEST
        # story = "I am a boring story that is a placeholder for testing that uses the model: " + selectedmodel

        lstory = story.replace("\n", " ")
        lstory = lstory.replace("I'm a forest,", "I am")
        lstory = lstory.replace("I am a forest,", "I am")
        lstory = lstory.replace("I'm just a forest,", "I am")
        lstory = lstory.replace("I am just a forest,", "I am")
        lstory = lstory.replace("Forest: ", "")

        return ' '.join(lstory.split())

    def generate_text_test1(self,userPrompt):
        response = "Grandma loves ham"
        return response

    def generate_text_test2(self,userPrompt):
        response = "Apes are gross"
        return response

    def generate_text_test3(self,userPrompt):
        response = "Your dad loves cheese"
        return response


    def replace_spaces_with_pluses(self, sample):
        """Returns a string with each space being replaced with a plus so the email hyperlink can be formatted properly"""
        changed = list(sample)
        for i, c in enumerate(changed):
            if(c == ' ' or c =='  ' or c =='   ' or c=='\n' or c=='\n\n'):
                changed[i] = '+'
        return ''.join(changed)

