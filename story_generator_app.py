import streamlit as st
import openai
from ml_backend import ml_backend
import os
import re
import openai
import datetime
from contextlib import redirect_stdout
import sys
from ruamel.yaml import YAML
from PIL import Image

st.title("Story Generator")

files = os.listdir('data')

option = st.selectbox(
     'Select your config file ',
     files)

st.write('You selected:', option)

st.markdown("Generate Story")

backend = ml_backend()

#### LOAD ENTITY CONFIG
yaml=YAML(typ='safe')
yaml.default_flow_style = False
configfile="./data/water_land_ndwi_hongkong.yaml"
sessionfile="./data/session.yaml"

with open(configfile, encoding='utf-8') as f:
   econfig = yaml.load(f)
#### END CONFIG

#### START SESSION VARS
if 'ouput1' not in st.session_state:
    st.session_state.ouput1 = 'awaiting output...'
if 'ouput2' not in st.session_state:
    st.session_state.ouput2 = 'awaiting output...'
if 'ouput3' not in st.session_state:
    st.session_state.ouput3 = 'awaiting output...'

oa = openai
oa.api_key = os.getenv("OPENAI_API_KEY")

maxlength = 256
elementmodel = econfig['entitydescr']['element']
gentype = econfig['entitydescr']['id']
gencount = 1
selectedmodel = "unknown"

if elementmodel == "earth":
   selectedmodel = "davinci:ft-personal-2022-05-08-13-37-54"
elif elementmodel == "water":
   selectedmodel =  "davinci:ft-personal:water-2022-03-31-23-56-04"
elif elementmodel == "fire":
   selectedmodel = "davinci:ft-personal:fire-2022-07-06-02-12-31"
elif elementmodel == "air":
   selectedmodel = "davinci:ft-personal:air-2022-07-05-23-19-23"
else:
   selectedmodel = "unknown"
   print("Selected model is unknown")

### READ YAML DATA
intro = econfig['prompt']['intro']
entitybio = econfig['entitydescr']['bio']
chartloc = econfig['entitydata']['chartstorage']
act0descr = econfig['prompt']['act0descr']
act1descr = econfig['prompt']['act1descr']
act2descr = econfig['prompt']['act2descr']
act3descr = econfig['prompt']['act3descr']
entitytype = str(econfig['entitydescr']['type'])
etypeupper = entitytype.upper()

image = Image.open("charts/" + chartloc)
st.image(image, caption='Data Chart')



act0rawprompt  = intro + act0descr + entitybio
act0prettyprompt = intro.replace('\\n','\n') + act0descr.replace('\\n','\n') +  entitybio

act1rawprompt = act1descr
act1prettyprompt = act1descr.replace('\\n',' \n')
### END READ YAML DATA


with st.form(key="form"):
    output1 = ''
    introf = st.text_area('Intro', act0prettyprompt, height=300)
    act1desc = st.text_area('Act 1', act1prettyprompt, height=150)

    submit_act1 = st.form_submit_button(label='Generate Act1')
    if submit_act1:
        with st.spinner("Generating Act..."):
            output1 = backend.generate_text_test1(introf)
        st.session_state.ouput1 = output1
        #st.write('Output1 = ', st.session_state.ouput1)

    act1static = etypeupper + ': some output...'
    act1res = st.text(etypeupper + ': ' + st.session_state.ouput1)


with st.form(key="form2"):
    output2 = ''
    act2rawprompt = act1rawprompt + act1static + '\\n\\n' + act2descr
    act2prettyprompt = act2descr.replace('\\n', '\n')
    act2static = etypeupper + ': some output...'
    act2desc = st.text_area('Act 2', act2prettyprompt, height=150)
    submit_act2 = st.form_submit_button(label='Generate Act2')
    if submit_act2:
        with st.spinner("Generating Act..."):
            output2 = backend.generate_text_test2(act2rawprompt)
        st.session_state.ouput2 = output2
        #st.write('Output2 = ', st.session_state.ouput2)

    act2res = st.text(etypeupper + ': ' + st.session_state.ouput2)


with st.form(key="form3"):
    output3 = ''
    act3rawprompt = act3descr
    act3prettyprompt = act3descr.replace('\\n', '\n')
    act3static = etypeupper + ': some output...'
    act3desc = st.text_area('Act 3', act3prettyprompt, height=150)
    submit_act3 = st.form_submit_button(label='Generate Act3')
    #act3res = st.text(act3static)
    if submit_act3:
        with st.spinner("Generating Act..."):
            output3 = backend.generate_text_test3(act3rawprompt)
        st.session_state.ouput3 = output3
        #st.write('Output3 = ', st.session_state.ouput3)

    act2res = st.text(etypeupper + ': ' + st.session_state.ouput3)

with st.form(key="form4"):
    show_story = st.form_submit_button(label='Show final story')
    if show_story:
        st.markdown(st.session_state.ouput1)
        st.markdown(st.session_state.ouput2)
        st.markdown(st.session_state.ouput3)