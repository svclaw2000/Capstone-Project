# 인스타그램 캡션 추천 알고리즘
> 순천향대학교 빅데이터공학과 2020-2 캡스톤프로젝트1 결과물

## Introduction
인스타그램 게시물을 작성할 때, 어떤 해시태그를 달아야할지 고민되는 분들을 위한 알고리즘  
좋아요를 많이 받을 수 있는 해시태그 추천 및 이미지에 어울리는 문구 추천

## Features
- 3개월간 수집한 7개 카테고리의 22개 해시태그에 해당하는 약 400GB의 이미지와 캡션 데이터 사용
  ```
  셀카 : 셀카
  일상 : 일상, 소통, 데일리
  패션 : 패션, 남친룩, 여친룩
  음식 : 음식, 먹스타그램, 카페, 맛집
  여행 : 여행, 하늘, 바다, 산
  연애 : 연애, 커플사진, 커플사진관
  애완동물 : 애완동물, 댕댕, 냥냥
  ```
### 이미지에 대한 카테고리 분류
- 모델 구조: CNN + DNN
- Train Accuracy: 71%, Validation Accuracy: 53%
### 이미지 + 분류를 이용한 문장 생성
- 모델 구조
  - CNN + 감정 태깅 + RNN
  - CNN + seq2seq
  - Stacked Autoencoder + (LSTM / Seq2Seq / GAN)
- 데이터의 특성에 맞는 모델을 선택하지 못하여 

## Test Environments
```
Ubuntu 16.04 LTS
Python 3.7
```

## Framework and Dependency
```
Flask 1.1.2
Tensorflow 2.3.1
konlpy 0.5.2
nltk 3.5
Pillow 7.2.0
KNU 한국어 감성사전
```

## 👨‍💻 Members
- [박규훤](https://github.com/svclaw2000): [FrontEnd/ML&DL Engineering] svclaw2000@gmail.com
- [김아경](https://github.com/EP000): [ML&DL Engineering] bxzx55@gmail.com
- [서민지](https://github.com/jaaaamj0711): [ML&DL Engineering] jaaaamj0711@gmail.com
