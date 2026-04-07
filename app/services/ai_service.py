from app.models.topic import Topic


def build_topic_context(topic: Topic, max_chars: int = 12000) -> str:
    parts = []
    current_length = 0

    for material in topic.materials:
        if material.parse_status != "success":
            continue
        if not material.extracted_text:
            continue

        text = material.extracted_text.strip()
        if not text:
            continue

        remaining = max_chars - current_length
        if remaining <= 0:
            break

        chunk = text[:remaining]
        parts.append(chunk)
        current_length += len(chunk)

    return "\n\n".join(parts).strip()


def build_prompt(topic_title: str, context: str, question_text: str) -> str:
    return f"""
Ты учебный помощник.

Тема: {topic_title}

Ниже дан учебный материал:
{context}

Ответь на вопрос ученика только на основе этого материала.

Вопрос:
{question_text}
""".strip()


def call_llm(prompt: str) -> str:
    # Пока заглушка
    return "Это тестовый ответ нейронки."