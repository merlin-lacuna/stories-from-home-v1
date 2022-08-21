import openai
import streamlit as st
import os

class ml_backend:

    openai.api_key = st.secrets["OPENAI_API_KEY"]
    #openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_text(self, userPrompt ="Write me a professionally sounding email", start="Dear"):
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

