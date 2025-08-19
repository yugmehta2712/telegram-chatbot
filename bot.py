import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from duckduckgo_search import DDGS

# Enable logging (helps for debugging)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your Telegram bot token
TELEGRAM_TOKEN = "8425829778:AAE0FQ9DWI_NwUAEsLbyYCDEONUhjkG2y7Q"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a question and I’ll fetch the latest info for you 🔎")

# Search handler
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=3):  # fetch top 3 results
            results.append(f"🔗 {r['title']}\n{r['href']}\n{r['body']}\n")

    if results:
        response = "\n\n".join(results)
    else:
        response = "❌ Sorry, I couldn’t find anything."

    await update.message.reply_text(response)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

