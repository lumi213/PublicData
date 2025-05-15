import pandas as pd
from tqdm import tqdm
tqdm.pandas()

import numpy as np
import torch
import os
from sentence_transformers import SentenceTransformer

current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재파일이 있는 경로
data_dir = "C:/Project/Chatbot/data/test" # 데이터디렉토리 경로

#"""
train_file = os.path.join(data_dir, "train_data.xlsx")
model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

df = pd.read_excel(train_file)
df['embedding_vector'] = df['질문(Query)'].progress_map(lambda x : model.encode(x))
df.to_excel(os.path.join(data_dir, "train_data_embedding.xlsx"), index=False)

# embedding_data = torch.tensor(df['embedding_vector'].tolist())
# torch.save(embedding_data, os.path.join(data_dir, 'embedding_data.pt'))
embedding_array = np.array(df['embedding_vector'].tolist())
embedding_data = torch.tensor(embedding_array)
save_path = os.path.join(data_dir, 'embedding_data.pt')
os.makedirs(os.path.dirname(save_path), exist_ok=True)
torch.save(embedding_data, save_path)
#"""

class create_embedding_data:
    def __init__(self, preprocess, df):
        # 텍스트 전처리기
        self.p = preprocess

        # 질문 데이터프레임
        self.df = df

        # pre-trained SBERT
        self.model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

    def create_pt_file(self):
        # 질문 목록 리스트
        target_df = list(self.df['질문(Query)'])

        # 형태소 분석
        for i in range(len(target_df)):
            sentence = target_df[i]
            pos = self.p.pos(sentence)
            keywords = self.p.get_keywords(pos, without_tag=True)
            temp = ""
            for k in keywords:
                temp += str(k)
            target_df[i] = temp

        self.df['질문 전처리'] = target_df
        self.df['embedding_vector'] = self.df['질문 전처리'].progress_map(lambda x : self.model.encode(x))
        #embedding_data = torch.tensor(self.df['embedding_vector'].tolist())

        embedding_array = np.array(self.df['embedding_vector'].tolist())
        embedding_data = torch.tensor(embedding_array)
        torch.save(embedding_data, os.path.join(current_dir, 'embedding_data.pt'))
