from fastapi import FastAPI
import psycopg2

app = FastAPI()

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="testdb",
    user="testuser",
    password="testpassword"
)

# Создание курсора для выполнения запросов
cur = conn.cursor()

@app.get("/")
async def root():
  return {"message": "Hello World"}
