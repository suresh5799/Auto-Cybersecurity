import streamlit as st
import os
from streamlit_option_menu import option_menu

 
upload = "Client_folder"
#os.makedirs(upload, exist_ok=True)

upload1 ="Poc_folder"
#os.makedirs(upload1, exist_ok=True)

upload2 ="CS_Goals_folder"

# Function to delete a file by name
def delete_file(filename,upload):
    file_path = os.path.join(upload, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return f"File '{filename}' has been deleted."
    else:
        return f"File '{filename}' not found."
 
# Get list of files in the upload folder
def list_files():
    if os.path.exists(upload):
        return os.listdir(upload) 
    else:
        []
# Get list of files in the upload folder
def list_files1():
    if os.path.exists(upload1):
        return os.listdir(upload1) 
    else:
        []

# Get list of files in the upload folder
def list_files2():
    if os.path.exists(upload2):
        return os.listdir(upload2) 
    else:
        []

def show_delete_file():
    #st.title("Delete a File")
 
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
            #st.write("### Available files")
            if os.path.exists(upload):
                files_in_folder = list_files()
                files_in_folder.insert(0,"Select a file")
                if files_in_folder:
                    #st.write("Available files:")
                    for file in files_in_folder:
                        #st.write(file)
                        pass
                else:
                    st.write("No files uploaded yet.")

            
                # File deletion section
                #st.write("### Delete a File")

                #file_to_delete = st.text_input("Enter the filename:")
                present_files=st.selectbox("",files_in_folder,key="present_files")
                if st.button("Delete File"):
                    if present_files:
                        result = delete_file(present_files,upload)
                        st.write(result)
                    else:
                        st.warning("Please enter an filename to delete.")

            else:
                st.warning("The folder doesn't exist yet. Please upload a file using Upload File Page")
        
        elif selected == "POC FOLDER":
            #st.write("### Available files")
            if os.path.exists(upload1):
                files_in_folder = list_files1()
                files_in_folder.insert(0,"Select a file")
                if files_in_folder:
                    #st.write("Available files:")
                    for file in files_in_folder:
                        pass
                        #st.write(file)
                else:
                    st.write("No files uploaded yet.")

            
                # File deletion section
                #st.write("### Delete a File")
                present_files=st.selectbox("",files_in_folder,key="present_files")
                #file_to_delete = st.text_input("Enter the filename:")
                
                if st.button("Delete File"):
                    if present_files:
                        result = delete_file(present_files,upload1)
                        st.write(result)
                    else:
                        st.warning("Please enter an filename to delete.")

            else:
                st.warning("The folder doesn't exist yet. Please upload a file using Upload File Page")

        elif selected == "CS Goals Folder":
            #st.write("### Available files")
            if os.path.exists(upload2):
                #files_in_folder[0]="Select an file"
                files_in_folder = list_files2()
                files_in_folder.insert(0,"Select a file")
                if files_in_folder:
                    #st.write("Available files:")
                    
                    for file in files_in_folder:
                        pass
                        #st.write(file)
                else:
                    st.write("No files uploaded yet.")

            
                # File deletion section
                #st.write("### Delete a File")
                present_files=st.selectbox("",files_in_folder,key="present_files")
                #file_to_delete = st.text_input("Enter the filename:")
                
                if st.button("Delete File"):
                    if present_files:
                        result = delete_file(present_files,upload2)
                        st.write(result)
                    else:
                        st.warning("Please enter an filename to delete.")

            else:
                st.warning("The folder doesn't exist yet. Please upload a file using Upload File Page")


    except Exception as e:
            pass

