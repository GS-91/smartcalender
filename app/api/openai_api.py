from fastapi import APIRouter
from openai import OpenAI
import os

router = APIRouter()

# OpenAI-API-Schlüssel aus Datei laden
def load_api_key():
    try:
        with open("api_key.txt", "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise Exception("Die Datei 'api_key.txt' wurde nicht gefunden. Bitte füge dort deinen API-Schlüssel ein.")

api_key = load_api_key()

# OpenAI-Client initialisieren
client = OpenAI(api_key=api_key)

@router.post("/generate_funny_response/")
def generate_funny_response(event_text: str):
    """
    Generiert eine humorvolle Antwort zu einem Kalendereintrag.
    
    - `event_text`: Beschreibung des Kalendereintrags (z. B. "Meeting mit Chef um 10 Uhr").
    """
    prompt = f"Erstelle eine humorvolle, witzige und freche Antwort für diesen Termin: {event_text}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        funny_response = response.choices[0].message.content.strip()
        return {"response": funny_response}
    except Exception as e:
        return {"error": f"Fehler bei der OpenAI-Anfrage: {e}"}
