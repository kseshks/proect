from openai import OpenAI

from app.core.config import settings
from app.models.topic import Topic

client = OpenAI(
    api_key=settings.DEEPSEEK_API_KEY,
    base_url=settings.DEEPSEEK_BASE_URL,
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


def ask_deepseek(topic_title: str, context: str, question_text: str) -> str:
     prompt = build_prompt(topic_title, context, question_text)

     response = client.chat.completions.create(
         model=settings.DEEPSEEK_MODEL,
         messages=[
             {"role": "system", "content": "Ты полезный и аккуратный учебный помощник."},
             {"role": "user", "content": prompt},
         ],
         temperature=0.2,
         max_tokens=1200,
     )

     return response.choices[0].message.content or ""