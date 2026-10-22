from flask import Flask, jsonify, render_template, request

from jev_client import call_jev, parse

app = Flask(__name__)

# 판정 기준 (PRD 3.1). risk가 이 값 이상이면 경고한다.
THRESHOLDS = {
    "INSURANCE": 2.5,
    "LOAN": 3.0,
    "PHISHING": 2.0,
}

ALERT_MESSAGES = {
    "INSURANCE": "보험 가입 권유 전화로 의심됩니다.",
    "LOAN": "대출 권유 전화로 의심됩니다.",
    "PHISHING": "보이스피싱이 의심됩니다. 개인정보나 송금 요구에 응하지 마세요.",
}


def decide_alert(category, risk):
    """경고 문구를 반환한다. 경고하지 않으면 None."""
    if category in THRESHOLDS and risk >= THRESHOLDS[category]:
        return ALERT_MESSAGES[category]
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    phone = data.get("phone", "").strip()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "통화 내용을 입력하세요."}), 400

    result, ms = call_jev(phone, text)
    if result is None:
        return jsonify({"error": "Jev API 호출에 실패했습니다. 터미널 출력을 확인하세요."}), 502

    category, risk = parse(result)
    return jsonify({
        "category": category,
        "risk": risk,
        "alert": decide_alert(category, risk),
        "ms": round(ms),
    })


if __name__ == "__main__":
    app.run(port=5001)
