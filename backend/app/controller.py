from app.openai_integration import search_for_destination


def ai_search(query: str):
    return search_for_destination(query)
