import json
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"

QUESTIONS = {
    "category": {
        "type": "choice",
        "instructions": "이 통화 초반 내용이 어떤 종류의 전화인지 고르세요.",
        "criteria": {
            "INSURANCE": "보험 가입을 권유하는 전화",
            "LOAN": "대출을 권유하는 전화",
            "PHISHING": "개인정보나 송금을 요구하는 보이스피싱 의심 전화",
            "NORMAL": "위에 해당하지 않는 일반 전화",
        },
    },
    "risk": {
        "type": "score",
        "instructions": "이 통화가 스팸이나 사기일 위험이 어느 정도인지 평가하세요.",
        "criteria": ["위험 없음", "낮음", "보통", "높음", "매우 높음"],
    },
}


def call_jev(phone, text):
    """Jev API를 호출하고 (응답 JSON, 걸린 시간 ms)를 반환한다. 실패하면 (None, ms)."""
    api_key = os.getenv("JEV_API_KEY")
    if not api_key:
        print("JEV_API_KEY를 찾지 못했습니다. .env 파일을 확인하세요.")
        return None, 0

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": MODEL,
        "state": f"발신번호: {phone}\n통화 내용: {text}",
        "questions": QUESTIONS,
    }

    start = time.perf_counter()
    try:
        response = requests.post(API_URL, headers=headers, json=body, timeout=30)
    except requests.RequestException as e:
        ms = (time.perf_counter() - start) * 1000
        print(f"요청을 보내지 못했습니다: {e}")
        return None, ms
    ms = (time.perf_counter() - start) * 1000

    if response.status_code != 200:
        print(f"서버 오류: 상태 번호 {response.status_code}")
        print(f"메시지: {response.text}")
        return None, ms

    return response.json(), ms


def parse(result):
    """응답 JSON에서 (category, risk)를 꺼낸다."""
    answers = result["answers"]
    category = answers["category"]["choice"]
    risk = answers["risk"]["score"]
    return category, risk


if __name__ == "__main__":
    # 가상으로 만든 예시 번호와 문장
    phone = "010-0000-0000"
    text = "안녕하세요, 고객님. 이번에 새로 나온 암보험 상품이 있어서 안내드리려고 연락드렸습니다."

    result, ms = call_jev(phone, text)
    print(f"응답 시간: {ms:.0f} ms")

    if result is not None:
        print("응답 전체:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("answers.category:", json.dumps(result.get("answers", {}).get("category"), ensure_ascii=False))
        print("answers.risk:", json.dumps(result.get("answers", {}).get("risk"), ensure_ascii=False))
