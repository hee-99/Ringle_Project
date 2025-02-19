# 모듈 로드하기

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from konlpy.tag import Okt
from sklearn.model_selection import train_test_split
import matplotlib
import re

# 데이터 로드하기
test_data = pd.read_csv('링글_250208.csv')
test_data.info()

# 필요한 열만 빼서 진행
test_data = test_data[['score', 'content']]

# 평점에 맞게 label 설정
def star_evaluate(rating):
  if rating >=4:
    return 1
  elif rating <= 3:
    return 0

test_data['label'] = test_data['score'].apply(star_evaluate)

# 한글만 데이터 프레임에 저장하는 코드
test_data = test_data.replace({'content':{r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]' :  r''}}, regex=True)

# 불용어 제거
stopwords = [
    '의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '를', '으로', '자', '에', '와', '한',
    '하다', '에', '는', '가', '이다', '을', '를', '이', '다', '그', '가', '에', '한', '하다', '것',
    '등', '그리고', '나', '아니', '있다', '없다', '이다', '같다', '때문에', '등', '그', '고', '의','도','앱','못','.','...',',','..','좋아요','좋습니다', '너무', '!', '입니다', '더', '','수업',
    '돼서','어플','년','계속','중','휴대폰','때','이후', 'tt','ttt','t','영어','수','할','로','하는','하고', '에서', '0', '링글', 'pxa', 'x','하면', '정말', '많이'
]

stopwords = list(set(stopwords))


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@

okt = Okt()

# 리뷰 토근화 진행
test_data['tokenized'] = test_data['content'].apply(okt.morphs)
test_data['tokenized'] = test_data['tokenized'].apply(lambda x: [item for item in x if item not in stopwords])

# 워드클라우드 시각화

#https://hangeul.naver.com/font 에서 나눔글꼴 다운로드


from PIL import Image
import matplotlib
matplotlib.rcParams['figure.facecolor'] = 'white'
matplotlib.rcParams['axes.facecolor'] = 'white'

from collections import Counter
import matplotlib.font_manager as fm
fontpath = r"C:\Users\user\OneDrive\바탕 화면\개인 프로젝트\프리텐다드\public\static\alternative\Pretendard-Regular.ttf" #각자의 경로를 넣습니다.
font = fm.FontProperties(fname=fontpath, size=9)
plt.rcParams['font.family'] = font.get_name()

plt.rcParams['axes.unicode_minus'] = False

from wordcloud import WordCloud

# 이미지 로드
img = Image.open('동그라미.png')
imgArray = np.array(img)

# negative_words = np.hstack(test_data[test_data.label == 0]['tokenized'].values)
positive_words = np.hstack(test_data[test_data.label == 1]['tokenized'].values)

# nw = Counter(negative_words)
# print(nw.most_common(20))
# # 빈도가 높은 순으로 15개
# nwc = nw.most_common(15)

pw = Counter(positive_words)
print(pw.most_common(20))
pwc = pw.most_common(15)

# wordCloud생성
# 한글꺠지는 문제 해결하기위해 font_path 지정
# negative_word_cloud = WordCloud(font_path=fontpath,
#                background_color='white', width=800, height=600,mask=imgArray)
positive_word_cloud = WordCloud(font_path=fontpath,
               background_color='white', width=800, height=600,mask=imgArray)

# '''부정'''
# print(dict(nwc))
# cloud = negative_word_cloud.generate_from_frequencies(dict(nwc))
# plt.figure(figsize=(10, 8))
# plt.title('구글 플레이 스토어 부정 리뷰 키워드')
# plt.axis('off')
# plt.imshow(cloud)
# plt.show()

'''긍정'''
print(dict(pwc))
cloud = positive_word_cloud.generate_from_frequencies(dict(pwc))
plt.figure(figsize=(10, 8))
plt.title('Most Common Positive Words')
plt.axis('off')
plt.imshow(cloud)
plt.show()


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# 화상영어 이용자 목적 시각화 코드

df = pd.read_csv('화상영어_리뷰_250208.csv')

# 2️⃣ 학습 목적 키워드 사전 정의
keywords = {
    "비즈니스 영어": ["비즈니스", "회의", "프레젠테이션", "업무", "회사", "직장", "비즈니스 영어"],
    "면접 준비": ["면접", "인터뷰", "취업", "외국계", "지원", "HR"],
    "유학 준비": ["유학", "교환학생", "대학원", "에세이", "논문", "아카데믹"],
    "시험 대비": ["IELTS", "토플", "TOEFL", "시험", "스피킹 테스트", "점수", "리딩", "리스닝"],
}

# 3️⃣ 학습 목적 키워드 빈도 분석
category_count = Counter()

for review in df["content"].dropna():  # NaN 값 제외
    for category, words in keywords.items():
        if any(re.search(rf"\b{word}\b", review, re.IGNORECASE) for word in words):
            category_count[category] += 1

# 4️⃣ 총 리뷰 수 및 비율 계산
total_reviews = len(df["content"].dropna())  # 총 리뷰 개수
keyword_ratios = {key: (value / total_reviews) * 100 for key, value in category_count.items()}

# 키워드 비율 데이터를 리스트 형식으로 변환
keyword_ratios = dict(keyword_ratios)  # 딕셔너리 형태로 변환
labels = list(keyword_ratios.keys())
sizes = list(keyword_ratios.values())

# 파이 차트 시각화 (폰트 크기 및 볼드 적용)
plt.figure(figsize=(8, 8))

# 파이 차트 생성
wedges, texts, autotexts = plt.pie(
    sizes, 
    labels=labels, 
    autopct="%1.1f%%", 
    startangle=140, 
    colors=["#EFEBFF", "#A995F4", "#775AE6", "#8d8d8d"]
)

# 폰트 크기 및 볼드 설정
for text in texts:  # 라벨 (카테고리명) 설정
    text.set_fontsize(20)
    text.set_fontweight('bold')

for autotext in autotexts:  # 퍼센트 값 설정
    autotext.set_fontsize(20)
    autotext.set_fontweight('bold')

# 제목 설정 (폰트 크기 및 볼드)
plt.title("화상 영어 시장 학습 목적 키워드 비율", fontsize=20, fontweight='bold')


plt.savefig("keyword_pie_chart.png", transparent=True, dpi=300)  # PNG 저장 (투명 배경)

# 차트 표시
plt.show()
