import os
from fastapi import APIRouter

from openai import OpenAI

router = APIRouter()


def load_api_key():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "api_key.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise Exception("Die Datei 'api_key.txt' wurde nicht gefunden.")


def get_openai_client():
    api_key = load_api_key()
    return OpenAI(api_key=api_key)


@router.post("/generate_funny_response/")
def generate_funny_response(event_text: str):
    prompt = (
        f'Erstelle einen lustigen Titel für: "{event_text}". '
        "Maximal 10 Wörter, übertrieben & spaßig."
    )
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        return {"result": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"error": f"Fehler bei der Anfrage an OpenAI: {str(e)}"}
