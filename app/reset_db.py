from sqlalchemy import text
from database import engine
from models import Base

print("正在暴力清除所有舊資料...")

with engine.connect() as connection:
    connection.execute(text("DROP SCHEMA public CASCADE;"))
    connection.execute(text("CREATE SCHEMA public;"))
    connection.commit()

print("建立新資料表格...")
Base.metadata.create_all(bind=engine)

print("已成功重建資料庫！")