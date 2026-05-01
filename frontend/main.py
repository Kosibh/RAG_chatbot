## Importing Packages ##
import time
import requests
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page

#--------------------------------------------------------------------------------------------#

# FastAPI server URLs
FASTAPI_URL_FILES = "http://127.0.0.1:8000/upload-files/"
FASTAPI_URL_URLS = "http://127.0.0.1:8000/process-urls/"
FASTAPI_URL_QUERY = "http://127.0.0.1:8000/generate-response/"

#--------------------------------------------------------------------------------------------#

# Page settings
st.set_page_config(page_title='RAG ChatBot', layout='wide', initial_sidebar_state='expanded')

# Hide Streamlit default elements
hide_streamlit_style = """
                       <style>            
                       #MainMenu {visibility: hidden;}            
                       footer {visibility: hidden;}
                       .block-container {padding-top: 2.41rem;}        
                       </style>            
                       """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Hide pages display in sidebar
no_pages_display_in_sidebar_style = """
                                    <style>
                                    div[data-testid="stSidebarNav"] {display: none;}
                                    </style>
                                    """
st.markdown(no_pages_display_in_sidebar_style, unsafe_allow_html=True)

# Title display in a central column
col1, col2, col3, col4, col5 = st.columns([0.2, 0.3, 3, 0.1, 0.4])
with col1:
    pass
with col2:
    pass
with col3:
    st.write('<p style="font-size:320%; color:Green; background-color:Lavender; text-align: center"><strong>RAG ChatBot</strong></p>',
             unsafe_allow_html=True)
with col4:
    pass

st.write('---'*20)
st.write('')

#--------------------------------------------------------------------------------------------#

# clear the chat history from streamlit session state
def clear_history():
    if 'messages' in st.session_state:
        del st.session_state['messages']

#--------------------------------------------------------------------------------------------#

# Sidebar with menu options
st.sidebar.write('')
st.sidebar.write('')

with st.sidebar:
    sidebar_options = option_menu(menu_title=None,
                                  options=['Ask Question', 'About the App'],
                                  icons=['question-circle', 'info-circle'],
                                  default_index=0,
                                  styles={"icon": {"font-size": "14px"},
                                          "nav-link": {"font-size": "15px",
                                                       "text-align": "left",
                                                       "font-weight": "bold"}})

# Sidebar actions for "Ask Question"
if sidebar_options == 'Ask Question':
    with st.sidebar:
        st.write('---'*20)

        upload_data_type = st.selectbox('Upload data:', options=['Local Documents', 'Web URLs'], index=None, placeholder='Load data from...')

        # File upload and URL input moved to the sidebar
        if upload_data_type == 'Local Documents':
            st.write('---')
            uploaded_files = st.file_uploader('Upload files:', type=['pdf', 'docx', 'txt', 'pptx', 'xlsx'], accept_multiple_files=True)

            if uploaded_files:
                st.write('---')
                if st.button("Process Files", key='files'):
                    st.write('---'*30)
                    with st.spinner("'Reading, chunking and embedding file...'"):
                        
                        # Prepare the files to send to FastAPI
                        files_to_upload = [('files', (file.name, file.getvalue(), file.type)) for file in uploaded_files]

                        # Send request to FastAPI
                        response = requests.post(FASTAPI_URL_FILES, files=files_to_upload)

                        if response.status_code == 200:
                            result = response.json()
                            st.write(f'Number of chunks: {result["num_chunks"]}')
                            st.write(f'Embedding cost: ${result["embedding_cost"]:.4f}')
                            st.session_state.data = 101
                            st.write('---')
                            st.success('Data files uploaded, chunked and embedded successfully.')
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")

        elif upload_data_type == 'Web URLs':
            st.write('---')
            url_inputs = st.text_area("Enter Web URLs (max 5).", placeholder="https://example1.com\nhttps://example2.org\nhttps://example3.com")
            urls_list = [url.strip() for url in url_inputs.split("\n") if url.strip()]

            if len(urls_list) > 5:
                st.error("You can only enter up to 5 URLs.")
            elif urls_list:
                st.write('---')
                if st.button("Process URLs", key='urls'):
                    st.write('---'*30)
                    with st.spinner("'Reading, chunking and embedding URLs...'"):
                        
                        # Send URLs to FastAPI for processing
                        payload = {"urls": urls_list}
                        response = requests.post(FASTAPI_URL_URLS, json=payload)

                        if response.status_code == 200:
                            result = response.json()
                            st.write(f'Number of chunks: {result["num_chunks"]}')
                            st.write(f'Embedding cost: ${result["embedding_cost"]:.4f}')
                            st.session_state.data = 101
                            st.write('---')
                            st.success('Web URLs uploaded, chunked and embedded successfully.')
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")
            else:
                pass

    if 'data' in st.session_state:
        # initialize chat history
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message['role'] == 'user':
                    st.markdown(message["content"])
                else:
                    st.markdown(message["content"])
                    st.write(f'***Referred:*** *{message["source_file"]}*')

        
        # user's question text input widget
        prompt = st.chat_input('Ask Something...', key='ques')
        
        if prompt:
            # Prepare the payload as JSON
            payload = {"query": prompt}

            # Send the query to the FastAPI endpoint
            response = requests.post("http://127.0.0.1:8000/generate-response/", json=payload)

        
            if response.status_code == 200:
                response_data = response.json()
                response_answer = response_data["answer"]
                response_source = response_data["sources"]

                # display user response in chat message container
                with st.chat_message("user"):
                    st.write(prompt)

                # add user message to chat history
                st.session_state.messages.append({'role': 'user', 'content':prompt, 'source_file':''})

                # display assistant response in chat message container
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""

                    # Simulate stream of response with milliseconds 
                    for chunk in response_answer.split():
                        full_response += chunk + " "
                        time.sleep(0.05)

                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")

                    message_placeholder.markdown(full_response)
                    st.write(f'***Referred:*** *{response_source}*')

                # add assistant message to chat history
                st.session_state.messages.append({'role': 'assistant', 'content':full_response, 'source_file': response_source})
        
                with st.sidebar:
                    st.write('---'*20)
                    history_button = st.button('Clear Chat History', on_click=clear_history)

    else:
        without_data_ask = st.chat_input('Ask Something...')
        if without_data_ask:
            st.error('Please upload and add your data...', icon='👈')


# about the app page
elif sidebar_options == 'About the App':
    switch_page('about')

else:
    pass

