import streamlit as st
import requests
import json

st.title("Direct PDF to JSON Conversion")


uploadFile = st.file_uploader("Upload the pdf you want converted", type=("pdf"))

if st.button('Convert'):
    files = {'file': uploadFile}
    res = requests.post(url= "http://127.0.0.1:8000/uploadfile/", files=files)
    st.subheader(f"File recieved, it's being processed! {res.text}")
    fileName = res.text
    newURL = "http://127.0.0.1:8000/items/" + fileName
    res = requests.get(url=newURL)
    if (res):
        st.write("File Processing Completed! Download your JSON file below.")
        returnName = fileName.replace(".pdf",".json")
        st.download_button(label="Download JSON", data=res.json(), file_name=returnName[1:len(returnName)-1:1], mime="application/json", icon=":material/download:",)

st.title("Pinecone storage and quarry")

splitFile = st.file_uploader("Upload the file you want to upsert into the Pinecone" , type=("pdf"))
if st.button('Upsert'):
    files = {'file': splitFile}
    res = requests.post(url= "http://127.0.0.1:8000/uploadfile/", files=files)
    st.subheader(f"File recieved, it's being processed! {res.text}")
    fileName = res.text
    newURL = "http://127.0.0.1:8000/pineconeUplpoad/" + fileName
    res = requests.get(url=newURL)
    if (res):
        st.write("File Upsert Completed! The result was:" , res.text)

semantic = st.text_input("Enter text to do semantic search")
if semantic:
    newURL = "http://127.0.0.1:8000/pinecone/" + semantic
    res = requests.get(url=newURL)
    if res:
        st.subheader(f"Top 5 semantic searches {res.text}")

semantic = st.text_input("Enter text to do id search")
if semantic:
    newURL = "http://127.0.0.1:8000/idsearch/" + semantic
    res = requests.get(url=newURL)
    if res:
        st.subheader(f"Top 10 id searches {res.text}")

# C:\Users\ling1\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts
# streamlit run testFrontEnd.py