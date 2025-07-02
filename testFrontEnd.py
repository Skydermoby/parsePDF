import streamlit as st
import requests

st.title("Aaron's super shabby front end :p")

uploadFile = st.file_uploader("Upload the pdf you want converted", type=("pdf"))

if st.button('Convert'):
    files = {'file': uploadFile}
    res = requests.post(url= "http://127.0.0.1:8000/uploadfile/", files=files)
    st.subheader(f"Response from API = {res.text}")

#steamlit run testFrontEnd.py