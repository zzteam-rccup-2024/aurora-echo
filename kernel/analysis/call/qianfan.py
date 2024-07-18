from qianfan import ChatCompletion


def send_to_qianfan(prompt, model="ERNIE-4.0-8K"):
    chat_comp = ChatCompletion()
    resp = chat_comp.do(model=model, messages=prompt)
    print(resp["body"])
