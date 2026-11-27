import pandas as pd


def 정제(df):
	정제된_df = df.copy()

	# 점수가 비어 있는 행을 삭제한다.
	정제된_df = 정제된_df.dropna(subset=["점수"])
	print(f"점수 누락 제거 후: {len(정제된_df)}행")

	# 모든 열이 같은 중복 행을 하나만 남긴다.
	정제된_df = 정제된_df.drop_duplicates()
	print(f"중복 제거 후: {len(정제된_df)}행")

	# 반과 과목의 앞뒤 공백을 제거한다.
	정제된_df["반"] = 정제된_df["반"].str.strip()
	정제된_df["과목"] = 정제된_df["과목"].str.strip()
	print(f"공백 제거 후: {len(정제된_df)}행")

	# 점수가 0점 이상 100점 이하인 행만 남긴다.
	정제된_df = 정제된_df[정제된_df["점수"].between(0, 100)]
	print(f"점수 범위 필터 후: {len(정제된_df)}행")

	반별_점수_평균 = 정제된_df.groupby("반")["점수"].mean()
	print(반별_점수_평균)

	과목별_반별_점수_평균 = 정제된_df.groupby(["과목", "반"])["점수"].mean()
	print(과목별_반별_점수_평균)

	return 정제된_df


def 반별평균(df):
	반별_통계 = (
		df.groupby("반")["점수"]
		.agg(["count", "mean", "median", "max"])
		.round(2)
		.rename(columns={"count": "개수", "mean": "평균", "median": "중앙값", "max": "최댓값"})
	)
	print(반별_통계)
	return 반별_통계["평균"]
