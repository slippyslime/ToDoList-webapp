from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler

TOKEN = '' # - Вставить ваш API токен бота в телеграме


async def start(update, context):
    domen = "" # - Вставить ваш домен
    telegram_user_id = str(update.message.from_user.id)
    web_app_url = f"{domen}/?user_id={telegram_user_id}"
    keyboard = [
        [InlineKeyboardButton("Open Web App", web_app={"url": web_app_url})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Click the button below to open the Web App:", reply_markup=reply_markup)


def main():
    application = Application.builder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()


if __name__ == '__main__':
    main()