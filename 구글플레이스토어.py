# 앱에 맞는 리뷰 가져오기

from google_play_scraper import reviews
import pandas as pd

# 크롤링할 앱 ID 설정 (구글 플레이 스토어 URL에서 확인 가능)
app_id = "kr.epopsoft.word"  # 예: 카카오톡

# 리뷰 크롤링 (200개 가져오기)
review_data, _ = reviews(
    app_id,
    lang="ko",  # 한국어 리뷰
    country="kr",  # 한국 스토어
    count=150,  # 가져올 리뷰 개수
)

# 데이터프레임으로 변환
df = pd.DataFrame(review_data)

df.to_csv('말해보카_250208.csv',index=False, encoding='utf-8-sig')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2

from google_play_scraper import reviews
import pandas as pd
# 1크롤링할 앱 ID 리스트
app_ids = [
    "com.cambly.cambly",
    "com.selabs.speak",
    "com.mint05.story",
    "kr.epopsoft.word",
    "com.ringle"
]

# 모든 앱의 리뷰를 저장할 리스트
all_reviews = []

# 반복문을 사용해 각 앱의 리뷰 크롤링
for app_id in app_ids:
    print(f"{app_id} 크롤링 중...")  # 진행 상황 출력

    try:
        review_data, _ = reviews(
            app_id,
            lang="ko",  # 한국어 리뷰
            country="kr",  # 한국 스토어
            count=10000,  # 가져올 리뷰 개수 (앱당 150개)
        )
        
        # 데이터프레임 변환 및 'app_id' 컬럼 추가
        df = pd.DataFrame(review_data)
        df["app_id"] = app_id  # 앱 ID 컬럼 추가
        all_reviews.append(df)  # 리스트에 추가

    except Exception as e:
        print(f"{app_id} 크롤링 실패: {e}")  # 오류 발생 시 출력
import csv
# 모든 리뷰 데이터 합치기
final_df = pd.concat(all_reviews, ignore_index=True)
final_df.to_csv('화상영어_250208.csv', index=False, quoting=csv.QUOTE_ALL)

# 데이터 저장하기
final_df.to_csv('화상영어_250208.csv', index=False, encoding='utf-8-sig', escapechar='\\')
