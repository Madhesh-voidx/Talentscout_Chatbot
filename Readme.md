# TalentScout Hiring Assistant 🤖

This project is a conversational AI-powered chatbot designed to act as a preliminary technical interviewer. It gathers essential candidate information and generates a tailored set of questions based on a declared tech stack. After the interview, it provides a comprehensive summary and a score to assess the candidate's performance.

## 🚀 Features

* **User Information Gathering**: Collects the candidate's name, email, phone number, and desired position.
* **Position and Experience Validation**: Validates the entered position using an LLM and confirms the years of experience.
* **Dynamic Question Generation**: Generates a set of relevant technical questions based on the candidate's years of experience and tech stack.
* **Interview Summary**: Analyzes the candidate's answers and provides a holistic summary, including strengths, areas for improvement, and an overall score.
* **Conversational Flow**: Manages the multi-step interview process using Streamlit's session state management.

## ⚙️ Installation Instructions

To set up and run this application locally, follow these steps.

### Prerequisites

Ensure you have Python 3.9 or higher installed on your system.

### Step 1: Clone the Repository
Clone this repository to your local machine using Git:

git clone [https://github.com/MADHESH1234/Talentscout_Chatbot.git](https://github.com/MADHESH1234/Talentscout_Chatbot.git)
cd Talentscout_Chatbot

### Step 2: Install Dependencies
pip install -r requirements.txt

### Step 3: Configure Your API Key
Create a file named .env in the root of your project directory and add your llm API key to it.

GEMINI_API_KEY="YOUR_API_KEY_HERE"

###  Usage
To run the chatbot, execute the following command in your terminal:

streamlit run app.py

The application will launch in your web browser. Follow the on-screen prompts to start the interview.

### Technical Details
 * **Framework:** The application is built as a single-page app using Streamlit for the user interface and session state management.

* **Language Model:** The core of the chatbot's intelligence is powered by the Google Generative AI library, utilizing the Gemini 1.5 Flash model.

* **Validation:** The re module is used for robust email and phone number validation.

* **Architecture:** The conversation is managed through a state machine, where the st.session_state.stage variable controls the flow of the interview.
