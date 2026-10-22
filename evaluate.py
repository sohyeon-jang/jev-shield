import time

import pandas as pd

from jev_client import call_jev, parse

PHONE = "010-0000-0000"  # 가상 번호

testset = pd.read_csv("testset.csv")

rows = []
for i, item in enumerate(testset.itertuples(), start=1):
    result, ms = call_jev(PHONE, item.text)
    if result is None:
        category, risk = None, None
    else:
        category, risk = parse(result)
    rows.append({
        "text": item.text,
        "label": item.label,
        "category": category,
        "risk": risk,
        "ms": round(ms),
    })
    print(f"[{i}/{len(testset)}] {item.label} -> {category} (risk {risk}, {ms:.0f} ms)")
    time.sleep(0.2)

df = pd.DataFrame(rows)
df.to_csv("results.csv", index=False, encoding="utf-8-sig")
print("\nresults.csv 저장 완료")

failed = df["category"].isna().sum()
ok = df[df["category"].notna()]
spam = ok[ok["label"] != "NORMAL"]
normal = ok[ok["label"] == "NORMAL"]

accuracy = (ok["category"] == ok["label"]).mean()
detection = (spam["category"] != "NORMAL").mean()
false_positive = (normal["category"] != "NORMAL").mean()

print("\n=== 결과 ===")
print(f"전체 문장: {len(df)}건 (호출 실패 {failed}건, 지표는 성공한 {len(ok)}건 기준)")
print(f"정확도: {accuracy:.1%} ({(ok['category'] == ok['label']).sum()}/{len(ok)})")
print(f"스팸 탐지율: {detection:.1%} ({(spam['category'] != 'NORMAL').sum()}/{len(spam)})")
print(f"정상 전화 오탐률: {false_positive:.1%} ({(normal['category'] != 'NORMAL').sum()}/{len(normal)})")

print("\n=== 혼동 행렬 (행: 정답, 열: 예측) ===")
print(pd.crosstab(ok["label"], ok["category"]).to_string())

print("\n=== label별 risk ===")
print(ok.groupby("label")["risk"].agg(["mean", "min", "max"]).round(2).to_string())

print(f"\n응답 시간 중앙값: {ok['ms'].median():.0f} ms")

wrong = ok[ok["category"] != ok["label"]]
print(f"\n=== 틀린 문장 ({len(wrong)}건) ===")
for item in wrong.itertuples():
    print(f"정답 {item.label} / 예측 {item.category} / risk {item.risk}: {item.text}")
