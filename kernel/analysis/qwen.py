import gc
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from kernel.config import device
from config import data


class Qwen:
    def __init__(self):
        self.model_id = f"{data['llama']['path']}/{data['llama']['model']}"
        self.device = device if device != torch.device('mps') else torch.device('cpu')

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            torch_dtype=torch.bfloat16,
            device_map=self.device,
        )

    def message(self, prompt):
        text = self.tokenizer.apply_chat_template(
            prompt,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt")

        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return response
