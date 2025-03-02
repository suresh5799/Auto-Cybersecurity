import streamlit as st
from streamlit_option_menu import option_menu
import base64
import os
import PyPDF2 as pdf
from fpdf import FPDF
import streamlit_scrollable_textbox as stx
import re
import time
import fitz


upload = "Client_folder"
os.makedirs(upload, exist_ok=True)

upload1 ="Poc_folder"
os.makedirs(upload1, exist_ok=True)

upload2 ="CS_Goals_folder"
os.makedirs(upload2, exist_ok=True)

d1=[]
d=[] 
error=[]

def set_background():
    image_path = "images/new0.jpg"
    with open(image_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    page_bg = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        #background-repeat:no-repeat;
        #position:relative;
        
    }}
    .stApp::before {{
       content:"";
       position:absolute;
       top:0;
       left:0;
       width:100%;
       height:100%;
       background:rgba(0,0,0,0.5)
       z-index:0;
        
    }}
    
    .stMarkdown, .stTextInput, .st.Button {{
        position:relative;
        z-index:1;
        color:white !important;
    }}
    
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

############################################## CS Goals#####################################################

def extract_text_from_pdf1(file_path,goal_name,file):
        results = {}
    #for file in os.listdir(upload):
        if file.endswith(".pdf"):
            #file_path = os.path.join(upload, file)
            with open(file_path, "rb") as pdf_file:
                reader = pdf.PdfReader(pdf_file)
                text = ""
                
                # Extract text from all pages
                for page in reader.pages:
                    #text += page.extract_text() + "\n"
                    text += page.extract_text()
 
                # Search for the goal name
                if goal_name.lower() in text.lower():
                    #print(goal_name)
                    start_index = text.lower().find(goal_name.lower())  # Find goal name
                    
                    extracted_text = text[start_index:]  # Extract from goal onward
                    lines = extracted_text.splitlines()

                    #Step 2: Select the first line
                    first_line = lines[0]
                    a=first_line.lower()
                    b=a.replace("  ","")
                    #print(b)
                    t=0
                    if goal_name == b:
                        
                        l=[]
                        c=0
                        ch=0
                    # Extract only the requirements (until next goal starts)
                        for line in extracted_text.splitlines():
                            if line.strip()=="":
                                c=c+1
                                ch=ch+1
                            elif c>=2:
                                if ch==1:
                                    c=1
                                    ch=0
                                    l.append("\n")
                                    l.append(line)
                                else:
                                    break
                    
                            else:
                                if ch==1:
                                    ch=0
                                    l.append("\n")
                                l.append(line)
                           
 
                    #All the requirements and goal name are prestent in the l list[] 
                        results[file] = l
 
                        return results
                    else: 
                        #if goal_name!=b:
                        t=t+1

############################################# GENERATE_PDF #########################################################   
def create_pdf():
            #st.title("Report Generated")
                                
            # Sample extracted data (stored as a list)
            data = d1
        #try:
            # Convert list to string (each item in new line)
            pdf_content = "\n".join(data)
                                
            # Create PDF object
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
                                
            # Write content to PDF (multi-cell to handle line breaks)
            pdf.multi_cell(0, 10, pdf_content)
            pdf_folder="requirements.pdf"
            os.makedirs(pdf_folder, exist_ok=True)
            pdf_filename = "report.pdf"
            pdf_path = os.path.join(pdf_folder, pdf_filename)
                                
            # Save the PDF
           
            #login=st.button("gene")
            #if login:
            pdf.output(pdf_path)
            
            #st.success(f"PDF successfully saved: {pdf_path}")
                                
            # Provide a download button
            st.success("PDF successfully generated!")
            time.sleep(5)
            with open(pdf_path, "rb") as pdf_file:    
                st.download_button(label="Download Extracted Data",data=pdf_file,file_name=pdf_filename,mime="application/pdf")
        # except Exception as e:
           # st.error(f"Error generating PDF: {e}")
           # st.write(f"Exception Occurred: {e}")  # Debugging logs
##########################################GENERATE PDF######################################################


def generate_pdf():
    try:
        #if st.button("gen"):
            st.success("\nGenerating PDF...")  # Debugging log
            time.sleep(2)
            
            # Sample content
            pdf_content = "\n".join(d)
    
            # Create PDF object
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, pdf_content)
    
            # ✅ Ensure folder exists
            pdf_folder = "pdf_reports"
            os.makedirs(pdf_folder, exist_ok=True)
    
            # Define file path
            pdf_path = os.path.join(pdf_folder, "requirements.pdf")
    
            # ✅ Save the PDF
            pdf.output(pdf_path)
    
            # ✅ Store PDF path in session state
            st.session_state.pdf_generated = True
            st.session_state.pdf_path = pdf_path
            
            st.success("PDF successfully generated!")
            time.sleep(3)
            st.write("Ready for Download!")
            with open(st.session_state.pdf_path, "rb") as pdf_file:
                
                st.download_button(label="Download PDF",data=pdf_file,file_name="requirements.pdf",mime="application/pdf")
 
    except Exception as e:
        st.error(f"❌ Error generating PDF: {e}")
 



################################## GENERATE_TEXT_FILE #######################################################
def text_file(): 
    # Sample extracted data (stored as a list)
    #if "d" not in st.session_state:
    #    st.session_state.d = d
    data=d1
    #st.write("d:", st.session_state.d)
    
    # Ensure the folder exists
    text_folder = "generated_text_files"
    os.makedirs(text_folder, exist_ok=True)
    
    # Define file path
    text_filename = "report.txt"
    text_path = os.path.join(text_folder, text_filename)
    
    # Write data to the text file
    with open(text_path, "w", encoding="utf-8") as file:
        file.write("\n".join(data))
    
    st.success("Text file generated successfully!")
    time.sleep(3)   
        # Provide download button
    with open(text_path, "rb") as file:
        st.download_button(label="Download Text File",data=file,file_name="report.txt",mime="text/plain")

###################################### NEW###############################
def normalize_text(text):
        """Remove extra spaces and normalize text."""
        normalized_lines = []
        for line in text.splitlines():
            # Compress spaces and tabs to a single space without removing the newline structure.
            normalized_line = re.sub(r'[ \t]+', ' ', line).strip()
            normalized_lines.append(normalized_line)
        return"\n".join(normalized_lines)


#########################################################################################################
def extract_text_from_pdf(file_path,goal_name,file):
            results = {}
            #self.get_doc=0
        #for file in os.listdir(upload):
            if file.endswith(".pdf"):
                #print("in endwith")
                #file_path = os.path.join(upload, file)
                text=""
                with fitz.open(file_path) as doc:
                    for page in doc:
                        text += page.get_text("text")
                       
                    text = normalize_text(text)
                    #print(text)
                    goal_name = normalize_text(goal_name)                    
                # Search for the goal name
                    if goal_name.lower() in text.lower():
                        #print("In if")
                        start_index = text.lower().find(goal_name.lower())  # Find goal name
                        extracted_text = text[start_index:]  # Extract the requirement from here onwards
 
                        lines = extracted_text.splitlines()
                        #Step 2: Select the first line
                        first_line = lines[0]
                        a=first_line.lower()
                        b=a.replace("  ","")
                        goal_name=goal_name.lower()
                        ch=goal_name.replace("  ","")
                        #print(f"c: {ch}")
                        if True:
                            #print("in c")
                            l=[]
                            c=0
                            ch=0
                        # Extract only the requirements (until next goal starts)
                            #print(extracted_text)
                            for line in extracted_text.splitlines():
                                if line.strip()=="":
                                    c=c+1
                                    ch=ch+1
                                elif c>=2:
                                    #break
                                        #Testing for multiple goals in an asset
                                        if ch==1:
                                            c=1
                                            ch=0
                                            l.append("\n")
                                        #l.append("Goal Name :")                                    
                                            l.append(line)                                              
                                        else:
                                            break
                                else:
                                    if ch==1:
                                        #c=1
                                        ch=0
                                        l.append("\n")                                
                                    l.append(line)
                        #All the requirements and goal name are prestent in the l list[]
                            results[file] = l
            return results

#########################################################################################################
def list_files():
    if os.path.exists(upload):
        return os.listdir(upload) 

def list_files1():
    if os.path.exists(upload1):
        return os.listdir(upload1)

'''          
def find_asset_name(file_path):
    with open(file_path, "rb") as pdf_file:
        reader = pdf.PdfReader(pdf_file)
        text = ""
                                
                # Extract text from all pages
        for page in reader.pages:
            text += page.extract_text() + "\n"
                
            
                
                # Regex to match asset names (e.g., "1. Secure Flash", "2. Secure Authentication")
            #asset_pattern = r"^\d+\.\s+[A-Za-z ]+"  # Matches lines starting with "1. " followed by text
    asset_pattern = r'^\s*\d+\.\s+(.+)'
                
    assets = re.findall(asset_pattern, text, re.MULTILINE)  # Use MULTILINE to match each line
                
                    # Remove the numbering (keep only asset names)
    cleaned_assets = [re.sub(r"^\d+\.\s+", "", asset) for asset in assets]
    #cleaned_assets1=normalize_text(cleaned_assets)
                
    return cleaned_assets
'''
    ###############################################################################

def find_asset_name(file_path):
    asset_names=[]
    pattern = re.compile(r'^\s*\d+\.\s+(.+)')  # Matches "1. <Asset Name>"
    #with open(file_path, "rb") as pdf_file:
    doc = fitz.open(file_path)
    for page in doc:
            text = page.get_text("text")  # Extract text from the page
            lines = text.split("\n")  # Split text into lines
            for line in lines:
                stripped_line = line.strip()
                match = pattern.match(stripped_line)
                if match:
                    asset_name = match.group(1).strip()
                    asset_names.append(asset_name)
    return asset_names


'''

def find_asset_name(file_path):
    asset_names = []
    pattern = re.compile(r"^\s*\d+\.\s+(.+)")  # Matches "1. <Asset Name>"
 
    with open(file_path, "rb") as pdf_file:
        reader = pdf.PdfReader(pdf_file)  # Open the PDF file
        for page in reader.pages:
            text = page.extract_text()  # Extract text from the page
            if text:
                lines = text.split("\n")  # Split text into lines
                for line in lines:
                    stripped_line = line.strip()
                    match = pattern.match(stripped_line)
                    if match:
                        asset_name = match.group(1).strip()
                        asset_names.append(asset_name)
 
    return asset_names
'''
#############################################################################
lfiles=os.listdir(upload)
lfiles1=os.listdir(upload1) 
lfiles2=os.listdir(upload2) 

if "selected_folder" not in st.session_state:
    st.session_state.selected_folder = None
if "file_selected" not in st.session_state:
    st.session_state.file_selected = False
if "asset_selected" not in st.session_state:
    st.session_state.asset_selected = False

############################################################  
"""
        if "show_second" not in st.session_state:
            st.session_state.show_second = False
        if "final_output" not in st.session_state:
            st.session_state.final_output = ""
        if "show_second1" not in st.session_state:
            st.session_state.show_second1 = False

"""

def show_search(): 
    #set_background()
    if "pdf_generated" not in st.session_state:
        st.session_state.pdf_generated = False
    if "pdf_path" not in st.session_state:
        st.session_state.pdf_path = None

    if st.session_state.role=="Engineer":
        col1,col3=st.columns([14,3],gap="large")
        #st.write("search")
    
        with col1:
            if st.button("🔼 :rainbow[Upload File]"):
                st.session_state.page = "upload_file"
                st.rerun()
        #with col2:
            #if st.button("🔍:blue[Search]"):
                #st.session_state.page = "old"
                #st.rerun()
        with col3:
            if st.button(":blue[Logout]"):
                st.session_state.logged_in=False
                #st.session_state.role=None
                st.session_state.page = "login"
                st.rerun()
        
######################################################### SEARCH ################################################################
       
        #st.set_page_config(page_title="Cybersecurity",page_icon="🔐",layout="centered")
        ################################################################



        #st.title("lml")

        hide="""
                <style>
                #MainManu {visibility:hidden;}
                footer {visibility:hidden;}
                header {visibility:hidden;}
                </style>
            """
        st.markdown(hide,unsafe_allow_html=True)
       
        selected=option_menu(menu_title=None,options=["CS Goals","CLIENT FOLDER","POC FOLDER"],icons=["🔍","bi bi-folder","bi bi-folder"],orientation="horizontal",)
        # Initialize session state variables
        # Initialize session state variables
        if selected != st.session_state.selected_folder:
            st.session_state.selected_folder = selected
            st.session_state.file_selected = False
            st.session_state.asset_selected = False
    

        l=["aaa","ccc"]

        try:
            if selected == 'CLIENT FOLDER' and st.session_state.username in l:
                if os.path.exists(upload):
                        
                        files=list_files()
                        files.insert(0,"Select an file")
                        #files[0]="Select a file"
                        file = st.selectbox("",files, key="file_select")
                        # First Submit Button
                        if st.button("Submit",key="sub_file"):
                           
                            if file:
                                #st.session_state.show_second = True  # Show second dropdown
                                st.session_state.file_selected = True
                                st.session_state.asset_selected= False
                                
                                
                                
                        elif file=="Select a afile":
                            st.warning("The folder does not exist yet. Please upload a file using Fileiploader Page")

                        #if st.session_state.show_second:
                        if st.session_state.file_selected:
                            
                            
                            file_path = os.path.join(upload, file)
                                #print(file_path)
                            asset_name=find_asset_name(file_path)
                            asset_name.insert(0,"Select asset name")
                            asset1= st.selectbox("", asset_name, key="asset_select")
                            asset=asset1.lower()
                            #print(asset)
                            if st.button("Submit",key="sub_asset"):
                                

    ##############################################################################################################################                            
                                if asset:
                                    st.session_state.asset_selected = True
                                    #print(goal_name)
                                    #if "uploaded_file" is not None: #not in st.session_state or not st.session_state["uploaded_file"]:
                                    if lfiles:   
                                    
                                        #for file in os.listdir(upload):
                                        
                                            file_path = os.path.join(upload, file)
                                            #print(file_path)
                                            pdf_text = extract_text_from_pdf(file_path,asset,file)
                                            
                                            if pdf_text:
                                                for file,text in pdf_text.items():
                                                    #st.write(f"### Results from: {file}")
                                                    d.append(file)
                                                    #st.write(text)
                                                    for a in text:
                                                        st.write(a)
                                                        d.append(a)
                                                    d.append("\n")
                                                generate_pdf()
                                            else:
                                                error.append(file)
                                                #st.warning(f"No matching goal found in this:{file}")
                                        
                                            st.error(f"No matching asset found in this files:{error}")
                                        #for a in error:
                                            #st.error(f"No matching goal found in this file:{a}")
                                            
                                            #if st.button("generate",key="sub_file1"):
                                            # st.session_state.record = True
                                            #if st.button("Generate PDF"):
                                            #generate_pdf()
                                            #if st.session_state.pdf_generated and st.session_state.pdf_path:
                                                #st.write("✅ PDF Ready for Download!")  # Debugging log
                                            
                                            #create_pdf()
                                            # The message and nested widget will remain on the page
                                                
                                        
                                            
                                        #text_file()
                                        
                                            #generate_pdf()
                                        
                                        # Display download button if PDF is generated
                                        
                                    else:
                                        st.error("Kindly upload the file before initializing the search")
                                        st.error("No files uploaded. Please upload the files first on the Upload File page.")

                                else:
                                    st.error("Enter the asset Name") 
                                st.session_state.reset_trigger = True  # Set the trigger to reset session state
                                st.experimental_rerun() 

#############################################################################################################################
            #elif selected == 'POC FOLDER':
                #with st.form("enter_form1",clear_on_submit=True):
                   # if os.path.exists(upload1):
                      #  files1=list_files1()
                      #  files1.insert(0,"Select a file")
                       # st.selectbox("Choose a PDF file",files1,key="files1")
                    #else:
                        #st.warning("The folder does not exist yet. Please upload a file using Fileiploader Page")

                    #submitted=st.form_submit_button("Submit")
            elif selected == 'POC FOLDER':
                
                if os.path.exists(upload1):
                        
                        files1=list_files1()
                        files1.insert(0,"Select an file")
                        #files[0]="Select a file"
                        file1 = st.selectbox("",files1, key="file_select1")
                        # First Submit Button
                        if st.button("Submit",key="sub_file1"):
                            #st.session_state.show_second1 = True  # Show second dropdown
                            if file1:
                                st.session_state.file_selected = True  # Show second dropdown
                                st.session_state.asset_selected = False
                        elif file1=="Select a afile":
                            st.warning("The folder does not exist yet. Please upload a file using Fileiploader Page")

                        if st.session_state.file_selected:
                            
                            file_path = os.path.join(upload1, file1)
                                #print(file_path)
                            asset_name=find_asset_name(file_path)
                            asset_name.insert(0,"Select asset name")
                            asset1= st.selectbox("", asset_name, key="asset_select")
                            asset=asset1.lower()
                            #print(asset)
                            if st.button("Submit",key="sub_asset"):
                                
    ##############################################################################################################################                            
                                if asset:
                                    st.session_state.asset_selected = True
                                    if lfiles1:   
                                    
                                        #for file in os.listdir(upload):
                                            file_path = os.path.join(upload1, file1)
                                            #print(file_path)
                                            pdf_text = extract_text_from_pdf(file_path,asset,file1)
                                            
                                            if pdf_text:
                                                for file,text in pdf_text.items():
                                                    #st.write(f"### Results from: {file}")
                                                    d.append(file)
                                                    #st.write(text)
                                                    for a in text:
                                                        st.write(a)
                                                        d.append(a)
                                                    d.append("\n")
                                                generate_pdf()
                                            else:
                                                error.append(file)
                                                #st.warning(f"No matching goal found in this:{file}")
                                        
                                            st.error(f"No matching asset found in this files:{error}")
                                        #for a in error:
                                            #st.error(f"No matching goal found in this file:{a}")
                                            
                                            #if st.button("generate",key="sub_file1"):
                                            # st.session_state.record = True
                                            #if st.button("Generate PDF"):
                                            #generate_pdf()
                                            #if st.session_state.pdf_generated and st.session_state.pdf_path:
                                                #st.write("✅ PDF Ready for Download!")  # Debugging log
                                            
                                            #create_pdf()
                                            # The message and nested widget will remain on the page
                                                
                                        
                                            
                                        #text_file()
                                        
                                            #generate_pdf()
                                        
                                        # Display download button if PDF is generated
                                        
                                    else:
                                        st.error("Kindly upload the file before initializing the search")
                                        st.error("No files uploaded. Please upload the files first on the Upload File page.")

                                else:
                                    st.error("Enter the asset Name") 
#############################################################################################################################
            elif selected == "CS Goals":

                        error=[]
                    # Search Functionality
                        st.subheader("Enter the Goal Name")
                        #Here asking a goal name to user
                        goal_name1 = st.text_input("e.g., Secure Authentication or Secure Flash.")
                        #print(goal_name1)
                        goal_name=goal_name1.lower()
                        
                        if st.button("Search"):
                            if goal_name:
                                #print(goal_name)
                                #if "uploaded_file" is not None: #not in st.session_state or not st.session_state["uploaded_file"]:
                                if lfiles2:   
                                
                                    for file in os.listdir(upload2):
                                        file_path = os.path.join(upload2, file)
                                        #print(goal_name)
                                        pdf_text = extract_text_from_pdf1(file_path,goal_name,file)
                                        if pdf_text:
                                            for file,text in pdf_text.items():
                                                st.write(f"### Results from: {file}")
                                                d1.append(file)
                                                #st.write(text)
                                                for a in text:
                                                    st.write(a)
                                                    d1.append(a)
                                                d1.append("\n")

                                            
                                        else:
                                            error.append(file)
                                            #st.warning(f"No matching goal found in this:{file}")
                                    
                                    st.error(f"No matching goal found in this files:{error}")
                                    #for a in error:
                                        #st.error(f"No matching goal found in this file:{a}")
                                    
                                    if text:
                                        create_pdf()
                                    
                                        # The message and nested widget will remain on the page
                                    
                                    
                                        
                                    #text_file()
                                    
                                    #generate_pdf()
                                    
                                    # Display download button if PDF is generated
                                    
                                else:
                                    st.error("Kindly upload the file before initializing the search")
                                    st.error("No files uploaded. Please upload the files first on the Upload File page.")

                            else:
                                st.error("Enter the Goal Name")

                    #else:
                        #st.error("Unauthorized PS Number. You are not allowed to Search")

                #elif a:
                       # st.error("Please Enter your PS Number to proceed.")
            else:
                st.error("Unauthorized User")

            #st.session_state.show_second = False
        except Exception as e:
            pass
            #st.error(f"❌ Error generating PDF: {e}")


######################################################################################################################################
        


    if st.session_state.role=="Admin":
    
        col1, col2, col3,col5 = st.columns([29,25,30,12])
    
        with col1:
            if st.button("🔼 :rainbow[Upload File]"):
                st.session_state.page = "upload_file"
                st.rerun()
        with col2:
            if st.button("📂 :green[File Catalog]"):
                st.session_state.page = "list_of_files"
                st.rerun()
        with col3:
            if st.button("❌ :violet[Remove File]"):
                st.session_state.page = "delete_file"
                st.rerun()
        #with col4:
           # if st.button("🔍:blue[Search]"):
               # st.session_state.page = "old"
                #st.rerun()
        with col5:
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
       
        selected1=option_menu(menu_title=None,options=["CS Goals","CLIENT FOLDER","POC FOLDER"],icons=["","bi bi-folder","bi bi-folder"],orientation="horizontal",)
        #print(selected)
        if selected1 != st.session_state.selected_folder:
            st.session_state.selected_folder = selected1
            st.session_state.file_selected = False
            st.session_state.asset_selected = False

        try:
            if selected1 == "CLIENT FOLDER":
                if os.path.exists(upload):
                        
                        files=list_files()
                        files.insert(0,"Select an file")
                        #files[0]="Select a file"
                        file = st.selectbox("",files, key="file_select")
                        # First Submit Button
                        if st.button("Submit",key="sub_file"):
                            if file:
                                #st.session_state.show_second = True  # Show second dropdown
                                st.session_state.file_selected = True
                                st.session_state.asset_selected= False
                            #st.session_state.show_second = True  # Show second dropdown

                        elif file=="Select a afile":
                            st.warning("The folder does not exist yet. Please upload a file using Fileiploader Page")

                        if st.session_state.file_selected:
                            
                            file_path = os.path.join(upload, file)
                                #print(file_path)
                            asset_name=find_asset_name(file_path)
                            asset_name.insert(0,"Select asset name")
                            asset1= st.selectbox("", asset_name, key="asset_select")
                            asset=asset1.lower()
                            #print(asset)
                            if st.button("Submit",key="sub_asset"):
    ##############################################################################################################################                            
                                if asset:
                                    st.session_state.asset_selected= True
                                    #print(goal_name)
                                    #if "uploaded_file" is not None: #not in st.session_state or not st.session_state["uploaded_file"]:
                                    if lfiles:   
                                    
                                        #for file in os.listdir(upload):
                                        
                                            file_path = os.path.join(upload, file)
                                            #print(file_path)
                                            pdf_text = extract_text_from_pdf(file_path,asset,file)
                                            
                                            if pdf_text:
                                                for file,text in pdf_text.items():
                                                    #st.write(f"### Results from: {file}")
                                                    d.append(file)
                                                    #st.write(text)
                                                    for a in text:
                                                        st.write(a)
                                                        d.append(a)
                                                    d.append("\n")
                                                generate_pdf()
                                            else:
                                                error.append(file)
                                                #st.warning(f"No matching goal found in this:{file}")
                                        
                                            st.error(f"No matching asset found in this files:{error}")
                                        #for a in error:
                                            #st.error(f"No matching goal found in this file:{a}")
                                            
                                            #if st.button("generate",key="sub_file1"):
                                            # st.session_state.record = True
                                            #if st.button("Generate PDF"):
                                            #generate_pdf()
                                            #if st.session_state.pdf_generated and st.session_state.pdf_path:
                                                #st.write("✅ PDF Ready for Download!")  # Debugging log
                                            
                                            #create_pdf()
                                            # The message and nested widget will remain on the page
                                                
                                        
                                            
                                        #text_file()
                                        
                                            #generate_pdf()
                                        
                                        # Display download button if PDF is generated
                                        
                                    else:
                                        st.error("Kindly upload the file before initializing the search")
                                        st.error("No files uploaded. Please upload the files first on the Upload File page.")

                                else:
                                    st.error("Enter the asset Name")  

#############################################################################################################################
            #elif selected == 'POC FOLDER':
                #with st.form("enter_form1",clear_on_submit=True):
                   # if os.path.exists(upload1):
                      #  files1=list_files1()
                      #  files1.insert(0,"Select a file")
                       # st.selectbox("Choose a PDF file",files1,key="files1")
                    #else:
                        #st.warning("The folder does not exist yet. Please upload a file using Fileiploader Page")

                    #submitted=st.form_submit_button("Submit")
            elif selected1 == "POC FOLDER":
                if os.path.exists(upload1):
                        
                        files1=list_files1()
                        files1.insert(0,"Select an file")
                        #files[0]="Select a file"
                        file1 = st.selectbox("",files1, key="file_select1")
                        # First Submit Button
                        if st.button("Submit",key="sub_file1"):
                            if file1:
                                #st.session_state.show_second = True  # Show second dropdown
                                st.session_state.file_selected = True
                                st.session_state.asset_selected= False
                        
                        elif file1=="Select a afile":
                            st.warning("The folder does not exist yet. Please upload a file using Fileiploader Page")

                        if st.session_state.file_selected:
                            
                            file_path = os.path.join(upload1, file1)
                                #print(file_path)
                            asset_name=find_asset_name(file_path)
                            asset_name.insert(0,"Select asset name")
                            asset1= st.selectbox("", asset_name, key="asset_select")
                            asset=asset1.lower()
                            #print(asset)
                            if st.button("Submit",key="sub_asset"):
    ##############################################################################################################################                            
                                if asset:
                                    st.session_state.asset_selected= True
                                    #print(goal_name)
                                    #if "uploaded_file" is not None: #not in st.session_state or not st.session_state["uploaded_file"]:
                                    if lfiles1:   
                                    
                                        #for file in os.listdir(upload):
                                            file_path = os.path.join(upload1, file1)
                                            #print(file_path)
                                            pdf_text = extract_text_from_pdf(file_path,asset,file1)
                                            
                                            if pdf_text:
                                                for file,text in pdf_text.items():
                                                    #st.write(f"### Results from: {file}")
                                                    d.append(file)
                                                    #st.write(text)
                                                    for a in text:
                                                        st.write(a)
                                                        d.append(a)
                                                    d.append("\n")
                                                generate_pdf()
                                            else:
                                                error.append(file)
                                                #st.warning(f"No matching goal found in this:{file}")
                                        
                                            st.error(f"No matching asset found in this files:{error}")
                                        #for a in error:
                                            #st.error(f"No matching goal found in this file:{a}")
                                            
                                            #if st.button("generate",key="sub_file1"):
                                            # st.session_state.record = True
                                            #if st.button("Generate PDF"):
                                            #generate_pdf()
                                            #if st.session_state.pdf_generated and st.session_state.pdf_path:
                                                #st.write("✅ PDF Ready for Download!")  # Debugging log
                                            
                                            #create_pdf()
                                            # The message and nested widget will remain on the page
                                                
                                        
                                            
                                        #text_file()
                                        
                                            #generate_pdf()
                                        
                                        # Display download button if PDF is generated
                                        
                                    else:
                                        st.error("Kindly upload the file before initializing the search")
                                        st.error("No files uploaded. Please upload the files first on the Upload File page.")

                                else:
                                    st.error("Enter the asset Name") 
#############################################################################################################################
            elif selected1 == "CS Goals":

                        error=[]
                    # Search Functionality
                        st.subheader("Enter the Goal Name")
                        #Here asking a goal name to user
                        goal_name1 = st.text_input("e.g., Secure Authentication or Secure Flash.")
                        #print(goal_name1)
                        goal_name=goal_name1.lower()
                        
                        if st.button("Search"):
                            if goal_name:
                                #print(goal_name)
                                #if "uploaded_file" is not None: #not in st.session_state or not st.session_state["uploaded_file"]:
                                if lfiles2:   
                                
                                    for file in os.listdir(upload2):
                                        file_path = os.path.join(upload2, file)
                                        #print(goal_name)
                                        pdf_text = extract_text_from_pdf1(file_path,goal_name,file)
                                        if pdf_text:
                                            for file,text in pdf_text.items():
                                                st.write(f"### Results from: {file}")
                                                d1.append(file)
                                                #st.write(text)
                                                for a in text:
                                                    st.write(a)
                                                    d1.append(a)
                                                d1.append("\n")

                                            
                                        else:
                                            error.append(file)
                                            #st.warning(f"No matching goal found in this:{file}")
                                        
                                    
                                    st.error(f"No matching goal found in this files:{error}")
                                    #for a in error:
                                        #st.error(f"No matching goal found in this file:{a}")
                                    
                                    if pdf_text:
                                         create_pdf()
                                    
                                        # The message and nested widget will remain on the page
                                    
                                    
                                        
                                    #text_file()
                                    
                                    #generate_pdf()
                                    
                                    # Display download button if PDF is generated
                                    
                                else:
                                    st.error("Kindly upload the file before initializing the search")
                                    st.error("No files uploaded. Please upload the files first on the Upload File page.")

                            else:
                                st.error("Enter the Goal Name")

                    #else:
                        #st.error("Unauthorized PS Number. You are not allowed to Search")

                #elif a:
                       # st.error("Please Enter your PS Number to proceed.")
            else:
                st.error("Unauthorized User")

            #st.session_state.show_second = False
        except Exception as e:
            pass
            #st.error(f"❌ Error generating PDF: {e}")
    

'''
 ################################################### NAVIGATION FOR OTHER PAGES##################################
def show_search():
    #st.title("Search Page")
 
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
 
    with col1:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "login"
            st.rerun()
    
    with col2:
        if st.button("📁 Upload File"):
            st.session_state.page = "upload_file"
            st.rerun()
 
    with col3:
        if st.button("🗑 Delete File"):
            st.session_state.page = "delete_file"
            st.rerun()
 
    with col4:
        if st.button("List of Files"):
            st.session_state.page = "list_of_files"
            st.rerun()
'''

###########################################################################################################################

