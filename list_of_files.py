import streamlit as st
import os
from streamlit_option_menu import option_menu
 
upload = "Client_folder"
#os.makedirs(upload, exist_ok=True)

upload1 ="Poc_folder"
#os.makedirs(upload1, exist_ok=True)

upload2 ="CS_Goals_folder"

# Get list of files in the upload folder
def list_files(upload):
    if os.path.exists(upload):
        return os.listdir(upload) 
    else:
        []
 
def show_list_of_files():
    #st.title("List of Uploaded Files")
 
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
    st.write("### Select Directory")

    

    selected=option_menu(menu_title=None,options=["CS Goals Folder","CLIENT FOLDER","POC FOLDER"],icons=["","bi bi-folder","bi bi-folder"],orientation="horizontal",)

    try:
        if selected == "CLIENT FOLDER":
            # Display list of uploaded files
            #st.write("## Files in the Upload Folder")
            if os.path.exists(upload):
                files_in_folder = list_files(upload)
                if files_in_folder:
                    st.write("### Available files:")
                    for file in files_in_folder:
                        st.write(file)
                else:
                    st.warning("No files uploaded yet.")

            else:
                st.error("The folder does not exist yet. Please upload a file using Fileuploader Page")
        
        elif selected == "POC FOLDER":
            #st.write("## Files in the Upload Folder")
            if os.path.exists(upload1):
                files_in_folder = list_files(upload1)
                if files_in_folder:
                    st.write("### Available files:")
                    for file in files_in_folder:
                        st.write(file)
                else:
                    st.warning("No files uploaded yet.")

            else:
                st.error("The folder does not exist yet. Please upload a file using Fileuploader Page")

        elif selected == "CS Goals Folder":
            #st.write("## Files in the Upload Folder")
            if os.path.exists(upload2):
                files_in_folder = list_files(upload2)
                if files_in_folder:
                    st.write("### Available files:")
                    for file in files_in_folder:
                        st.write(file)
                else:
                    st.warning("No files uploaded yet.")

            else:
                st.error("The folder does not exist yet. Please upload a file using Fileuploader Page")


    except Exception as e:
            pass

