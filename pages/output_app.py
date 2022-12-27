import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="AI Output", page_icon="📖")
st.markdown("<h1>AI Output</h1>",unsafe_allow_html=True)
st.sidebar.header("AI Output")

def load_chart(chartstorage):
    ### Try to load the appropriate chart image from
    imgpath = "charts/" + chartstorage
    try:
        image = Image.open(imgpath)
    except:
        image = Image.open("charts/chart_not_ready.png")
        st.write(f'{imgpath} does not appear to exist')
        # st.image(image, caption='Data Chart')
    ###################
    return image

df = pd.read_csv("streamlit_db.csv")
for index, row in df.iterrows():
    result = df.loc[index]
    fieldname = result['field']
    if fieldname[:6] == 'entity':
        if fieldname[:16] == 'entitydata_chart':
            st.markdown(f" <h5>{fieldname.replace('entitydata_','')}:</h5>", unsafe_allow_html=True)
            image = load_chart(result['value'])
            st.image(image, caption='Data Chart')
        else:
            st.markdown(f" <h5>{fieldname.replace('entitydata_','').replace('entitydescr_','')}:</h5>{result['value']}", unsafe_allow_html=True)
    elif fieldname == 'storygenerations':
        continue
    elif fieldname[:6] == 'prompt':
        st.markdown(f"<h4>{fieldname}:</h4> \n\n {result['value']} ",unsafe_allow_html=True)
    else:
        st.markdown(f"<h3>{fieldname}:</h3> \n\n {result['value']} ",unsafe_allow_html=True)
        #st.markdown(f"**{fieldname}:**")
        #st.markdown(f"{result['value']}")