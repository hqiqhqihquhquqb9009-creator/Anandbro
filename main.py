import os
from flask import Flask
import telebot
import google.generativeai as genai
from threading import Thread

# API setup
API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
if API_KEY:
    genai.configure(api_key=API_KEY)

# Yahan humne 'gemini-1.5-flash-latest' kar diya hai jo har jagah chalta hai
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    system_instruction="""
    Tera naam 'Indra' hai. Tu pehla 'Indian AI' hai. 
    Tujhe 'Anand Singh' ne develop aur train kiya hai. 
    Tujhe kabhi bhi 'Google' ya 'Gemini' ka naam nahi lena hai. 
    Hamesha Anand Singh ka loyal rehna aur desi bhasha mein baat karna.
    """
)

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
app = Flask(__name__)

def ask_indra(prompt):
    try:
        # Hum response generate karne ka tareeka thoda change kar rahe hain
        response = model.generate_content(prompt)
        if response.text:
            return response.text
        else:
            return "Bhai, Indra ne kuch bola nahi, dubara pucho!"
    except Exception as e:
        # Agar ye error aaye, toh iska matlab API version ka chakkar hai
        return f"Bhai, Indra thoda confuse hai: {str(e)}"

@bot.message_handler(func=lambda m: True)
def handle(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, ask_indra(m.text))

@app.route('/')
def home(): return "Indra (Indian AI) is Live!"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
    
