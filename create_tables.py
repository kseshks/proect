from app.core.database import engine, Base
from app.models import (
    Teacher, Student, Test, Question,
    Answer, TestResult, StudentAnswer
)

def create_tables():
    print("Создание таблиц...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы успешно созданы!")

if __name__ == "__main__":
    create_tables()