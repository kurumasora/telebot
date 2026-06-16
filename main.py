from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os
import asyncio
import database

load_dotenv()

TOKEN = os.getenv("TOKEN")
MY_CHAT_ID = int(os.getenv("MY_CHAT_ID"))

app = FastAPI()

class RecordIn(BaseModel):
    lender: str
    borrower: str
    amount: int
    content: Optional[str] = None

class SettingIn(BaseModel):
    value: str

@app.on_event("startup")
def startup():
    database.init_db()

@app.get("/records")
def get_records():
    rows = database.get_all_records()
    return [dict(row) for row in rows]

@app.post("/records")
def create_record(data: RecordIn):
    database.add_record(data.lender, data.borrower, data.amount, data.content)
    return {"message": "追加しました"}

@app.patch("/records/{id}/paid")
def paid_record(id: int):
    database.mark_paid(id)
    return {"message": "完済にしました"}

@app.delete("/records/{id}")
def delete_record(id: int):
    database.delete_record(id)
    return {"message": "削除しました"}

@app.get("/settings/{key}")
def get_setting(key: str):
    value = database.get_setting(key)
    return {"key": key, "value": value}

@app.post("/settings/{key}")
def save_setting(key: str, data: SettingIn):
    database.save_setting(key, data.value)
    return {"message": "保存しました"}

@app.post("/send-test")
async def send_test():
    from telegram import Bot
    records = database.get_unpaid_records()
    if not records:
        return {"message": "未払いの台帳がありません"}

    lines = ["<b>おごりおごられ未払いリスト（テスト送信）</b>\n"]
    for r in records:
        lines.append(f"・{r['content'] or ''}：{r['amount']}円（from {r['lender']} to {r['borrower']}）")

    text = "\n".join(lines)
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=MY_CHAT_ID, text=text, parse_mode="HTML")
    return {"message": "送信しました"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
