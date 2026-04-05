from app.models.topic import Topic
from app.models.topic_material import TopicMaterial


def generate_answer(topic: Topic, materials: list[TopicMaterial], question_text: str) -> str:
    # Пока заглушка.
    # Потом сюда подключить LLM.
    materials_text = ", ".join(
        [m.title or m.url or m.original_name or "материал" for m in materials]
    ) or "без материалов"

    return (
        f"Заглушка ответа.\n"
        f"Тема: {topic.title}\n"
        f"Вопрос: {question_text}\n"
        f"Материалы: {materials_text}"
    )