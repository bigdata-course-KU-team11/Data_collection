# 데이터 수집 및 전처리 폴더
## 1. 실시간 발송 재난문자 수집
- 국민재난안전포털에서 selenium을 이용하여 실시간으로 기재되는 재난문자 정보를 수집
- file: data_web_crawler.ipynb
- link: http://www.safekorea.go.kr/idsiSFK/neo/main/main.html
## 2. 과거 재난문자 수집
- 공공데이터포털의 재난문자방송 발령현황 API 서비스를 활용
- 시작일 2011/11/18 기준
- json 형태로 받은 뒤, pandas의 DataFrame 형식으로 변환하여 활용
- file: api_crawling.ipynb
- link: https://www.data.go.kr/data/3058822/openapi.do
## 3. 데이터 전처리
- 안전문자 word-tokenization
