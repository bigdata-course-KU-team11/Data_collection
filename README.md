# 2020 빅데이터 청년인재 고려대학교 과정
#### NoonMap Project

## 11조 프로젝트 소개
  ### 11조원
    김민석, 신은채

  ### 주제
    수도권 지역의 교량 침수 위험도 예측 'NoonMap' 프로젝트

  ### 내용
    1. 관측소별 하천 수위, 교량 데이터 EDA 및 전처리를 통한 모델 Train, Test용 Database 생성
    2. 시계열 모델(Prophet, RNN, LSTM, GRU) 활용한 과거 하천 수위 패턴 학습 후, 이를 기반으로 미래 하천 수위 예측
    3. 실시간 하천 수위 값 활용한 미래 하천 수위를 예측하여 Map에 시각화를 통해 직관적으로 전달하는 웹 서비스
    
  ### 서비스 개요
    서비스의 이름인 NOONMAP은 눈(NOON)으로 보는 맵(MAP)을 줄인 것으로, 교량별 침수 위험도를 지도상에 나타내어 한눈에 볼 수 있는 저희 서비스의 특성을 나타냅니다.
    NOONMAP 서비스는 현재의 침수 위험도가 아닌 1시간 후의 침수 위험도를 제공합니다.
    이는 과거 하천 수위의 패턴을 분석하고, 시계열 모델을 통해 예측한 1시간 후의 하천 수위와 교량별 높이를 고려하여 산출해낸 지표입니다.

  ### requirements.txt
    프로젝트 실행을 위한 Python 패키지 목록입니다.
    pip install -r requirement.txt 명령어를 통해 설치할 수 있습니다.
    pip uninstall -r requirement.txt 명령어를 통해 삭제도 가능합니다.
    pip freeze > requirement.txt 명령어를 통해 설치한 모든 패키지 정리가 가능합니다.
    
  ### Database
    해당 Github에서는 프로젝트의 bridge_db.db 파일을 별도 첨부하지 않았습니다.
    
  ### 개발 환경
    데이터 수집, 전처리, DB 생성, 모델 개발: Jupyter Notebook, SQLite, Colab, Python
    웹 서비스 구현: Flask, Bootstrap, SQLAlchemy(ORM), HTML, CSS, JavaScript

  ### 결과물
   웹 페이지 구성: home, about, services, team
    
    1. home -> about
      1-1) home의 start 버튼을 눌러 about 화면으로 이동합니다.
![img1](https://github.com/bigdata-course-KU-team11/NoonMap-Project/blob/master/img/step1.gif)

    2. about -> services
      2-1) 서울, 인천, 경기 지역 중 교량 침수 위험도를 예측하고 싶은 지역을 선택합니다.
      2-2) 서울 지역을 선택 후, 서울 지역 내의 교량들을 markercluster로 나타남을 볼 수 있습니다.
![img1](https://github.com/bigdata-course-KU-team11/NoonMap-Project/blob/master/img/step2.gif)

    3. services
      3-1) 서울 지역의 markercluster를 click하여 해당 좌표에 위치한 교량들의 침수 위험도 정보(안전, 주의, 위험)를 marker의 색을 통해 1차 확인 가능합니다.
      3-2) 해당 교량의 marker를 클릭하여 popup을 통해 세부 정보를 확인할 수 있습니다.
![img1](https://github.com/bigdata-course-KU-team11/NoonMap-Project/blob/master/img/step3.gif)

    4. services
      4-1) 동일하게 다른 지역의 교량 침수 위험도를 확인할 수 있습니다.
![img1](https://github.com/bigdata-course-KU-team11/NoonMap-Project/blob/master/img/step5.gif)
