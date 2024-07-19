from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from kernel.config import device

model_id = "data/models/meta-llama/Meta-Llama-3-8B-Instruct"

if device == torch.device('mps'):
    device = torch.device('cpu')
    # Llama-3-8B-Instruct doesn't support MPS


def send_to_llama_offline(prompt):
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.bfloat16,
        device_map=device,
    )

    input_ids = tokenizer.apply_chat_template(
        prompt,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(device)

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=128,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )
    response = outputs[0][input_ids.shape[-1]:]

    return tokenizer.decode(response, skip_special_tokens=True)

