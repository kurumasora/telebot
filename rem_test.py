import datetime
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, ContextTypes
from telegram.constants import ParseMode

load_dotenv()

# --- 設定 ---
TOKEN = os.getenv('TOKEN')
MY_CHAT_ID = int(os.getenv('MY_CHAT_ID'))

# HTML形式のリマインダー内容
async def send_styled_reminder(context: ContextTypes.DEFAULT_TYPE):
    # 現在時刻を取得
    now = datetime.datetime.now().strftime('%H:%M:%S')
    
    # 送信するメッセージ（HTMLタグを使用）
    text = (
        f"<b>【定期リマインダー(テスト)】</b>\n"
        f"現在の時刻： <code>{now}</code>\n\n"
        f"📌 <b>本日の予定</b>\n"
        f"・<pre>python-telegram-bot</pre> の実装テスト\n"
        f"・コードの改良とデバッグ\n\n"
        f"<i>※このメッセージは10秒ごとに送信されます。</i>\n"
        f"<a href='https://core.telegram.org/bots/api#formatting-options'>公式のHTMLリファレンス</a>"
    )

    await context.bot.send_message(
        chat_id=MY_CHAT_ID, 
        text=text,
        parse_mode=ParseMode.HTML  # HTML形式を有効化
    )
    print(f"[{now}] リマインダーを送信しました。")

def main():
    # Applicationの作成
    application = ApplicationBuilder().token(TOKEN).build()
    job_queue = application.job_queue

    # 10秒ごとに繰り返し実行 (intervalは秒単位)
    job_queue.run_repeating(send_styled_reminder, interval=10, first=1)

    print("Bot稼働中... (10秒ごとにHTML形式で送信します)")
    application.run_polling()

if __name__ == '__main__':
    main()