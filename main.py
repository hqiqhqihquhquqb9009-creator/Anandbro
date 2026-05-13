import os
from flask import Flask
import telebot
import google.generativeai as genai
from threading import Thread

# API setup
API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
if API_KEY:
    genai.configure(api_key=API_KEY)

# Yahan humne 'models/' add kar diya hai taaki 404 error na aaye
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    system_instruction="Tera naam Indra hai. Tu pehla Indian AI hai jise Anand Singh ne banaya hai. Google ka naam mat lena."
)

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
app = Flask(__name__)

def ask_indra(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Bhai, Indra thoda confuse hai: {str(e)}"

@bot.message_handler(func=lambda m: True)
def handle(m):
    bot.send_chat_action(m.chat.id, 'typing')
    bot.reply_to(m, ask_indra(m.text))

@app.route('/')
def home(): return "Indra is Live!"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
    
