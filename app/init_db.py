from database import engine
from models import Base
import models 

print("正在連線到資料庫...")
print(f"資料庫位址: {engine.url}")


print("正在建立表格...")
# 這行指令會去檢查資料庫，如果表不存在就建立，已存在就不動
Base.metadata.create_all(bind=engine)


print("✅ 表格建立完成！")