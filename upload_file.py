import streamlit as st
import os
from streamlit_option_menu import option_menu
 
upload = "Client_folder"
#os.makedirs(upload, exist_ok=True)

upload1 ="Poc_folder"
#os.makedirs(upload1, exist_ok=True)

upload2 ="CS_Goals_folder"
#os.makedirs(upload2, exist_ok=True)#

def file_exists(filename):
    return os.path.exists(os.path.join(upload, filename))
def file_exists1(filename):
    return os.path.exists(os.path.join(upload1, filename))
def file_exists2(filename):
    return os.path.exists(os.path.join(upload2, filename))
 
def show_upload_file():
    #st.title("Upload File Page")
 
    col1, col2 = st.columns([14, 2])
    with col1:
        if st.button("🏠 Home"):
            st.session_state.page = "search"
            st.rerun()
    with col2:
        if st.button(":blue[Logout]"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()

        
    hide="""
        <style>
        #MainManu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
        </style>
    """
    st.markdown(hide,unsafe_allow_html=True)
    st.header("Select Directory")
    

    selected=option_menu(menu_title=None,options=["CS Goals Folder","CLIENT FOLDER","POC FOLDER"],icons=["","bi bi-folder","bi bi-folder"],orientation="horizontal",)


    try:
        if selected == "CLIENT FOLDER":
            #File uploaded into uploaded_file folder
            uploaded_file = st.file_uploader("Upload PDF", type='pdf')
            if uploaded_file:
                file_path = os.path.join(upload, uploaded_file.name)
                    # Check if the file already exists
                if file_exists(uploaded_file.name):
                    st.error(f"A file with the name '{uploaded_file.name}' already exists. Please rename the file before uploading.")
                else:
                    # Save the file
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                            #st.session_state["uploaded_file"]=uploaded_file
                    st.success(f"File uploaded successfully: {uploaded_file.name}")
            
                    

        elif selected == "POC FOLDER":
            
            #File uploaded into uploaded_file folder
            uploaded_file = st.file_uploader("Upload PDF", type='pdf')
            if uploaded_file:
                file_path = os.path.join(upload1, uploaded_file.name)
                    # Check if the file already exists
                if file_exists1(uploaded_file.name):
                    st.error(f"A file with the name '{uploaded_file.name}' already exists. Please rename the file before uploading.")
                else:
                    # Save the file
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                            #st.session_state["uploaded_file"]=uploaded_file
                    st.success(f"File uploaded successfully: {uploaded_file.name}")

        elif selected == "CS Goals Folder":
            #File uploaded into uploaded_file folder
            uploaded_file = st.file_uploader("Upload PDF", type='pdf')
            if uploaded_file:
                file_path = os.path.join(upload2, uploaded_file.name)
                    # Check if the file already exists
                if file_exists2(uploaded_file.name):
                    st.error(f"A file with the name '{uploaded_file.name}' already exists. Please rename the file before uploading.")
                else:
                    # Save the file
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                            #st.session_state["uploaded_file"]=uploaded_file
                    st.success(f"File uploaded successfully: {uploaded_file.name}")

        else:
            st.error("Select an Folder")
        
    except Exception as e:
        st.error(f" Error! Select an Folder: {e}")


 


    
   