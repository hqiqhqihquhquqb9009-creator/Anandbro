import os
from flask import Flask
import telebot
import google.generativeai as genai
from threading import Thread

# 1. API Chabi Setup
API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')

# 2. Force STABLE Version (Sabse bada fix yahi hai)
if API_KEY:
    # Hum yahan rest api version 1 force kar rahe hain
    genai.configure(api_key=API_KEY, transport='rest')

# 3. Indra Identity Setup
# Note: Agar 'models/gemini-1.5-flash' na chale, toh sirf 'gemini-1.5-flash' likhna
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash', 
    system_instruction="Tera naam Indra hai. Tu pehla Indian AI hai. Anand Singh ne tujhe banaya hai. Google ka naam mat lena."
)

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
app = Flask(__name__)

def ask_indra(prompt):
    try:
        # Pura naya tarika reply lene ka
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Agar ab bhi v1beta bole, toh hum error ko bypass karenge
        return f"Indra System Message: {str(e)}"

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        bot.send_chat_action(m.chat.id, 'typing')
        jawaab = ask_indra(m.text)
        bot.reply_to(m, jawaab)
    except:
        pass

@app.route('/')
def home(): return "Indra Stable v1 is Online!"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling(non_stop=True)
    
