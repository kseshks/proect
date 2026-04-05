from app.core.database import Base, engine
from app.models import (
    Admin,
    Teacher,
    ClassRoom,
    Student,
    Topic,
    TopicMaterial,
    TopicQuestion,
    TopicAssignment,
    TopicDialogMessage,
)


def create_tables():
    print("Создание таблиц...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы успешно созданы!")


if __name__ == "__main__":
    create_tables()