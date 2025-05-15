from konlpy.tag import Komoran
import pickle
from tensorflow.keras import preprocessing
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

class Preprocess:
    def __init__(self, word2index_dic=os.path.join(current_dir, '../train_tools/dict/chatbot_dict.bin')):
        # 단어 인덱스 사전 불러오기
        if word2index_dic != '':
            with open(word2index_dic, "rb") as f:
                self.word_index = pickle.load(f)
                print("단어 사전 로드 완료..")
        else:
            self.word_index = None
            print("단어 사전 로드 실패..")

        # Komoran 형태소 분석기 초기화
        self.komoran = Komoran()

        # 제외할 품사 목록 설정
        self.exclusion_tags = [
            'JKS', 'JKC', 'JKG', 'JKO', 'JKB', 'JKV', 'JKQ',
            'JX', 'JC', 'SF', 'SP', 'SS', 'SE', 'SO',
            'EP', 'EF', 'EC', 'ETN', 'ETM', 'XSN', 'XSV', 'XSA'
        ]

    # 형태소 분석기 POS 태거
    def pos(self, sentence):
        return self.komoran.pos(sentence)

    # 불용어 제거 후 필요한 품사 정보만 가져오기
    def get_keywords(self, pos, without_tag=False):
        word_list = [word for word, tag in pos if tag not in self.exclusion_tags]
        return word_list if without_tag else [(word, tag) for word, tag in pos if tag not in self.exclusion_tags]

    # 키워드를 단어 인덱스 시퀀스로 변환
    def get_wordidx_sequence(self, keywords):
        if self.word_index is None:
            return []
        return [self.word_index.get(word, self.word_index.get('OOV', 0)) for word in keywords]

    # 문장을 토크나이저로 시퀀스로 변환
    def preprocess_text(self, text, tokenizer, max_len):
        pos = self.pos(text)
        keywords = self.get_keywords(pos, without_tag=True)
        sequence = tokenizer.texts_to_sequences([keywords])
        padded_sequence = preprocessing.sequence.pad_sequences(sequence, maxlen=max_len, padding='post')
        return padded_sequence