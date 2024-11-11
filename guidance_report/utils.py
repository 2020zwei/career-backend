import openai
from django.conf import settings


openai.api_key = settings.OPENAI_API_KEY


def generate_gpt_response(prompt, max_tokens=100):
    response = openai.ChatCompletion.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        model="gpt-4o-mini",
		max_tokens=max_tokens
    )
    return response['choices'][0]['message']['content']
