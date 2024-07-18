from transformers import T5Tokenizer, T5ForConditionalGeneration
from kernel.config import device

model_name = "google/flan-t5-xl"


def send_to_flan_t5_offline(prompt):
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name, device_map=device)

    input_ids = tokenizer("\n".join([item for user, item in prompt]), return_tensors="pt").input_ids.to(device)
    outputs = model.generate(input_ids, max_length=256)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
