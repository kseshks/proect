from openai import OpenAI

from app.core.config import settings
from app.models.topic import Topic

client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url=settings.OPENROUTER_BASE_URL,
)


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


def ask_nemotron(topic_title: str, context: str, question_text: str) -> str:
    prompt = build_prompt(topic_title, context, question_text)

    try:
        response = client.chat.completions.create(
            model=settings.OPENROUTER_MODEL,
            messages=[
                {"role": "system", "content": "Ты полезный учебный помощник. Отвечай на русском языке."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1200,
        )

        if response and response.choices and len(response.choices) > 0:
            choice = response.choices[0]
            if choice.message and choice.message.content:
                return choice.message.content

        return "Модель не вернула ответ. Попробуйте ещё раз."

    except Exception as e:
        return f"Ошибка при запросе к ИИ: {str(e)}"