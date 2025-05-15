import pandas as pd

# 엑셀 파일 경로
상병코드_file_path = '고용노동부_산재요양신청서 상병코드(1)_20220920.csv'
업종별산재승인_file_path = '근로복지공단_업종별 산재신청 승인현황_20231231.csv'

# train_data.xlsx : 의도(Intent), 질문(Query), 답변(Answer), 답변 이미지
# train_data.csv  : text(질의), label(의도)

# 의도 [상병코드_조회, 산재승인율_조회]
# train_data.xlsx
# 상병코드, S320(요추의골절), 요추의골절(S320), 
# 업종별산재승인, 금융 및 보험업, 2023년에 924건중 794건이 승인되어 약85.9%의 산재신청이 승인되었습니다.,

# 엑셀 파일을 DataFrame으로 읽기 (첫 번째 시트 기준)
# df = pd.read_excel(excel_file_path)

df = pd.read_csv(csv_file_path)

# CSV 파일로 저장
df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')  # 한글 포함 시 utf-8-sig 권장

# 엑셀로 저장
df.to_excel(excel_file_path, index=False)