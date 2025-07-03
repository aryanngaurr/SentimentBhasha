import streamlit as st
import pandas as pd
import re
import pickle
from PyPDF2 import PdfReader
import docx2txt

# Load the saved model, vectorizer, and label encoder using pickle
def load_model():
    with open('sentiment_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    with open('label_encoder.pkl', 'rb') as le_file:
        label_encoder = pickle.load(le_file)
    return model, vectorizer, label_encoder

model, vectorizer, label_encoder = load_model()

# Function to clean the text data
def clean_text(text):
    text = re.sub(r'http\S+', '', text)  # remove URLs
    text = re.sub(r'<.*?>', '', text)    # remove HTML tags
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # remove special characters and punctuation
    text = text.lower()  # convert to lowercase
    return text

# Function to read uploaded files
def read_file(file):
    if file.type == "text/plain":
        text = file.read().decode("utf-8")
    elif file.type == "application/pdf":
        pdf_reader = PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = docx2txt.process(file)
    else:
        text = None
    return text

# Function to predict Threat
def predict_Threat(text):
    clean_input = clean_text(text)
    input_vector = vectorizer.transform([clean_input]).toarray()
    prediction = model.predict(input_vector)
    predicted_label = label_encoder.inverse_transform(prediction)[0]
    return predicted_label


def main():
    st.title("AI Powered In Wireless Network")

   
    st.header("Upload a File")
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])

    if uploaded_file is not None:
        text = read_file(uploaded_file)
        if text:
            st.write("File content:")
            st.text_area("Text Preview", text, height=200)

            
            st.write("Threat Predictions:")
            comments = text.split("\n")  
            for comment in comments:
                if comment.strip():
                    Threat = predict_Threat(comment)
                    st.write(f"Comment: {comment.strip()}")
                    st.write(f"Predicted Threat: {Threat}")
                    st.write("---")
        else:
            st.error("Could not read the file. Please upload a valid file.")

   
    st.header("Enter a threat")
    user_input = st.text_area("Type of Threat", height=100)

    if st.button("Predict Threat"):
        if user_input.strip():
            Threat = predict_Threat(user_input)
            st.write(f"The predicted Threat is: **{Threat}**")
        else:
            st.error("Please write a valid comment.")

if __name__ == '__main__':
    main()
