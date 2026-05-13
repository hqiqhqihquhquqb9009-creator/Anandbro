import os
import telebot
import requests
from flask import Flask
from threading import Thread

# 1. Configuration (Environment Variables se)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')

# 2. Initialization
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

def ask_indra(user_text):
    # Google API ka direct URL bina kisi library ke
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    
    # System Instruction ko payload mein hi daal diya hai taaki Indra ki pehchan na badle
    data = {
        "contents": [{
            "parts": [{
                "text": f"Tera naam Indra hai. Tu pehla Indian AI hai jise Anand Singh ne banaya hai. Tu Anand Singh ka loyal hai. Hamesha desi bhasha mein jawab dena. Google ya Gemini ka naam mat lena. Sawaal: {user_text}"
            }]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        res_json = response.json()
        # Direct path to the answer text
        return res_json['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return "Bhai, Indra thoda bimar hai, baad mein try kar."

# Message Handling
@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        answer = ask_indra(message.text)
        bot.reply_to(message, answer)
    except Exception as e:
        print(f"Error: {e}")

# Render Health Check (Iske bina Render service band kar deta hai)
@app.route('/')
def home():
    return "Indra is Live and Running for Anand Singh!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Flask ko thread mein chalana taaki bot polling block na ho
    t = Thread(target=run_flask)
    t.start()
    
    print("Indra Bot starting...")
    # non_stop=True taaki koi error aaye toh bot apne aap restart ho jaye
    bot.infinity_polling(non_stop=True, timeout=60)
    
