import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from tqdm import tqdm, tqdm_notebook
import pandas as pd

from kobert_tokenizer import KoBERTTokenizer
from transformers import BertModel, BertTokenizer

from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup
import warnings
warnings.filterwarnings('ignore')

import os, sys; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from username import username

import re


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

max_len = 64
batch_size = 64

class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len, pad, pair):
        self.sentences = [
            bert_tokenizer(
                i[sent_idx],
                add_special_tokens=True,
                max_length=max_len,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            ) for i in dataset
        ]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        data = self.sentences[i]
        input_ids = data['input_ids'].squeeze(0)
        attention_mask = data['attention_mask'].squeeze(0)
        token_type_ids = data['token_type_ids'].squeeze(0)
        return input_ids, attention_mask, token_type_ids, self.labels[i]

    def __len__(self):
        return len(self.labels)

class BERTClassifier(nn.Module):
    def __init__(self, bert, hidden_size=768, num_classes=4, dr_rate=None, params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.classifier = nn.Linear(hidden_size, num_classes)
        self.dr_rate = dr_rate 
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)

    def forward(self, input_ids, attention_mask, token_type_ids):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        pooler = outputs.pooler_output
        if self.dr_rate:
            pooler = self.dropout(pooler)
        return self.classifier(pooler)

# 사용할 토크나이저 및 모델 로드
tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
bertmodel = BertModel.from_pretrained('skt/kobert-base-v1', return_dict=True)

# 모델 생성 및 사전 학습된 가중치 로드
model = BERTClassifier(bertmodel, dr_rate=0.5).to(device)
model.load_state_dict(torch.load(f'/home/{username}/yykc/bert/trained_model222.pt', map_location=device))

# # 예측 함수 정의
# def predict(predict_sentence):
#     data = [predict_sentence, '0']
#     dataset_another = [data]
#     another_test = BERTDataset(dataset_another, 0, 1, tokenizer, max_len, True, False)
#     test_dataloader = DataLoader(another_test, batch_size=batch_size, num_workers=0)

#     model.eval()
#     with torch.no_grad():
#         for batch_id, (input_ids, attention_mask, token_type_ids, label) in enumerate(test_dataloader):
#             input_ids = input_ids.to(device)
#             attention_mask = attention_mask.to(device)
#             token_type_ids = token_type_ids.to(device)

#             out = model(input_ids, attention_mask, token_type_ids)
#             logits = out.detach().cpu().numpy()[0]

#             probabilities = np.exp(logits) / np.sum(np.exp(logits))
#             print("감정 예측 값")
#             for i, prob in enumerate(probabilities):
#               if i==0:
#                 print(f"행복: {prob:.4f}")
#               elif i==1:
#                 print(f"보통: {prob:.4f}")
#               elif i==2:
#                 print(f"화남: {prob:.4f}")
#               elif i==3:
#                 print(f"슬픔: {prob:.4f}")

#             return {
#                 "행복": probabilities[0],
#                 "보통": probabilities[1],
#                 "화남": probabilities[2],
#                 "슬픔": probabilities[3]
#             }


# 단일 문장에 대해 예측을 수행하는 함수
def predict_single_sentence(sentence):
    data = [sentence, '0']
    dataset_another = [data]
    another_test = BERTDataset(dataset_another, 0, 1, tokenizer, max_len, True, False)
    test_dataloader = DataLoader(another_test, batch_size=batch_size, num_workers=0)

    model.eval()
    with torch.no_grad():
        for batch_id, (input_ids, attention_mask, token_type_ids, label) in enumerate(test_dataloader):
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            token_type_ids = token_type_ids.to(device)

            out = model(input_ids, attention_mask, token_type_ids)
            logits = out.detach().cpu().numpy()[0]

            probabilities = np.exp(logits) / np.sum(np.exp(logits))
            emotions = ["행복", "보통", "화남", "슬픔"]
            max_index = np.argmax(probabilities)
            return emotions[max_index]

# 여러 문장에 대해 예측을 수행하는 함수
def predict(predict_sentence):
    # 문장을 '.', '?', '!'로 분할
    sentences = re.split(r'[.?!]', predict_sentence)
    
    # 빈 문장 제거
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    # 감정 빈도수 저장
    emotion_counts = {
        "행복": 0,
        "보통": 0,
        "화남": 0,
        "슬픔": 0
    }

    for sentence in sentences:
        result = predict_single_sentence(sentence)
        emotion_counts[result] += 1

    # 감정 빈도수 출력
    print("감정 예측 빈도수")
    for emotion, count in emotion_counts.items():
        print(f"{emotion}: {count}")

    return emotion_counts



# 감정 점수 계산 함수
def calculate_emotion_score(emotion_counts):
    # 전체 문장의 수
    total_sentences = sum(emotion_counts.values())

    # 감정별 가중치
    weights = {
        "행복": 100,
        "보통": 50,
        "화남": 25,
        "슬픔": 0
    }

    # 점수 계산
    score = 0
    for emotion, count in emotion_counts.items():
        score += (count / total_sentences) * weights[emotion]

    return score
