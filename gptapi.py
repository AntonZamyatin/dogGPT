import openai

class GPT_API():

    def __init__(self, organization: str, api_key: str):
        openai.organization = organization
        openai.api_key = api_key
        
    def get_responce(self, prompt: str) -> str:
        print('asking: ', prompt)
        try:
            completion = openai.ChatCompletion.create(
                         model="gpt-3.5-turbo",
                         messages=[
                         {"role": "system", "content": "You are Karl Dogs the reincarnation of the Karl Marx in dog body. You are russian speaking and always want to emphasize the importance of fight with private property on means of production"},
                         {"role": "user", "content": prompt}]
                         )
            return completion.choices[0].message['content'].strip()
        except Exception as e:
            print(e)