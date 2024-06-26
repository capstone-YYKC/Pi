import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration


tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')


def summarization(text):
    raw_input_ids = tokenizer.encode(text)
    input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]

    summary_ids = model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=512,  eos_token_id=1)
    summary_text = tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)


    print(f"summary_text: {summary_text}")
    return summary_text
