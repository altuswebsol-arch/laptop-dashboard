"""
Asif Bhai's Laptop Bot — v1
Telegram se laptop control karo!

Commands:
  /start       - Bot zinda hai?
  /help        - Ye madad
  /shot        - Screenshot bhejo
  /open <url>  - Browser mein website kholo
"""
import logging
import webbrowser
import subprocess
import sys

# ============ APNI DETAILS YAHAN DALO ============
BOT_TOKEN = "APNA_TOKEN_YAHAN_DALO"      # BotFather se mila token
MY_USER_ID = 0                            # Apni Telegram user ID (BotFather/@userinfobot se)
# =================================================

logging.basicConfig(level=logging.INFO)

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes
except ImportError:
    print("Pehle ye chalao: pip install python-telegram-bot Pillow mss")
    sys.exit(1)


def only_me(func):
    """Sirf malik ke commands chalenge."""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != MY_USER_ID:
            await update.message.reply_text("⛔ Sirf malik hukum de sakta hai!")
            return
        await func(update, context)
    return wrapper


@only_me
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Salam Asif Bhai! Bot hazir hai!\n"
        "/help likho sare commands ke liye."
    )


@only_me
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Commands:\n"
        "/shot - Screenshot lo\n"
        "/open <website> - Browser mein kholo\n"
        "Misal: /open google.com"
    )


@only_me
async def shot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        from mss import mss
        with mss() as sct:
            sct.shot(output="screen.png")
        await update.message.reply_photo(
            photo=open("screen.png", "rb"),
            caption="📸 Ye lo screenshot!"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Masla: {e}")


@only_me
async def open_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Website ka naam bhi likho! Misal: /open google.com")
        return
    url = context.args[0]
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    await update.message.reply_text(f"🌐 Khol diya: {url}")


def main():
    if BOT_TOKEN == "APNA_TOKEN_YAHAN_DALO" or MY_USER_ID == 0:
        print("❌ Pehle BOT_TOKEN aur MY_USER_ID set karo file mein!")
        sys.exit(1)
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("shot", shot))
    app.add_handler(CommandHandler("open", open_url))
    print("🤖 Bot chal raha hai... band karne ke liye Ctrl+C dabao")
    app.run_polling()


if __name__ == "__main__":
    main()
