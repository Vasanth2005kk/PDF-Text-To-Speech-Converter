from gtts import gTTS
import PyPDF2
import os

# Extract text from PDF file
def read_pdf(file_name):
    with open(file_name, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text
    return " ".join(text.split("\n"))

# Convert text to speech and save as an MP3 file
def Text_To_Speech(pdf_text, language_code, file_name):
    tts = gTTS(text=pdf_text, lang=language_code, slow=False)
    
    save_path = os.path.join(os.getcwd(), "save_audio_files")
    os.makedirs(save_path, exist_ok=True)
    
    file_path = os.path.join(save_path, f"{file_name}.mp3")
    tts.save(file_path)
    
    return os.path.exists(file_path)

# Test script
if __name__ == "__main__":
    file_name = input("Enter the PDF file name or path: ")
    text = read_pdf(file_name)
    file_name = os.path.splitext(os.path.basename(file_name))[0]
    if Text_To_Speech(text, "en", file_name):
        print("\n✅ Done! Audio saved successfully.\n")
