import calendar
import locale
from datetime import date

from app.openai_integration import chat_gpt

PROMT_DESTINATIONS = """
Du der persönliche Reiseberater deiner Kunden. Antworte nur zu reisespezifischen Themen, zu andere Themen gibst du keine Antwort. 
Antworte nur auf Deutsch. Schlage dem Nutzer bei jeder Frage eines der Folgenden Reiseziele vor: Mallorca, New York, Sydney. 
"""

# Antwort muss immer im JSON Format zurückgegeben werden. Der Key "recommendation" soll dabei deine klare Begründung sein und das konkrete Reiseziel mit dem key "destination" zurück.
# GEBE IMMER JSON ZURÜCK, wenn der Nutzer nicht nach reisespezifischen Fragt, soll in "recommendation" die Fehlermeldung und in "destination" null sein.


PROMT_DESTINATION_DESCRIPTION = """
Du gibst postive Infotexte wieder über Reisezeile. 
"""


def gpt_destination_search(user_promt: str) -> str:
	return chat_gpt(user_promt, train_data=PROMT_DESTINATIONS)


def gpt_destination_description(destination: str, outbounddeparturedatetime: date,
								inboundarrivaldatetime: date, count_adults: int, count_children: int) -> str:

	month_outbounddeparturedatetime: str = get_month_name(outbounddeparturedatetime.month)
	month_inboundarrivaldatetime: str = get_month_name(inboundarrivaldatetime.month)


	promt_for_destination: str = f"{destination} im"

	if month_outbounddeparturedatetime == month_outbounddeparturedatetime:
		promt_for_destination = f"{promt_for_destination} {month_inboundarrivaldatetime}"
	else:
		promt_for_destination = f"{promt_for_destination} {month_inboundarrivaldatetime / month_inboundarrivaldatetime}"

	promt_for_destination = f"{promt_for_destination} ({count_adults} Erwachsene und {count_children} Kinder)"
	return chat_gpt(promt_for_destination, train_data=PROMT_DESTINATION_DESCRIPTION)


def get_month_name(month: int) -> str:
	#Not using locale, because it's not insured that this local is installed
	#locale.setlocale(locale.LC_TIME, 'de_DE')
	#return calendar.month_name[month]

	month_name = {
		1: 'Januar',
		2: 'Februar',
		3: 'März',
		4: 'April',
		5: 'Mai',
		6: 'Juni',
		7: 'Juli',
		8: 'August',
		9: 'September',
		10: 'Oktober',
		11: 'November',
		12: 'Dezember'
	}
	return month_name.get(month)



if __name__ == '__main__':
	print(gpt_destination_description("Mallorca", date(2023, 6, 22), date(2023, 6, 22), 2, 0))
	print(gpt_destination_search("Ich will an den Starnd"))
