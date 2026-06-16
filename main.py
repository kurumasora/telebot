from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import database

app = FastAPI()

# 台帳追加のときに受け取るデータの形を定義
class RecordIn(BaseModel):
    lender: str
    borrower: str
    amount: int
    memo: Optional[str] = None
    remind_at: Optional[str] = None

# 起動時にDBを初期化
@app.on_event("startup")
def startup():
    database.init_db()

# 台帳一覧取得
@app.get("/records")
def get_records():
    rows = database.get_all_records()
    return [dict(row) for row in rows]

# 台帳追加
@app.post("/records")
def create_record(data: RecordIn):
    remind_at_utc = None
    if data.remind_at:
        jst = datetime.fromisoformat(data.remind_at)
        remind_at_utc = (jst - timedelta(hours=9)).strftime("%Y-%m-%dT%H:%M")
    database.add_record(data.lender, data.borrower, data.amount, data.memo, remind_at_utc)
    return {"message": "追加しました"}

# 完済マーク
@app.patch("/records/{id}/paid")
def paid_record(id: int):
    database.mark_paid(id)
    return {"message": "完済にしました"}

# 削除
@app.delete("/records/{id}")
def delete_record(id: int):
    database.delete_record(id)
    return {"message": "削除しました"}

# 静的ファイル（HTML/CSS/JS）を配信
app.mount("/", StaticFiles(directory="static", html=True), name="static")