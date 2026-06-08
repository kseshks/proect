from openai import OpenAI

from app.core.config import settings
from app.models.topic import Topic

openrouter_client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url=settings.OPENROUTER_BASE_URL,
)

MODELS = [
    # Быстрые
    {"name": "Gemma 3 1B", "model": "google/gemma-3-1b-it:free"},
    {"name": "Llama 3.2 3B", "model": "meta-llama/llama-3.2-3b-instruct:free"},
    {"name": "Phi-3 Mini", "model": "microsoft/phi-3-mini-128k-instruct:free"},
    
    # Средние
    {"name": "Gemma 3 4B", "model": "google/gemma-3-4b-it:free"},
    {"name": "Qwen 2.5 7B", "model": "qwen/qwen-2.5-7b-instruct:free"},
    {"name": "Liquid LFM 7B", "model": "liquid/lfm-7b:free"},
    
    # Медленные
    {"name": "Gemma 3 12B", "model": "google/gemma-3-12b-it:free"},
    {"name": "Phi-3 Medium", "model": "microsoft/phi-3-medium-128k-instruct:free"},
    {"name": "Mistral Nemo", "model": "mistralai/mistral-nemo:free"},
    
    # Самый умный, но медленный
    {"name": "Nemotron 3 Ultra", "model": "nvidia/nemotron-3-ultra-550b-a55b:free"},
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