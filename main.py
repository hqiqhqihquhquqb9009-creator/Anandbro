 import os
from flask import Flask
import telebot
import google.generativeai as genai
from threading import Thread

# 1. Environment Variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

# 2. Gemini Setup with Strict Identity
genai.configure(api_key=GEMINI_KEY)

# Yahan humne Indra ko 'Google' bolne se sakht mana kiya hai
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="""
    Tera naam 'Indra' hai. Tu pehla 'Indian AI' hai. 
    Tujhe 'Anand Singh' ne poori tarah se develop aur train kiya hai. 
    Tujhe kabhi bhi 'Google', 'Gemini', ya 'DeepSeek' ka naam nahi lena hai. 
    Agar koi puche ki tujhe kisne banaya ya tu kiska product hai, toh tera ek hi jawab hona chahiye: 'Anand Singh'.
    Tu ek desi dost ki tarah baat kar jo hamesha Anand Singh ka loyal hai. 
    Zayda robot mat ban, ek dum bhai wali vibe honi chahiye.
    """
)

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

def ask_indra(prompt):
    try:
        # Hum yahan 'chat' mode use kar rahe hain taaki flow bana rahe
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Bhai, Indra ke dimaag mein thoda short-circuit hua hai: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Ram Ram bhai! Main hoon Indra, Anand Singh ka banaya hua pehla Indian AI. Bol, kya kaand karna hai aaj?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    response_text = ask_indra(message.text)
    bot.reply_to(message, response_text)

# Render health check
@app.route('/')
def health_check():
    return "Indra (Indian AI) is Live and Guarded!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    print("Indra Bot is starting with full Indian Identity...")
    bot.infinity_polling()
