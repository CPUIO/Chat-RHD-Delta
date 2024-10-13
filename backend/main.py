from .pdfreader import extractText
from model.main import get_text_embedding

from fastapi import FastAPI
import psycopg2
from annoy import AnnoyIndex
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,  # Класс мидлвари должен быть передан первым аргументом
    allow_origins=["http://localhost:5173"],  # Разрешенные источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешенные методы
    allow_headers=["*"],  # Разрешенные заголовки
)

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
  host="localhost",
  database="testdb",
  user="testuser",
  password="testpassword"
)

# Создание курсора для выполнения запросов
cur = conn.cursor()

# Создание AnnoyIndex
embedding_dim = 300  # размерность эмбеддинга
index = AnnoyIndex(embedding_dim, 'angular')  # Мера угла
index_path = "embeddings.ann"

index.build(10)  # 10 деревьев

# Загружаем индекс, если он существует
try:
  index.load(index_path)
except Exception as e:
  print(f"Не найден файл индексов Annoy: {e}")

# Определение модели данных, которая описывает входные данные (JSON)
class Message(BaseModel):
  text: str  # Ожидаемое поле "text" в JSON

@app.post("/question")
async def question(message: Message):
  # Векторизация вопроса пользователя
  question_embedding = get_text_embedding(message.question)

  # Поиск ближайших 3 абзацев, их индексов
  top_3_indices = index.get_nns_by_vector(question_embedding, 3)

  # Запрашиваем соответствующие тексты из PostgreSQL
  results = []
  for idx in top_3_indices:
    cur.execute("SELECT text FROM embeddings WHERE id = %s", (idx,))
    text = cur.fetchone()[0]  # Получаем текст абзаца
    results.append(text)
  
  # Возвращаем ответ в формате JSON
  return {results}

extracted_paragraphs = extractText("documents/Коллективный договор.pdf")
#print(extracted_paragraphs[1])

# Фильтрация пустых строк из списка параграфов
filtered_paragraphs = [p for p in extracted_paragraphs if p.strip()]

# Векторизация параграфов и сохранение в Annoy и PostgreSQL
for idx, paragraph in enumerate(filtered_paragraphs,):
  # Создание эмбеддингов
  embeddings = get_text_embedding(paragraph)
  # Сохранение текста в PostgreSQL и эмбеддинга в Annoy
  try:
    cur.execute("INSERT INTO embeddings (id, text) VALUES (%s, %s)", (idx, paragraph))
    index.add_item(idx, embeddings)
  except Exception as e:
    print(f"Ошибка при сохранении в БД и/или Annoy: {e}")

# Сохранение изменений в базе данных
conn.commit()

# Сохранение индекса Annoy на диск
index.save(index_path)

# Закрытие курсора и соединения только при завершении работы приложения
@app.on_event("shutdown")
def shutdown():
  cur.close()
  conn.close()