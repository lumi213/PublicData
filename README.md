# Chatbot Framework
챗봇 프레임워크

## 📖 목차
- [소개](#소개)
- [기능](#기능)
- [설치 방법](#설치방법)
- [사용법](#사용법)
- [폴더 구조](#폴더구조)
- [데이터 파일](#데이터파일일)
- [라이선스](#라이선스)

## 🧾 소개
chatbot, flask 2개의 서버로 구성되었습니다.

## 기능
간단한 버튼식 질의 - 링크
의도 분류 모델을 사용한 의도 분석

## 💾 설치방법
```bash
# 1. 저장소 클론

# 2-1. 가상환경 (env-flask, env-server) 생성 (선택)
py -3.11 -m venv env-flask
py -3.11 -m venv env-server

# 2-2. 가상환경 실행
.\env-flask\Scripts\activate.bat
.\env-server\Scripts\activate.bat

# 3. 필수 패키지 설치
python.exe -m pip install --upgrade pip
python.exe -m pip install -r requirements.txt

# 4. npm패키지 설치 (1flask에서)
npm install
```
# 실행시 패키지 오류발생시 requirements.txt의 주석을 참고해 패키지 재설치

## 사용법
1. 각 chatbot `./0server/chatbot.py`, flask `./1flask/application.py` 서버를 실행
2. http://localhost:5001 접속

## 폴더구조
# server `/0server`

# flask `/1flask`

## 데이터파일
# server
텍스트 전처리기 `utils/Preprocess.py`
1. 단어 사전 : `train_tools/dict/chatbot_dict.bin` 수정불요

의도 파악 모델 `models/intent/IntentModel.py` `train_intent.py`에서 `train_data.csv`요구
2. 레이블 매핑 정보 : `models/intent/index_to_label.json`
3. 모델 : `models/intent/intent_model.h5`
4. 토크나이저 : `models/intent/tokenizer.pickle`

`chatbot.py`
5. 엑셀 파일 : `train_tools/qna/train_data.xlsx`
6. 임베딩 pt 파일 : `train_tools/qna/embedding_data.pt` `create_embedding_data.py`에서 `train_data.xlsx`요구

# flask
랜덤 가게추첨 `utils/Button_handler.py`
1. 가게 리스트 : `utils/business_info.xlsx`

# IIS
cgi 설치

## 라이선스
# MIT License
`./License` 참조





# 기존 README.md 내용
# Chatbot4Univ
프로젝트 소개 티스토리 블로그 글 [[바로가기](https://seokii.tistory.com/146)]  
블로그 게시물을 통해 누구나 구현을 쉽게 따라할 수 있도록 모든 작업에 대한 글 작성을 진행했습니다.  
프로젝트 소개 게시물에 작성한 포스팅 목록이 있습니다.  

## About Project
대학교 AI 질의응답 챗봇 서비스 개발은  
스마트 캠퍼스 플랫폼이라는 학부생 졸업 작품 프로젝트에서  
AI 서비스를 1인 기획 및 개발한 프로젝트입니다.  

## Project Task
- 데이터 수집 및 가공
- 의도 분류 모델 학습
- 질의 응답 내용 작성과 임베딩후 pt파일로 저장
- 사용자의 질문과 구축된 질문 리스트의 유사도 비교
- 챗봇 소켓 서버 구현
- 챗봇 API 서버 구현
- 추가적으로 개선하기

## Result
다음과 같이 챗봇 소켓, API 서버를 구현하고  
Flutter로 구현한 어플리케이션에서 챗봇 서비스를 시연했습니다.  
<br>
<img src="https://user-images.githubusercontent.com/80209977/202237639-0a833634-c688-4243-b2e3-a948c603aa77.png" width="850" height="500"/>
