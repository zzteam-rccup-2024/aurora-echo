from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from kernel.config import device
from config import data


class Llama:
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
        input_ids = self.tokenizer.apply_chat_template(
            prompt,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.device)

        terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]

        outputs = self.model.generate(
            input_ids,
            max_new_tokens=128,
            eos_token_id=terminators,
            do_sample=True,
            temperature=0.6,
            top_p=0.9,
        )
        response = outputs[0][input_ids.shape[-1]:]

        return self.tokenizer.decode(response, skip_special_tokens=True)
