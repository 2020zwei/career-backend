import openai
from django.conf import settings


openai.api_key = settings.OPENAI_API_KEY


def generate_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        prompt=prompt,
        model="gpt-4o-mini"
    )
    return response['choices'][0]['message']['content']
