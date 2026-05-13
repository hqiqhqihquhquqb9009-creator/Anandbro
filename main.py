import os
from flask import Flask
import telebot
import google.generativeai as genai
from threading import Thread

# API Key setup
API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
if API_KEY:
    genai.configure(api_key=API_KEY)

# Simple Model Setup
model = genai.GenerativeModel('gemini-pro') 

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
app = Flask(__name__)

def ask_indra(prompt):
    try:
        # Pura desi instruction yahan bhejenge har baar
        full_prompt = f"Tera naam Indra hai. Anand Singh ne banaya hai. Desi bhasha mein jawab de. Sawaal: {prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Indra thoda bimar hai, baad mein try kar bhai: {str(e)}"

@bot.message_handler(func=lambda m: True)
def handle(m):
    reply = ask_indra(m.text)
    bot.reply_to(m, reply)

@app.route('/')
def home(): return "Indra is Live!"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    Thread(target=run).start()
    bot.infinity_polling()
    
