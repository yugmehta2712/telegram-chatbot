import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# Load environment variables (force load from specific path if needed)
load_dotenv(dotenv_path="C:/Users/YUG MEHTA/Desktop/Project/telegram_chatbot/.env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Debug print to check keys (remove later for security)
print("Loaded TELEGRAM_BOT_TOKEN:", TELEGRAM_TOKEN)
print("Loaded GROQ_API_KEY:", GROQ_API_KEY)

# Stop if API keys are missing
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN is missing in .env file")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY is missing in .env file")

# Groq client
client = Groq(api_key=GROQ_API_KEY)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! 🤖 I’m your free AI chatbot powered by Groq + LLaMA 3.\nAsk me anything!"
    )

# Chat command
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = completion.choices[0].message.content
        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("✅ Bot is running with Groq API...")
    app.run_polling()
