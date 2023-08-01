import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']


def chat_gpt(input, train_data="") -> str:
	completion = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{"role": "system", "content": train_data},
			{"role": "user", "content": input}
		]
	)
	output: str = completion.choices[0].message.content
	return output
