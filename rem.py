import datetime
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.constants import ParseMode
import database

load_dotenv()

TOKEN = os.getenv('TOKEN')
TARGET_IDS = [int(i) for i in os.getenv('TARGET_IDS').split(',')]


async def start_command(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"<b>Hello {user_name}</b>\n\n"
        "Thank you for using @azuki_reminder_bot\n"
    )
    await update.message.reply_text(text=welcome_text, parse_mode=ParseMode.HTML)
    print(f"new_user Name: {user_name}, ID: {update.effective_chat.id}")


# DBを定期チェックしてリマインドを送信
async def check_reminders(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M")
    records = database.get_pending_reminders(now)

    for record in records:
        text = (
            f"<b>リマインダー</b>\n\n"
            f"・{record['lender']} → {record['borrower']}\n"
            f"・{record['amount']}円\n"
            f"・{record['memo'] or ''}\n"
        )
        for chat_id in TARGET_IDS:
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode=ParseMode.HTML
                )
                print(f"ID: {chat_id} へ送信成功")
            except Exception as e:
                print(f"ID: {chat_id} への送信に失敗: {e}")

        database.mark_reminded(record['id'])


def main():
    database.init_db()

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))

    job_queue = application.job_queue

    # 1分ごとにDBをチェック
    job_queue.run_repeating(check_reminders, interval=60, first=5)

    print("リマインダーBot稼働中...")
    application.run_polling()


if __name__ == '__main__':
    main()