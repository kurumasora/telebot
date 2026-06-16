import datetime
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, ContextTypes
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

load_dotenv()

# --- 設定項目 ---
TOKEN = os.getenv('TOKEN')
TARGET_IDS = [int(i) for i in os.getenv('TARGET_IDS').split(',')]


async def start_command(update: ContextTypes.DEFAULT_TYPE, context: ContextTypes.DEFAULT_TYPE):
    # ユーザー名を取得（設定されていない場合は「ユーザー」とする）
    user_name = update.effective_user.first_name
    
    welcome_text = (
        f"<b>Hello {user_name}</b>\n\n"
        "Thank you for using @azuki_reminder_bot\n"
    )
    
    # 相手にメッセージを返信
    await update.message.reply_text(text=welcome_text, parse_mode=ParseMode.HTML)
    
    # 【便利！】相手のChat IDをターミナルに表示させる（ID確認の手間が省けます）
    print(f"new_user Name: {user_name}, ID: {update.effective_chat.id}")


# 送信するリマインダーの内容
async def daily_reminder_task(context: ContextTypes.DEFAULT_TYPE):
    # メッセージのデザイン（HTML形式）
    # ※ 友達が読みやすいよう、丁寧な表現にしています
    text = (
        "<b>おごりおごられ定期リマインダー</b>\n\n"
        "・はま代：2500円現金で\n"
        "・コメダ：1090円\n"
        "・二郎 ：1100円\n\n"
        
        "from <a href='https://t.me/azuki_komame'>@azuki_komame</a>"
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
            # 友達がBotをブロックしたり、まだStartを押していない場合にエラーになります
            print(f"ID: {chat_id} への送信に失敗しました。原因: {e}")

def main():
    # Applicationの作成
    application = ApplicationBuilder().token(TOKEN).build()
    # --- ここで「/start」コマンドを登録する ---
    application.add_handler(CommandHandler("start", start_command))

    job_queue = application.job_queue

    #for_test
    ##job_queue.run_once(daily_reminder_task, when=5)


   #japan_time
    target_time = datetime.time(hour=23, minute=59, second=0)
    
    # 毎日実行するジョブを登録
    job_queue.run_daily(daily_reminder_task, time=target_time)

    print(f"リマインダーBot稼働中... (毎日 {target_time} に送信)")
    

    application.run_polling()

if __name__ == '__main__':
    main()