import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import preprocessing
import pickle
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

# 의도 분류 모델 모듈
class IntentModel:
    def __init__(self, model_name, preprocess):
        # 학과명 레이블 매핑 정보 불러오기
        # JSON 파일 불러오기 
        with open(os.path.join(current_dir, 'index_to_label.json'), 'r',
                  encoding='utf-8') as f:
            labels = json.load(f)

        # 문자열로 된 숫자 키를 정수형으로 변환하여 self.labels에 저장
        self.labels = {int(k): v for k, v in labels.items()}
        print("레이블 매핑 정보 로드 완료:")

        # 의도 분류 모델 불러오기
        self.model = load_model(model_name)
        print("모델이 성공적으로 로드되었습니다.")

        # 전처리기 설정
        self.preprocess = preprocess

        # 토크나이저 불러오기
        with open(os.path.join(current_dir, 'tokenizer.pickle'), 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        print("토크나이저 로드 완료..")

    # 의도 클래스 예측
    def predict_class(self, query, max_len=100):
        try:
            # 형태소 분석 및 전처리
            pos = self.preprocess.pos(query)
            keywords = self.preprocess.get_keywords(pos, without_tag=True)
            sequences = self.tokenizer.texts_to_sequences([keywords])
            print(f"입력된 쿼리: {query}, 전처리 결과: {keywords}")

            # 패딩 처리
            padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=max_len, padding='post')

            # 예측 수행
            predict = self.model.predict(padded_seqs)
            predict_class = tf.math.argmax(predict, axis=1)
            return predict_class.numpy()[0]
        except Exception as e:
            print(f"예측 중 오류 발생: {e}")
            return "예측 오류"