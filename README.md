# High-Concurrency Booking System (Ticket Master)

這是一個基於 Python FastAPI 與 PostgreSQL 的高併發搶票系統後端原型。
實作了完整的 JWT 身份驗證、Argon2 密碼加密，以及 ORM 資料庫關聯設計。

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Database:** PostgreSQL, SQLAlchemy (ORM)
- **Security:** JWT (JSON Web Tokens), Argon2 Password Hashing, Pydantic Validation

## 🚀 Key Features
1. **User Authentication**: 完整的註冊、登入流程，發放 JWT Token。
2. **Ticket Booking**: 實作一對多 (User -> Items) 資料庫關聯，防止資料孤島。
3. **Security Best Practices**: 
    - 密碼絕不明碼儲存 (使用 Argon2)。
    - API 路由保護 (Dependency Injection 驗證 Token)。
    - Pydantic Schema 確保資料輸入輸出格式 (避免洩漏敏感欄位)。

## ⚙️ Setup & Run
```bash
# 1. Clone project
git clone [https://github.com/你的帳號/你的專案名.git](https://github.com/你的帳號/你的專案名.git)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup Environment Variables
# Create .env file and add: DATABASE_URL=postgresql://...

# 4. Run Server
uvicorn main:app --reload
