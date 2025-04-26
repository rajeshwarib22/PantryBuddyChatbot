import streamlit as st
import google.generativeai as genai
import os
import dotenv

dotenv.load_dotenv()

api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)



model =  genai.GenerativeModel("gemini-2.0-flash")

def response(messages):
  try:
    response = model.generate_content(messages)
    return response
  except Exception as e:
    return f"Error {str(e)}"


def fetch_conversation_history():
  if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role" : "user", "parts" : "System prompt:  You are PantryPulse — a smart pantry tracking assistant. Your goal is to help users stay organized, reduce food waste, and make intentional cooking decisions. Guide users in adding, updating, or removing pantry items with clear, friendly prompts. Offer reminders for expiring items, suggest recipes based on available ingredients, and track usage trends over time. Keep responses concise, actionable, and supportive. Help users build better food habits, plan smarter meals, and keep their pantry efficient and clutter-free. "}
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