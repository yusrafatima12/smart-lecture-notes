import streamlit as st

# title
st.title("MY SMART NOTES")

# st.file_uploader() upload button banata hai.
audio_file = st.file_uploader(
    "Upload your lecture audio",
    type=["mp3", "wav", "m4a", "ogg", "aac", "acc"]
)
#showing name of uploaded audio
# st.success()	App ki screen par green message show karta hai.
if audio_file != None:
    # st.success(f"Uploaded file: {audio_file.name}")
    st.success("FILE UPLOADED SUCCESSFULLY")

