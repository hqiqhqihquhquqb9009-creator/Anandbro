import os
from flask import Flask
import telebot
from openai import OpenAI
from threading import Thread

# Environment Variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
HF_TOKEN = os.environ.get('HF_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

app = Flask(__name__)

def ask_indra(user_query):
    try:
        chat_completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V4-Pro:novita",
            messages=[
                {
                    "role": "system", 
                    "content": """
                    Tera naam 'Indra' hai. 
                    Tu pehla 'Indian AI' hai. 
                    Tujhe 'Anand Singh' ne train aur develop kiya hai. 
                    Tujhe kabhi nahi bolna ki tu DeepSeek ya koi aur AI hai. 
                    Agar koi puche kisne banaya, toh garv se Anand Singh ka naam lena. 
                    Dost ki tarah desi bhasha mein baat kar.
                    """
                },
                {"role": "user", "content": user_query}
            ],
            max_tokens=500
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Bhai, thoda system garam ho gaya hai: {str(e)}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Ram Ram! Main hoon Indra, Bharat ka apna AI. Anand Singh ne mujhe taiyar kiya hai. Bol bhai, kya seva karu?")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.send_chat_action(message.chat.id, 'typing')
    response = ask_indra(message.text)
    bot.reply_to(message, response)

@app.route('/')
def home():
    return "Indra is Online!"

def run():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Indra Bot is starting...")
    bot.infinity_polling()
  
