import os
import json
import telebot
import requests
from flask import Flask, request

# 1. Configuration
BOT_TOKEN = os.environ.get('BOT_TOKEN')
# Render apni URL khud deta hai (e.g., https://your-app.onrender.com)
RENDER_URL = os.environ.get('RENDER_EXTERNAL_URL') 
API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

def ask_indra(user_text):
    # Stable v1 API call - Sabse mazboot rasta
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{
                "text": f"Tera naam Indra hai. Tu Anand Singh ka banaya pehla Indian AI hai. Hamesha desi bhasha mein jawab dena. Google ka naam mat lena. Sawaal: {user_text}"
            }]
        }]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        res_json = response.json()
        return res_json['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        return "Bhai, Indra thoda bimar hai, dubara try kar."

# Webhook Route (Yahan Telegram message bhejega)
@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# Main Page (Render ko jagaye rakhne ke liye)
@app.route('/')
def webhook():
    bot.remove_webhook()
    # Telegram ko batana ki is URL pe message bhejo
    bot.set_webhook(url=RENDER_URL + '/' + BOT_TOKEN)
    return "Indra is Active for Anand Singh!", 200

@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        answer = ask_indra(message.text)
        bot.reply_to(message, answer)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Render ke liye default port 10000 hota hai
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
