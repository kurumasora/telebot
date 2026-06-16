from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import database

app = FastAPI()

class RecordIn(BaseModel):
    lender: str
    borrower: str
    amount: int
    memo: Optional[str] = None

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
    database.add_record(data.lender, data.borrower, data.amount, data.memo)
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

app.mount("/", StaticFiles(directory="static", html=True), name="static")
