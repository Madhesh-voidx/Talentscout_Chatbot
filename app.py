import streamlit as st
import google.generativeai as genai
import re
import time
import os
from dotenv import load_dotenv


load_dotenv()


genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def is_valid_email(email):

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False

def is_valid_mobile(mobile_number):
    
    pattern = r'^\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*\d\D*$'
    if re.match(pattern, mobile_number):
        return True
    return False


if "messages" not in st.session_state:
    st.session_state.messages = []
if "stage" not in st.session_state:
    st.session_state.stage = "greeting"
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "generated_tech_stack" not in st.session_state:
    st.session_state.generated_tech_stack = None
if "technical_questions" not in st.session_state:
    st.session_state.technical_questions = None
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if st.session_state.stage == "greeting":
    greeting_message_1 = "Hello! 👋 Welcome to TalentScout a fictional recruitment agency specializing in technology placements. I'm here to gather some information and ask a few technical questions."
    greeting_message_2 = "To begin, what is your **Full Name**?"
    
    st.chat_message("assistant").markdown(greeting_message_1)
    st.session_state.messages.append({"role": "assistant", "content": greeting_message_1})
    
    st.chat_message("assistant").markdown(greeting_message_2)
    st.session_state.messages.append({"role": "assistant", "content": greeting_message_2})
    st.session_state.stage = "awaiting_name"

if st.session_state.stage == "awaiting_name":
    prompt = st.chat_input("Enter your full name...")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.user_info["full_name"] = prompt
        
        assistant_response = f"Thank you **{prompt}** . What is your **Email Address**?"
        st.chat_message("assistant").markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        st.session_state.stage = "awaiting_email"
        st.rerun()

elif st.session_state.stage == "awaiting_email":
    prompt = st.chat_input("Enter your valid email address...")
    if prompt:
        if is_valid_email(prompt):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.user_info["email"] = prompt

            assistant_response = f"Got it. What is your **Mobile Number**?"
            st.chat_message("assistant").markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            st.session_state.stage = "awaiting_mobile"
            st.rerun()
        else:
            error_message = f"The email address you've entered **'{prompt}'** doesn't look like a valid email address. Please enter a valid email address."
            st.chat_message("assistant").markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

elif st.session_state.stage == "awaiting_mobile":
    prompt = st.chat_input("Enter your vaild mobile number...")
    if prompt:
        if is_valid_mobile(prompt):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.user_info["mobile_number"] = prompt

            assistant_response = f"Thanks. What is your **Desired Position**?"
            st.chat_message("assistant").markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            st.session_state.stage = "awaiting_position"
            st.rerun()
        else:
            error_message = f"The number you've entered **'{prompt}'** doesn't look like a valid mobile number. Please enter a valid mobile number."
            st.chat_message("assistant").markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

elif st.session_state.stage == "awaiting_position":
    prompt = st.chat_input("Enter your desired position...")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.user_info["desired_position"] = prompt
        
        st.session_state.stage = "validating_position"
        st.rerun()

elif st.session_state.stage == "validating_position":
    with st.spinner("Validating position..."):
        pos = st.session_state.user_info["desired_position"]
        llm_validation_prompt = f"""
        Is '{pos}' a valid, work-related tech or IT position?
        Respond only with the word 'True' or 'False'.
        """
        try:
            response = model.generate_content(llm_validation_prompt)
            validation_result = response.text.strip().lower()

            if validation_result == "true":
                assistant_response = f"Great. How many years of experience do you have in **{pos}**?"
                st.chat_message("assistant").markdown(assistant_response)
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                st.session_state.stage = "awaiting_years_of_experience"
                st.rerun()
            else:
                error_message = f"I'm sorry, **'{pos}'** does not seem like a valid tech or IT position. Please enter a different one."
                st.chat_message("assistant").markdown(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})
                st.session_state.stage = "awaiting_position"
                st.rerun()
        
        except Exception as e:
            error_message = f"I'm having trouble validating this position. Please try again. Error: {e}"
            st.chat_message("assistant").markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.session_state.stage = "awaiting_position"
            st.rerun()

elif st.session_state.stage == "awaiting_years_of_experience":
    prompt = st.chat_input("Enter your years of experience...")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.user_info["years_of_experience"] = prompt

        assistant_response = f"What is your **Current Location**?"
        st.chat_message("assistant").markdown(assistant_response)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        st.session_state.stage = "awaiting_location"
        st.rerun()



elif st.session_state.stage == "awaiting_location":
    prompt = st.chat_input("Enter your current location...")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.user_info["location"] = prompt
        
        st.session_state.stage = "generating_tech_stack"
        st.rerun()

elif st.session_state.stage == "generating_tech_stack":
    with st.spinner("Generating tech stack list based on your desired position..."):
        llm_prompt = f"""
        Generate a comprehensive, comma-separated list of the core and extended tech stack required for a professional role as a '{st.session_state.user_info["desired_position"]}'.
        Do not include any other text, greetings, or explanations.
        Example: "Python, Django, PostgreSQL, AWS, React, Docker, Kubernetes"
        """
        try:
            response = model.generate_content(llm_prompt)
            tech_stack_options = [tech.strip() for tech in response.text.split(',')]
            st.session_state.generated_tech_stack = tech_stack_options
            
            assistant_response = f"Based on a **{st.session_state.user_info['desired_position']}** role, here are some common technologies i have listed. Please select all the ones you have experience or familiar with...."
            st.chat_message("assistant").markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            st.session_state.stage = "select_tech_stack"
            st.rerun()
        except Exception as e:
            error_message = f"I'm sorry, I couldn't generate the list. Please try again later. Error: {e}"
            st.chat_message("assistant").markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.session_state.stage = "awaiting_position"
            st.rerun()

elif st.session_state.stage == "select_tech_stack":
    selected_tech = st.multiselect(
        "Select your tech stack",
        options=st.session_state.generated_tech_stack,
        placeholder="Choose your tech stack"
    )
    
    submit_button = st.button("Submit Tech Stack")
    
    if submit_button:
        st.session_state.user_info["tech_stack"] = selected_tech
        
        final_message = "Thank you! for the information. I will now generate your technical questions based on your techstack."
        st.chat_message("assistant").markdown(final_message)
        st.session_state.messages.append({"role": "assistant", "content": final_message})

        st.session_state.stage = "generate_questions"
        st.rerun()

elif st.session_state.stage == "generate_questions":
    user_data = st.session_state.user_info
    summary_message = "Here is the list of information you've entered📋:\n\n"
    summary_message += f"- **Name**: {user_data.get('full_name', 'N/A')}\n"
    summary_message += f"- **Email**: {user_data.get('email', 'N/A')}\n"
    summary_message += f"- **Mobile**: +91 {user_data.get('mobile_number', 'N/A')}\n"
    summary_message += f"- **Desired Position**: {user_data.get('desired_position', 'N/A')}\n"
    summary_message += f"- **Years of Experience**: {user_data.get('years_of_experience', 'N/A')}\n"
    summary_message += f"- **Location**: {user_data.get('location', 'N/A')}\n"
    summary_message += f"- **Tech Stack**: {', '.join(user_data.get('tech_stack', ['N/A']))}\n\n"
    summary_message += "Please wait while I generate your technical questions based on your tech stack. 🤖"

    st.chat_message("assistant").markdown(summary_message)
    st.session_state.messages.append({"role": "assistant", "content": summary_message})
    
    st.session_state.stage = "questions_generated"
    st.rerun()

elif st.session_state.stage == "questions_generated":
    tech_stack = st.session_state.user_info.get("tech_stack", [])
    if not tech_stack:
        st.error("No tech stack was provided to generate questions. Please restart and select one.")
        st.stop()
    
    tech_stack_string = ", ".join(tech_stack)
    llm_prompt = f"""
    You are an AI assistant specialized in generating technical interview questions.
    
    Based on the following tech stack: {tech_stack_string}
    
    Generate **exactly 5** unique, clear, and concise technical interview questions to assess a candidate's proficiency in these technologies.
    
    Format the output as a numbered list. Do not include any extra text, introductions, or explanations.
    """
    
    with st.spinner("Generating technical questions..."):
        try:
            response = model.generate_content(llm_prompt)
            questions_list = [q.strip() for q in response.text.split('\n') if q.strip()]
            
            st.session_state.technical_questions = questions_list
            st.session_state.stage = "ask_question"
            st.session_state.current_question_index = 0
            st.rerun()
        
        except Exception as e:
            st.error(f"Failed to generate questions. Please try again. Error: {e}")
            st.stop()


elif st.session_state.stage == "ask_question":
    questions = st.session_state.technical_questions
    current_index = st.session_state.current_question_index
    
    if current_index < len(questions):
        question = questions[current_index]
        st.chat_message("assistant").markdown(question)
        st.session_state.messages.append({"role": "assistant", "content": question})
        st.session_state.stage = "awaiting_answer"
        st.rerun()
    else:
        st.chat_message("assistant").markdown("You have answered all the questions in this set. Do you want to answer more questions?")
        st.session_state.messages.append({"role": "assistant", "content": "You have answered all the questions in this set. Do you want to answer more questions?"})
        st.session_state.stage = "awaiting_more_questions_answer"
        st.rerun()

elif st.session_state.stage == "awaiting_answer":
    user_answer = st.chat_input("Enter your answer here...")
    
    if user_answer:
        st.chat_message("user").markdown(user_answer)
        st.session_state.messages.append({"role": "user", "content": user_answer})
        
        if "answers" not in st.session_state.user_info:
            st.session_state.user_info["answers"] = []

        question_index = st.session_state.current_question_index
        if question_index < len(st.session_state.technical_questions):
            question_text = st.session_state.technical_questions[question_index]
            st.session_state.user_info["answers"].append({
                "question": question_text,
                "answer": user_answer
            })
        
        st.session_state.current_question_index += 1
        st.session_state.stage = "ask_question"
        st.rerun()

elif st.session_state.stage == "awaiting_more_questions_answer":
    user_response = st.chat_input("Enter 'yes' to continue or 'no' to finish.")
    
    if user_response:
        st.chat_message("user").markdown(user_response)
        st.session_state.messages.append({"role": "user", "content": user_response})
        
        response_lower = user_response.lower()
        if "yes" in response_lower or "yep" in response_lower or "sure" in response_lower:
            st.chat_message("assistant").markdown("Great! Generating the next set of questions...")
            st.session_state.messages.append({"role": "assistant", "content": "Great! Generating the next set of questions..."})
            st.session_state.current_question_index = 0
            st.session_state.technical_questions = None
            st.session_state.stage = "questions_generated"
            st.rerun()
        elif "no" in response_lower or "nope" in response_lower or "nah" in response_lower:
            st.session_state.stage = "generate_summary"
            st.rerun()
        else:
            st.chat_message("assistant").markdown("I didn't understand that. Please enter 'yes' or 'no'.")
            st.session_state.messages.append({"role": "assistant", "content": "I didn't understand that. Please enter 'yes' or 'no'."})
            st.rerun()

elif st.session_state.stage == "generate_summary":
    user_info = st.session_state.user_info
    
    if "answers" not in user_info or not user_info["answers"]:
        st.error("No answers were collected. Cannot generate a summary.")
        st.stop()

    with st.spinner("Analyzing your responses and generating the summary..."):
        qa_pairs_string = ""
        for i, pair in enumerate(user_info["answers"]):
            qa_pairs_string += f"Question {i+1}: {pair['question']}\nAnswer {i+1}: {pair['answer']}\n\n"

        llm_prompt = f"""
        You are a seasoned technical mentor and career advisor. Provide a concise summary of the candidate's technical interview performance. Address the candidate directly using "you".

        **Candidate Profile:**
        - Years of Experience: {user_info.get('years_of_experience', 'N/A')}
        - Declared Tech Stack: {', '.join(user_info.get('tech_stack', ['N/A']))}

        **Interview Transcript:**
        {qa_pairs_string}

        The summary must include:
        1.  **Strengths & Analysis:** An overall analysis of your answers compared to your tech stack and experience.
        2.  **Areas for Improvement:** Specific areas or concepts you should focus on to improve.give the area and points to that respective area as short as possible not in paragraph
        3.  **Additional Tech Stack:** Suggest 2-3 additional, relevant technologies to learn.
        4.  **Overall Score:** A single holistic score out of 5 (e.g., "3/5"). This score should be a holistic assessment of their performance, not a simple count of correct answers. For example, a score of 4/5 indicates a strong performance with some minor gaps.

        End with a final, happy, and positive concluding sentence. Do not use a number or heading for this final sentence.
        
        Format your response using clear headings and bullet points.
        """
        
        try:
            response = model.generate_content(llm_prompt)
            st.chat_message("assistant").markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            st.session_state.stage = "end_session"
            st.rerun()

        except Exception as e:
            st.error(f"Failed to generate summary. Please try again later. Error: {e}")
            st.session_state.stage = "generate_summary" 
            st.rerun()

elif st.session_state.stage == "end_session":
    st.chat_message("assistant").markdown("Thank you for your time. The interview session is now complete. Happy learning 👋")
    st.session_state.messages.append({"role": "assistant", "content": "Thank you for your time. The interview session is now complete. Happy learning 👋"})
    st.stop()