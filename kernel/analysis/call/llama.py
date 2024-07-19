from qianfan import ChatCompletion


def send_to_llama_online(prompt, model="Meta-Llama-3-70B"):
    chat_comp = ChatCompletion()
    resp = chat_comp.do(model=model, messages=prompt)
    print(resp["body"]['result'])
