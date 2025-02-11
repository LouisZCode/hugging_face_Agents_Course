import os
from huggingface_hub import InferenceClient

#Permits to use an open LLM, to check later how to get my local or Claude in this:
HF_TOKEN = os.environ.get("HF_TOKEN")
client = InferenceClient("meta-llama/Llama-3.2-3B-Instruct")


my_prompt = "what version are you?"
prompt=f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>{my_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

output = client.text_generation(
    prompt,
    max_new_tokens=100,
)

print(output)
