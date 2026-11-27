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

	return 정제된_df
