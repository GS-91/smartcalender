from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
import os

router = APIRouter()


def load_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY not set.")
    return api_key


class EventInput(BaseModel):
    event_text: str


@router.post("/generate_funny_response/")
def generate_funny_response(event: EventInput):
    prompt = (
        "Erstelle witzige Titel für diesen Termin: "
        f"{event.event_text}"
    )
    try:
        client = OpenAI(api_key=load_api_key())
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        return {"response": response.choices[0].message.content.strip()}
    except Exception as e:
        return {"error": f"Fehler bei der OpenAI-Anfrage: {e}"}
