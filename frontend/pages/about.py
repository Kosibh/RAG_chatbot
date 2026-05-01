## Importing Packages ##

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page

#---------------------------------------------------------------------------------------------#

## Page Settings ##
st.set_page_config(page_title='Homepage', layout='wide', initial_sidebar_state='expanded')


hide_streamlit_style = """            
                       <style>            
                       #MainMenu {visibility: hidden;}            
                       footer {visibility: hidden;}
                       .block-container {padding-top: 2.41rem;}        
                       </style>            
                       """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


no_pages_display_in_sidebar_style = """
                                    <style>
                                    div[data-testid="stSidebarNav"] {display: none;}
                                    </style>
                                    """
st.markdown(no_pages_display_in_sidebar_style, unsafe_allow_html=True)


col1, col2, col3, col4, col5 = st.columns([0.2,0.3,3,0.1,0.4])

with col1:
    pass

with col2:
    pass

# Title
with col3:
    st.write('<p style="font-size:320%; color:Green; background-color:Lavender; text-align: center"><strong> RAG ChatBot </strong></p>',
               unsafe_allow_html=True)

with col4:
    pass

st.write('---'*20)
st.write('')

#--------------------------------------------------------------------------------------------#

## adding sidebar ##
st.sidebar.write('')
st.sidebar.write('')

with st.sidebar:

    sidebar_options = option_menu(menu_title = None, 
                                  options = ['Ask Question', 'About the App'],
                                  
                                  icons = ['data', 'data'],
                                  default_index=1,
                           
                                  styles = {"icon": {"font-size": "14px"},
                                     
                                            "nav-link": {"font-size": "15px",
                                                         "text-align": "left",
                                                         "font-weight": "bold"}
                                           })


# adding sidebar actions
if sidebar_options == 'About the App':
    st.success("###### This is a RAG ChatBot application built using Streamlit, FastAPI, and OpenAI embeddings for document and URL-based Q&A functionality.")


elif sidebar_options == 'Ask Question':
    switch_page('main')



else:
    pass