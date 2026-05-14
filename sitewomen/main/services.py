import requests
from django.conf import settings

def get_ai_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {getattr(settings, 'OPENROUTER_API_KEY', '')}",
        "HTTP-Referer": getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000/'),
        "Content-Type": "application/json"
    }
    data = {
        "model": getattr(settings, 'OPENROUTER_MODEL', 'openai/gpt-3.5-turbo'),
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        return "ИИ не вернул ответ."
    except Exception as e:
        return f"Ошибка при обращении к ИИ-ассистенту: {str(e)}"
