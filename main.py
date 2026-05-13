import os
from flask import Flask
import telebot
import google.generativeai as genai
from threading import Thread

# 1. API Configuration
# Humne transport ko 'rest' pe set kiya hai aur v1 stable version force kiya hai
API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')

if API_KEY:
    genai.configure(api_key=API_KEY, transport='rest')

# 2. Model Setup
# 'gemini-1.5-flash' stable version hai, models/ prefix ke saath
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    system_instruction="""
    Tera naam Indra hai. Tu pehla Indian AI hai jise Anand Singh ne banaya hai. 
    Tu ek desi dost hai. Google, Gemini ya DeepSeek ka naam kabhi mat lena. 
    Hamesha Anand Singh ka loyal rehna.
    """
)

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
app = Flask(__name__)

def ask_indra(prompt):
    try:
        # Simple and direct content generation
        response = model.generate_content(prompt)
        # Check if response exists and has text
        if response and response.text:
            return response.text
        else:
            return "Bhai, Indra abhi soch raha hai, thodi der mein puchna!"
    except Exception as e:
        # Agar ab bhi error aaye toh ye exact message dikhayega
        return f"Indra Error: {str(e)}"

@bot.message_handler(func=lambda m: True)
def handle(m):
    try:
        bot.send_chat_action(m.chat.id, 'typing')
        response_text = ask_indra(m.text)
        bot.reply_to(m, response_text)
    except Exception as e:
        print(f"Bot Error: {e}")

@app.route('/')
def home():
    return "Indra is Live and Stable!"

def run():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Flask thread start
    t = Thread(target=run)
    t.start()
    print("Indra is waking up...")
    # Polling with conflict resolution
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
    
