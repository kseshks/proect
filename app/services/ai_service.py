from openai import OpenAI

from app.core.config import settings
from app.models.topic import Topic

openrouter_client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url=settings.OPENROUTER_BASE_URL,
)

MODELS = [
    # Быстрые
    {"name": "Nemotron Nano 9B", "model": "nvidia/nemotron-nano-9b-v2:free"},
    {"name": "Liquid LFM 2.5", "model": "liquid/lfm-2.5-1.2b-instruct:free"},
    {"name": "GPT-OSS 20B", "model": "openai/gpt-oss-20b:free"},
    
    # Средние
    {"name": "Gemma 4 31B", "model": "google/gemma-4-31b-it:free"},
    {"name": "Qwen 3 Next 80B", "model": "qwen/qwen3-next-80b-a3b-instruct:free"},
    {"name": "GLM-4.5 Air", "model": "z-ai/glm-4.5-air:free"},
    
    # Мощные
    {"name": "Gemma 4 26B", "model": "google/gemma-4-26b-a4b-it:free"},
    {"name": "Nemotron Super 120B", "model": "nvidia/nemotron-3-super-120b-a12b:free"},
    {"name": "GPT-OSS 120B", "model": "openai/gpt-oss-120b:free"},
    {"name": "Kimi K2.6", "model": "moonshotai/kimi-k2.6:free"},
]

def build_topic_context(topic: Topic, max_chars: int = 12000) -> str:
    parts = []
    for material in topic.materials:
        if material.parse_status != "success" or not material.extracted_text:
            continue
        text = material.extracted_text.strip()
        if not text:
            continue
        remaining = max_chars - len("\n\n".join(parts))
        if remaining <= 0:
            break
        parts.append(text[:remaining])
    return "\n\n".join(parts).strip()


def build_prompt(topic_title: str, context: str, question_text: str) -> str:
    return f"""Ты учебный помощник.
Тема: {topic_title}

Учебный материал:
{context}

Ответь на вопрос ученика только на основе материала. Отвечай на русском языке.

Вопрос: {question_text}"""


def ask_openai(model: str, prompt: str) -> str:
    response = openrouter_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Ты полезный учебный помощник. Отвечай на русском."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=800,
    )
    return response.choices[0].message.content


def ask_ai(topic_title: str, context: str, question_text: str) -> str:
    prompt = build_prompt(topic_title, context, question_text)

    for model_config in MODELS:
        try:
            result = ask_openai(model_config["model"], prompt)
            if result:
                return result
        except Exception as e:
            print(f"Ошибка {model_config['name']}: {str(e)[:100]}")
            continue

    return "Все ИИ-модели сейчас недоступны. Попробуйте позже."