from fastapi import APIRouter
from openai import OpenAI

router = APIRouter()


def load_api_key():
    try:
        with open("api_key.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise Exception("Die Datei 'api_key.txt' wurde nicht gefunden.")


api_key = load_api_key()
client = OpenAI(api_key=api_key)


@router.post("/generate_funny_response/")
def generate_funny_response(event_text: str):
    prompt = "Erstelle witzige Titel für diese Termin: " f"{event_text}"
    try:
        response = client.chat.completions.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )
        return {"response": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"error": f"Fehler bei der OpenAI-Anfrage: {e}"}
