import streamlit as st
import json
import TTS_Text_To_Speech as tts
import os

# Global variables
All_language = []
language_code = "en"

# Load language codes
@st.cache_data
def load_language_data():
    with open('language_codes.json', 'r') as file:
        return json.load(file)

@st.cache_data
def get_all_language():
    data = load_language_data()
    return [leng['language'] for leng in data]

@st.cache_data
def get_language_code(language_name):
    for i in load_language_data():
        if i['language'] == language_name:
            return i['code']

# Streamlit UI
st.set_page_config(page_title='PDF Text To Speech', page_icon='🔊')
st.title('📄 PDF Text To Speech Converter')

# Sidebar for language selection
with st.sidebar:
    st.write('🔗 **Select the language to convert the text to speech**')
    active = st.checkbox('Enable Languages', value=False)
    languages = get_all_language()
    language_name = st.radio(
        '', 
        languages, 
        index=28, 
        disabled=not active, 
        label_visibility='collapsed'
    )
    if active:
        language_code = get_language_code(language_name)

st.write(f"**Selected Language:** {language_name} ({language_code})")

# File upload section
PDF_file = st.file_uploader('📥 Upload a PDF file', type='pdf')
if PDF_file is not None:
    st.write(f"Uploaded file name: {PDF_file.name}")
    File_name = PDF_file.name.split('.')[0]
else:
    st.warning('⚠️ Please upload a PDF file.')

# Convert to Speech Button
if st.button('🎤 Convert to Speech'):
    if PDF_file is not None:
        with open("temp.pdf", "wb") as temp_file:
            temp_file.write(PDF_file.read())
        
        PDF_text = tts.read_pdf("temp.pdf")
        st.write(PDF_text)
        
        success = tts.Text_To_Speech(PDF_text, language_code, File_name)
        if success:
            audio_file = f'save_audio_files/{File_name}.mp3'
            st.audio(audio_file, format='audio/mp3')
            st.success('✅ Conversion successful! Audio is ready.')
            
            # Add download button
            with open(audio_file, "rb") as file:
                audio_bytes = file.read()
                st.download_button(
                    label="⬇️ Download Audio File",
                    data=audio_bytes,
                    file_name=f"{File_name}.mp3",
                    mime="audio/mp3"
                )
        else:
            st.error('❌ Failed to generate audio.')
        
        os.remove("temp.pdf")
    else:
        st.warning('⚠️ Please upload a PDF file first.')
