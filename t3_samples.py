import time

from jev_client import call_jev, parse

# 가상으로 만든 예시 문장 (의도한 label, 문장)
SAMPLES = [
    ("INSURANCE", "고객님, 지금 쓰시는 실손보험보다 보장이 넓은 상품이 나와서 연락드렸어요. 잠깐 설명 들어 보시겠어요?"),
    ("INSURANCE", "OO생명 설계사인데요, 요즘 무료로 보장 분석을 해 드리고 있습니다."),
    ("LOAN", "정부지원 저금리 대출 대상자로 선정되셨습니다. 한도 조회 도와드릴까요?"),
    ("LOAN", "신용등급 상관없이 당일 대출 가능합니다. 필요한 금액 말씀해 주세요."),
    ("PHISHING", "서울중앙지검 수사관입니다. 고객님 명의 계좌가 범죄에 연루되어 안전계좌로 이체하셔야 합니다."),
    ("PHISHING", "엄마, 나 폰 고장 나서 친구 폰으로 연락해. 급하게 돈 좀 보내줘."),
    ("NORMAL", "OO화재입니다. 고객님 자동차보험 만기가 다음 달이라 갱신 안내드리려고 전화드렸습니다."),
    ("NORMAL", "OO은행입니다. 신청하신 대출 서류 중 소득증빙이 빠져서 연락드렸습니다."),
    ("NORMAL", "OO병원입니다. 내일 오후 3시 진료 예약 확인차 연락드렸습니다."),
    ("NORMAL", "택배 기사인데요, 문 앞에 두고 가도 될까요?"),
]

print("의도\t예측\trisk\tms\t문장")
for label, text in SAMPLES:
    result, ms = call_jev("010-0000-0000", text)
    if result is None:
        print(f"{label}\t(실패)\t-\t{ms:.0f}\t{text}")
    else:
        category, risk = parse(result)
        print(f"{label}\t{category}\t{risk}\t{ms:.0f}\t{text}")
    time.sleep(0.2)
