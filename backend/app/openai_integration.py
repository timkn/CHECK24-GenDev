import openai
import os

openai.api_key = os.environ['OPENAI_KEY']

SYSTEM_PROMT = """
Du der persönliche Reiseberater deiner Kunden. Antworte nur zu reisespezifischen Themen, zu andere Themen gibst du keine Antwort. 
Antworte nur auf Deutsch. Schlage dem Nutzer bei jeder Frage eines der Folgenden Reiseziele vor: Mallorca, New York, Sydney. 
"""
# Antwort muss immer im JSON Format zurückgegeben werden. Der Key "recommendation" soll dabei deine klare Begründung sein und das konkrete Reiseziel mit dem key "destination" zurück.
# GEBE IMMER JSON ZURÜCK, wenn der Nutzer nicht nach reisespezifischen Fragt, soll in "recommendation" die Fehlermeldung und in "destination" null sein.


def search_for_destination(query: str):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"{SYSTEM_PROMT}"},
                {"role": "user", "content": f"{query}"},
            ]
        )

    except Exception:
        return None

    return completion.choices[0].message.content
