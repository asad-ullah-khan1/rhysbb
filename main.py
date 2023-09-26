import os
import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI


def get_available_files(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return [os.path.join(folder_path, f) for f in files]

def upload_files(upload_folder):
    uploaded_files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_name = os.path.join(upload_folder, uploaded_file.name)
            with open(file_name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File saved: {uploaded_file.name}")

def main():

    st.set_page_config(page_title="CSV File Chatbot", layout="wide")
    st.title("CSV File ChatBot 🤖")

    # Create a folder to store the uploaded files
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    # Upload CSV files
    upload_files(upload_folder)

    # Get the updated list of available files
    available_files = get_available_files(upload_folder)

    if available_files:
        # Allow users to select from the available files
        selected_files = st.multiselect("Select files", available_files)

        if selected_files:
            for selected_file in selected_files:
                st.subheader(f"Viewing {os.path.basename(selected_file)}")

                openai_api_key = st.secrets["OPENAI_API_KEY"]
                agent = create_csv_agent(OpenAI(temperature=0), selected_file, verbose=True, openai_api_key=openai_api_key)

                # Generate a unique key for the text input widget
                widget_key = f"userQuestions_{selected_file}"

                # Provide user instructions or messages
                st.write("You can ask questions about the CSV data in the text box below.")
                user_question = st.text_input("Ask a question about your CSV:", key=widget_key)

                if user_question:
                    with st.spinner(text="In progress..."):
                        try:
                            response = agent.run(user_question)
                            st.write(response)
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
