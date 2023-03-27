import openai
import tiktoken
from typing import Tuple

class GPT_API():

    def __init__(self, organization: str, api_key: str):
        openai.organization = organization
        openai.api_key = api_key
    
    def get_responce(self, prompt: str) -> Tuple[int, str]:
        try:
            sending_messages=[{"role": "system", "content": "You are qute speaking dog-assistant"},
                              {"role": "user", "content": prompt}]
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                      messages=sending_messages)
            num_tokens: int = completion.usage.prompt_tokens
            responce: str = completion.choices[0].message['content'].strip()
            return num_tokens, responce
        except Exception as e:
            print(e)
            
    def get_num_tokens_for_sending(self, messages, model="gpt-3.5-turbo-0301"):
        """Returns the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
            num_tokens = 0
            for message in messages:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
            See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")