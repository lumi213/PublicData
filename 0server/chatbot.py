import threading
import json
import pandas as pd
import tensorflow as tf
import torch
import os

from utils.BotServer import BotServer
from utils.Preprocess import Preprocess
from utils.FindAnswer import FindAnswer
from models.intent.IntentModel import IntentModel
from train_tools.qna.create_embedding_data import create_embedding_data

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' #0:모든 로그, 1:정보성 로그 무시, 2:경고 로그 무시(1포함), 3에러 로그 무시(2포함)
current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재파일이 있는 경로

# tensorflow gpu 메모리 할당 설정
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
        tf.config.experimental.set_virtual_device_configuration(gpus[0],
                        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2048)])
    except RuntimeError as e:
        print(e)

# 로그 기능 구현
from logging import handlers
import logging

# log settings
LogFormatter = logging.Formatter('%(asctime)s,%(message)s')

# handler settings
LogHandler = handlers.TimedRotatingFileHandler(
    filename=os.path.join(current_dir, 'logs/chatbot.log'), when='midnight', interval=1, encoding='utf-8')
LogHandler.setFormatter(LogFormatter)
LogHandler.suffix = "%Y%m%d"

# logger set
Logger = logging.getLogger()
Logger.setLevel(logging.ERROR)
Logger.addHandler(LogHandler)

# 전처리 객체 생성
try:
    p = Preprocess(word2index_dic=os.path.join(current_dir, 'train_tools/dict/chatbot_dict.bin'))
    print("텍스트 전처리기 로드 완료..")
except Exception as e:
    print(f"텍스트 전처리기 로드 실패.. {e}")

# 의도 파악 및 비속어 필터링 모델 초기화
try:
    intent = IntentModel(model_name=os.path.join(current_dir, "models/intent/intent_model.h5"), preprocess=p)
    print("의도 파악 모델 로드 완료..")
except Exception as e:
    print(f"의도 파악 모델 로드 실패: {e}")

# 엑셀 파일 로드
try:
    df = pd.read_excel(os.path.join(current_dir, 'train_tools/qna/train_data.xlsx'))
    print("엑셀 파일 로드 완료..")
except:
    print("엑셀 파일 로드 실패..")

# pt 파일 갱신 및 불러오기
try:
    create_embedding_data = create_embedding_data(df=df, preprocess=p)
    create_embedding_data.create_pt_file()
    embedding_data = torch.load(os.path.join(current_dir, 'train_tools/qna/embedding_data.pt'))
    print("임베딩 pt 파일 갱신 및 로드 완료..")
except Exception as e:
    print(f"임베딩 pt 파일 갱신 및 로드 실패.. {e}")
    print(current_dir)


def preprocess_user_input(query):
    query = query.lower()  # 소문자로 변환

    # 각 의도에 대한 전처리 규칙 추가
    if '식단' in query:
        return '식단안내'
    elif '연락처' in query or '학과 연락처' in query:
        return '교내연락처'
    elif '일정' in query or '학사 일정' in query:
        return '학사일정'
    elif '캠퍼스 맵' in query or '캠퍼스 지도' in query:
        return '캠퍼스맵'
    elif '등록금' in query or '등록 안내' in query:
        return '등록안내'
    elif '장학금' in query or '장학 안내' in query:
        return '장학안내'
    elif '통학 버스' in query or '통학' in query or '셔틀' in query or '버스' in query:
        return '통학버스'
    elif '수강 신청' in query or '강의' in query:
        return '수강신청'
    elif '상권' in query or '상권 안내' in query or '맛집' in query:
        return '상권안내'

    return query  # 기본적으로 원본 쿼리 반환


def to_client(conn, addr):
    try:
        # 데이터 수신
        read = conn.recv(2048)  # 수신 데이터가 있을 때까지 블로킹
        print('======================')
        print('Connection from: %s' % str(addr))

        if read is None or not read:
            print('클라이언트 연결 끊어짐')
            exit(0)  # 스레드 강제 종료

        # json 데이터로 변환
        recv_json_data = json.loads(read.decode())
        print("데이터 수신 : ", recv_json_data)
        query = recv_json_data['Query']

        # 사용자 입력 전처리
        processed_query = preprocess_user_input(query)  # 표준화된 쿼리

        # 의도 파악
        intent_pred = intent.predict_class(processed_query)
        intent_name = intent.labels[intent_pred]

        # 의도에 따른 응답 처리
        if intent_name == '교내연락처':
            answer = "교내연락처"
        elif intent_name == '학사일정':
            answer = "학사일정"
        elif intent_name == '캠퍼스맵':
            answer = "캠퍼스맵"
        elif intent_name == '식단안내':
            answer = "식단안내"
        elif intent_name == '등록안내':
            answer = "등록안내"
        elif intent_name == '장학안내':
            answer = "장학안내"
        elif intent_name == '통학버스':
            answer = "통학버스"
        elif intent_name == '수강신청':
            answer = "수강신청"
        elif intent_name == '상권안내':
            answer = "상권안내"
        else:
            # 답변 검색
            f = FindAnswer(df=df, embedding_data=embedding_data, preprocess=p)
            selected_qes, score, answer, query_intent = f.search(query, intent_name)  # 원본 쿼리 사용

            if score < 0.7:
                answer = "❗부정확한 질문이거나 답변할 수 없습니다.❗️\n 수일 내로 답변을 업데이트하겠습니다.\n 죄송합니다 :("
                Logger.error(f"{query},{intent_name},{selected_qes},{query_intent},{score}")

        send_json_data_str = {
            "Query": selected_qes if 'selected_qes' in locals() else query,
            "Answer": answer,
            "Score": float(score) if 'score' in locals() else 1.0,  # 기본 score 설정
            "Intent": intent_name
        }
        message = json.dumps(send_json_data_str)  # json객체 문자열로 반환
        conn.send(message.encode())  # 응답 전송
        print("응답 전송됨: ", message)

    except Exception as ex:
        print(ex)



if __name__ == '__main__':
    # 봇 서버 동작
    port = 5050
    listen = 1000
    bot = BotServer(port, listen)
    bot.create_sock()
    print("bot start..")

    while True:
        conn, addr = bot.ready_for_client()
        client = threading.Thread(target=to_client, args=(
            conn,   # 클라이언트 연결 소켓
            addr,   # 클라이언트 연결 주소 정보
        ))
        client.start()