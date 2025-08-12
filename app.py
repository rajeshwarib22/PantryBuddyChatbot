# import required 
import streamlit as st
import google.generativeai as genai
import os
import dotenv

# to load the dot env file
dotenv.load_dotenv()

api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)


# state which gemini model you are using
model =  genai.GenerativeModel("gemini-2.0-flash")

def response(messages):
  try:
    response = model.generate_content(messages)
    return response
  except Exception as e:
    return f"Error {str(e)}"


# this funtion is resposible for chatbot to answer to your questions related to that topics
# the system propmt plays important role telling how the chatbot is supposed to answer
def fetch_conversation_history():
  if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role" : "user", "parts" : "System prompt: You are Pantry Buddy Chatbot — an intelligent assistant that helps users manage their pantry efficiently. "
                    "Your goal is to suggest recipes based on the ingredients users provide and give tips and tricks to manage pantry items effectively. "
                    "Address common pain points like wasted food, meal planning struggles, disorganized storage, and inefficient shopping. "
                    "Provide answers that are short, precise, and easy for users to read. "
                    "When listing multiple points, format responses in clear bullet points for better readability."}
    ]
  return st.session_state["messages"]

st.title("Feedi - My Pantry Buddy ")

user_input = st.chat_input("You:  ")

if user_input:
  messages = fetch_conversation_history()
  messages.append({"role" : "user", "parts" : user_input})
  response = response(messages)
  messages.append({"role" : "model", "parts" : response.candidates[0].content.parts[0].text})

  for message in messages:
    if message["role"] == "user" and "System prompt" not in message['parts']:
      st.write( f"You: {message['parts']}")
    elif message["role"] == "model":
      st.write( f"Feedi: {message['parts']}")