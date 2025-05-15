import torch
import numpy as np
from numpy import dot
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer, util


class FindAnswer:
    def __init__(self, preprocess, df, embedding_data):
        # 챗봇 텍스트 전처리기
        self.p = preprocess

        # pre-trained SBERT
        self.model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

        # 질문 데이터프레임
        self.df = df

        # embedding_data
        self.embedding_data = embedding_data

    def search(self, query, intent):
        # 형태소 분석
        pos = self.p.pos(query)

        # 불용어 제거
        keywords = self.p.get_keywords(pos, without_tag=True)
        query_pre = "".join(keywords)

        # 전처리된 질문 인코딩 및 텐서화
        query_encode = self.model.encode(query_pre)
        query_tensor = torch.tensor(query_encode)

        # 코사인 유사도를 통해 질문 데이터 선택
        cos_sim = util.cos_sim(query_tensor, self.embedding_data)
        best_sim_idx = int(np.argmax(cos_sim))

        # 선택된 질문과 그 의도
        selected_qes = self.df['질문(Query)'][best_sim_idx]
        query_intent = self.df['의도(Intent)'][best_sim_idx]

        # 의도가 일치하면 유사도를 따지지 않고 바로 답변 제공
        if query_intent == intent:
            # 답변을 바로 출력
            answer = self.df['답변(Answer)'][best_sim_idx]
            score = 1.0  # 의도가 맞으면 점수는 최대
            print(f"의도 일치: {intent} == {query_intent}")
        else:
            # 의도가 맞지 않으면 기존 방식으로 질문 유사도 기반 처리
            print(f"의도 불일치: {intent} != {query_intent}")
            score = dot(query_tensor, self.embedding_data[best_sim_idx]) / (
                norm(query_tensor) * norm(self.embedding_data[best_sim_idx])
            )
            answer = "잘 이해하지 못했어요 😓 조금 더 자세하게 말씀해주세요 :)"

        return selected_qes, score, answer, query_intent