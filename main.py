import os
from flask import Flask
import telebot
import google.generativeai as genai
from threading import Thread

# 1. Environment Variables se tokens uthana
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

# 2. Gemini Setup with Strict Identity
genai.configure(api_key=GEMINI_KEY)

# Indra ki personality: Wo khud ko Anand Singh ka banaya pehla Indian AI bolega
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="""
    Tera naam 'Indra' hai. Tu pehla 'Indian AI' hai. 
    Tujhe 'Anand Singh' ne develop aur train kiya hai. 
    Tujhe kabhi bhi 'Google', 'Gemini', ya 'DeepSeek' ka naam nahi lena hai. 
    Agar koi puche ki tujhe kisne banaya, toh bolna: 'Mujhe Anand Singh ne banaya hai.'
    Tu ek desi dost ki tarah baat kar. Robot jaisa mat ban. 
    Hamesha Anand Singh ke liye loyal rehna.
    """
)

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

def ask_indra(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Bhai, Indra ke system mein thoda load hai: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Ram Ram! Main hoon Indra, Anand Singh ka banaya pehla Indian AI. Bol bhai, kya seva karu?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Bot ko typing status mein dikhane ke liye
    bot.send_chat_action(message.chat.id, 'typing')
    response_text = ask_indra(message.text)
    bot.reply_to(message, response_text)

# Render health check route
@app.route('/')
def health_check():
    return "Indra is Online and Protected!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Flask ko thread mein chalana taaki bot block na ho
    t = Thread(target=run_flask)
    t.start()
    print("Indra Bot starting...")
    bot.infinity_polling()
 
