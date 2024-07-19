from qianfan import ChatCompletion


def send_to_llama_online(prompt, model="Meta-Llama-3-70B"):
    chat_comp = ChatCompletion()
    if len(prompt) == 2:
        prompt = [{'role': 'user', 'content': "".join([item['content'] for item in prompt])}]
    resp = chat_comp.do(model=model, messages=prompt)
    return resp["body"]['result']
