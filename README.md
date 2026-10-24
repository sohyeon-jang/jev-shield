# Jev-Shield
 
통화 초반 문장으로 보험·대출·피싱 전화를 분류하고, 기준에 해당하면 경고를 띄우는 Flask 웹 데모입니다.<br>
분류에는 TypeSafe의 Jev API(`jev-1.13.0`)를 썼습니다. 입력은 웹 화면에 넣는 가상 문장이며, 실제 통화 연동은 포함하지 않습니다.
 
## 결과
 
가상 문장 66건(INSURANCE 11, LOAN 11, PHISHING 11, NORMAL 33)을 호출했고 실패는 없었습니다.
 
| 기준 | 지표 | 값 |
| :--- | :--- | :--- |
| category만 | 정확도 | 89.4% (59/66) |
| category만 | 스팸 탐지율 | 100% (33/33) |
| category만 | 정상 전화 오탐 | 6/33 |
| category + risk 기준값 | 스팸 경고 | 31/33 |
| category + risk 기준값 | 정상 전화 오탐 | 1/33 |
 
- 응답 시간은 중앙값 224 ms입니다(최소 198, 최대 478). 작성자 컴퓨터에서 잰 값이고 네트워크 왕복을 포함합니다.
- category가 틀린 7건 중 6건은 보험사·은행의 정상 안내 전화였습니다.
- 경고가 뜨지 않은 스팸은 보험 2건(risk 2.29, 2.35)입니다.
## 동작
 
Jev에 두 가지를 묻습니다.
 
- `category`: INSURANCE, LOAN, PHISHING, NORMAL 중 하나
- `risk`: 0(위험 없음)~4(매우 높음), 확률이 반영되어 소수로 나옴
category가 스팸 종류이고 risk가 기준값 이상이면 경고합니다.
 
| category | risk 기준 |
| :--- | :---: |
| INSURANCE | 2.5 이상 |
| LOAN | 3.0 이상 |
| PHISHING | 2.0 이상 |
 
기준값은 테스트 세트와 별도로 만든 예시 문장 10개로 정한 임시 값입니다.
 
## 실행
 
```bash
conda activate jev-shield
pip install flask requests python-dotenv
```
 
```
JEV_API_KEY=본인_키
```
 
```bash
python evaluate.py   # 66건 평가, results.csv 생성
python app.py        # http://localhost:5001
```
 
## 파일
 
| 파일 | 역할 |
| :--- | :--- |
| `jev_client.py` | Jev 호출, category·risk 추출 |
| `t3_samples.py` | 기준값용 예시 문장 호출 |
| `testset.csv` | 가상 테스트 문장 66건 |
| `evaluate.py` | 전체 호출, 지표 계산 |
| `app.py` | 웹 서버, 경고 판정 |
| `templates/index.html` | 입력·결과 화면 |
 
## 한계
 
- 직접 만든 가상 문장 66건의 결과라서 실제 통화를 대표하지 못합니다.
- 보험은 스팸과 정상의 risk가 겹칩니다. 기준값을 낮추면 놓친 스팸은 잡히지만 정상 문장에도 경고가 뜹니다.
- 같은 문장을 두 번 호출하면 risk가 0.01~0.13 달라졌습니다. 기준값 근처에서는 경고 여부가 바뀔 수 있습니다.
- 음성 인식 시간과 모바일 네트워크 지연은 반영하지 않았습니다.
테스트 문장과 번호는 모두 가상입니다.
