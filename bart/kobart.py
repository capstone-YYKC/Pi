import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration

tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

file_path = '/home/test01/yykc/bart/diary.txt'

with open(file_path, 'r', encoding='utf8') as file:
    text = file.read()


def summarization(text):
    raw_input_ids = tokenizer.encode(text)
    input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]

    summary_ids = model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=512,  eos_token_id=1)
    summary_text = tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)

    # file_path = '/home/test01/yykc/bart/summarize.txt'

    # with open(file_path,'w',encoding='utf8') as file:
    #     file.write(summary_text)

    print(f"summary_text: {summary_text}")
    return summary_text
