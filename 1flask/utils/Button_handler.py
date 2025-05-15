from flask import Blueprint, request, jsonify

button_blueprint = Blueprint('buttons', __name__)

# 버튼 풀 (index 기반)
button_pool = [
    # 하위 버튼
    {"text": "서류 목록 보기", "url": "#"},
    {"text": "신청서 다운로드", "url": "#"},
    {"text": "제출처 알아보기", "url": "#"},
    {"text": "요양급여", "url": "#"},
    {"text": "휴업급여", "url": "#"},
    {"text": "장해급여", "url": "#"},
    {"text": "간병급여", "url": "#"},
    {"text": "장해등급표 보기", "url": "#"},
    {"text": "장해등급 판정 기준", "url": "#"},
    {"text": "장해급여 금액 안내", "url": "#"},
    # 외부 링크
    {"text": "근로복지공단 지사 찾기", "url": "#"}, # 10
    {"text": "요양급여 신청 바로가기", "url": "#"},
    {"text": "휴업급여 신청 바로가기", "url": "#"},
    {"text": "장해급여 신청 바로가기", "url": "#"},
    {"text": "간병급여 신청 바로가기", "url": "#"},
    {"text": "장해등급 기준표 보기", "url": "#"},
    # 파일
    {"text": "장해급여 금액 안내", "url": "#"}, # 16
    {"text": "장해급여 금액 안내", "url": "#"},
    {"text": "장해급여 금액 안내", "url": "#"},
    {"text": "장해급여 금액 안내", "url": "#"}
]

def get_buttons_by_index(indexes):
    return [button_pool[i] for i in indexes if 0 <= i < len(button_pool)]

@button_blueprint.route('/handle-button-click', methods=['POST'])
def handle_button_click():
    data = request.json
    button_title = data.get('buttonTitle')

    response_message = "❗ 해당 기능은 준비 중입니다."
    buttons = []

    # 상위 버튼
    if button_title == "질병 코드 안내":
        response_message = "🩺 질병명을 입력해 주세요.\n관련 질병 코드와 산재 승인 여부를 안내해드릴게요."

    elif button_title == "산재 신청 절차":
        response_message = ("🧾 산재 신청 절차는 다음과 같습니다:\n\n"
                            "1️⃣ 재해 발생\n"
                            "2️⃣ 병원 진료 및 진단서 발급\n"
                            "3️⃣ 요양급여 신청서 등 서류 준비\n"
                            "4️⃣ 근로복지공단에 제출")
        buttons = get_buttons_by_index([0, 1, 2])

    elif button_title == "보상금 종류 안내":
        response_message = "💰 어떤 보상 항목에 대해 알고 싶으신가요?"
        buttons = get_buttons_by_index([3, 4, 5, 6])

    elif button_title == "장해등급 기준":
        response_message = "📋 확인하고 싶은 항목을 선택해 주세요."
        buttons = get_buttons_by_index([7, 8, 9])

    elif button_title == "자주 묻는 질문":
        response_message = ("❓ 자주 묻는 질문입니다:\n"
                            "• 요양급여 신청은 어떻게 하나요?\n"
                            "• 산재 처리는 얼마나 걸리나요?\n"
                            "• 장해등급은 어떻게 결정되나요?\n"
                            "더 궁금하신 점은 자유롭게 입력해 주세요.")

    # 하위 버튼
    elif button_title == "서류 목록 보기":
        response_message = ("📄 제출해야 할 서류는 다음과 같습니다:\n\n"
                            "✅ 요양급여신청서\n✅ 진단서 또는 소견서\n✅ 사업주 확인서 또는 미제출 사유서\n"
                            "✅ 근무 확인서\n✅ 재해경위서")
        buttons = get_buttons_by_index([1, 2])

    elif button_title == "신청서 다운로드":
        response_message = ("📎 신청서 다운로드 링크입니다:\n\n"
                            f"<a href='/static/file/산업재해보상보험_요양급여신청서.hwp' download>📄 요양급여 신청서</a><br>"
                            f"<a href='/static/file/재해경위서.hwp' download>📄 재해경위서</a><br>"
                            f"<a href='/static/file/사업주확인서.hwp' download>📄 사업주확인서</a>")

    elif button_title == "제출처 알아보기":
        response_message = ("📬 서류는 가까운 근로복지공단 지사에 방문 또는 온라인 제출이 가능합니다.<br>"
                            "<a href='https://www.comwel.or.kr/comwel/intr/srch/srch.jsp' target='_blank'>👉 지사 찾기</a>")

    elif button_title == "요양급여":
        response_message = ("📌 요양급여 안내\n업무상 재해로 치료가 필요한 경우 치료비 등을 지원하는 급여입니다.\n\n"
                            "▶ 신청 조건: 산재로 인정된 부상 또는 질병\n"
                            "▶ 신청 시기: 치료가 필요한 즉시\n"
                            "▶ 제출 서류: 요양급여신청서, 진단서, 사업주 확인서 등\n"
                            "▶ 제출처: 근로복지공단 지사 또는 온라인<br/>"
                            "<a href='https://www.gov.kr/mw/AA020InfoCappView.do?HighCtgCD=A05007&CappBizCD=14900000261&tp_seq=' target='_blank' class='text-blue-600 underline'>👉 신청 바로가기</a>")

    elif button_title == "휴업급여":
        response_message = ("📌 휴업급여 안내\n치료로 인해 일을 하지 못한 기간 동안 지급되는 급여입니다.\n\n"
                            "▶ 신청 조건: 요양으로 인해 근로하지 못한 기간\n"
                            "▶ 신청 시기: 요양 시작일로부터 3일 초과 시\n"
                            "▶ 제출 서류: 휴업급여신청서, 진단서 등\n"
                            "▶ 제출처: 근로복지공단 지사 또는 온라인<br/>"
                            "<a href='https://www.gov.kr/mw/AA020InfoCappView.do?CappBizCD=14900000265' target='_blank' class='text-blue-600 underline'>👉 신청 바로가기</a>")

    elif button_title == "장해급여":
        response_message = ("📌 장해급여 안내\n치료 종료 후에도 장해가 남는 경우 지급되는 급여입니다.\n\n"
                            "▶ 신청 조건: 장해등급이 인정되는 경우\n"
                            "▶ 신청 시기: 요양 종료 후 장해 판정 시\n"
                            "▶ 제출 서류: 장해급여신청서, 장해진단서 등\n"
                            "▶ 제출처: 근로복지공단<br/>"
                            "<a href='https://www.gov.kr/mw/AA020InfoCappView.do?CappBizCD=14900000266' target='_blank' class='text-blue-600 underline'>👉 신청 바로가기</a>")

    elif button_title == "간병급여":
        response_message = ("📌 간병급여 안내\n중증 장해로 인해 간병이 필요한 경우 지급되는 급여입니다.\n\n"
                            "▶ 신청 조건: 요양 중 또는 장해 판정 후 간병이 필요한 경우\n"
                            "▶ 신청 시기: 의사의 소견에 따라 간병 필요 시\n"
                            "▶ 제출 서류: 간병급여신청서, 의사 소견서 등\n"
                            "▶ 제출처: 근로복지공단 또는 온라인<br/>"
                            "<a href='https://www.gov.kr/mw/AA020InfoCappView.do?HighCtgCD=A05007&CappBizCD=14900000267&tp_seq=01' target='_blank' class='text-blue-600 underline'>👉 신청 바로가기</a>")

    elif button_title == "장해등급표 보기":
        response_message = ("📊 장해등급은 1급부터 14급까지 있으며, 재해의 정도에 따라 판정됩니다.<br>"
                            "<a href='https://easylaw.go.kr/CSP/CnpClsMain.laf?popMenu=ov&csmSeq=575&ccfNo=4&cciNo=2&cnpClsNo=1' target='_blank'>👉 장해등급 기준표 보기</a>")

    elif button_title == "장해등급 판정 기준":
        response_message = ("⚖️ 장해등급 판정 기준은 치료 종료 후 장해가 남았을 때 근로자의 노동능력 상실률, 부위, 일상생활 수행능력 등을 종합적으로 평가합니다.\n\n"
                            "📄 산재 장해등급 판정 기준:<br/>"
                            f"<a href='/static/file/산재 장해등급 판정 기준.pdf' download class='link-blue'>산재 장해등급 판정 기준 보기</a>")

    elif button_title == "장해급여 금액 안내":
        response_message = ("💰 장해급여는 등급에 따라 다음과 같이 지급됩니다:\n"
                            "• 1급: 평균임금의 329일분 (연금)\n"
                            "• 4~7급: 연금 or 일시금 선택\n"
                            "• 8~14급: 일시금 지급\n\n"
                            f"<img src='/static/images/장해급여표.png' alt='장해급여 표' "
                            "style='width:100%; max-width:400px; border:1px solid #ccc; border-radius:8px;' />" )

    # 공통 반환
    return jsonify(message=response_message, buttons=buttons)
