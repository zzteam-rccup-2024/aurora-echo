import gc
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from kernel.config import device

if device == torch.device('mps'):
    device = torch.device('cpu')
    # Qwen-2-1.5B doesn't support MPS

model_name = "Qwen/Qwen2-1.5B-Instruct"


def send_to_qwen_offline(prompt):
    model = AutoModelForCausalLM.from_pretrained(
        f"data/models/{model_name}",
        torch_dtype="auto",
        device_map=device
    )
    tokenizer = AutoTokenizer.from_pretrained(f"data/models/{model_name}")

    text = tokenizer.apply_chat_template(
        prompt,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    del model
    del tokenizer
    gc.collect()

    return response
