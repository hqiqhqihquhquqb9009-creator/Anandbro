import os
from flask import Flask
import telebot
from openai import OpenAI
from threading import Thread

# 1. Environment Variables se tokens uthana
BOT_TOKEN = os.environ.get('BOT_TOKEN')
HF_TOKEN = os.environ.get('HF_TOKEN')

# 2. Bot aur AI Client setup
bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

app = Flask(__name__)

def ask_deepseek(user_query):
    try:
        chat_completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V4-Pro:novita",
            messages=[
                {"role": "user", "content": user_query}
            ],
            max_tokens=500
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Bhai, thoda error aa gaya: {str(e)}"

# Telegram Commands
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Ram Ram bhai! Tera DeepSeek Bot taiyar hai. Kuch bhi pooch!")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # Bot ko 'typing' status mein dikhane ke liye
    bot.send_chat_action(message.chat.id, 'typing')
    
    response = ask_deepseek(message.text)
    bot.reply_to(message, response)

# 3. Render ke liye Flask Health Check
@app.route('/')
def home():
    return "Bot is Alive!"

def run():
    # Render automatically PORT environment variable deta hai
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Flask ko alag thread mein chalana taaki bot block na ho
    t = Thread(target=run)
    t.start()
    
    print("Bot is starting...")
    bot.infinity_polling()
    
