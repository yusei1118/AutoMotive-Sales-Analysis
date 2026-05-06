import pandas as pd

df = pd.read_csv("car_prices.csv", engine="python", on_bad_lines="skip")

print(df.head())

df["vin_length"] = df["vin"].astype(str).apply(len)

print(df["vin_length"].value_counts())


broken = df[df["vin_length"] != 17].copy()

broken_shifted = broken.copy()

cols = list(df.columns)

# 右に1つズレてる → 左に戻す
broken_shifted[cols] = broken_shifted[cols].shift(-1, axis=1)

df_fixed = df.copy()

df_fixed.loc[broken.index] = broken_shifted

df_fixed["vin_length"] = df_fixed["vin"].astype(str).apply(len)
print(df_fixed["vin_length"].value_counts())

##################################################################
import numpy as np

df = df_fixed.copy()

# 数値に変換
df["sellingprice"] = pd.to_numeric(df["sellingprice"], errors="coerce")
df["mmr"] = pd.to_numeric(df["mmr"], errors="coerce")

# 1ドルは明らかに異常なので除外
df = df[df["sellingprice"] != 1].copy()

# 修正前の価格を保存
df["sellingprice_original"] = df["sellingprice"]

# ratio作成
df["ratio_before"] = df["sellingprice"] / df["mmr"]

# 10倍くらい高い場合 → 10分の1にする
df.loc[
    (df["ratio_before"] >= 8) & (df["ratio_before"] <= 12),
    "sellingprice"
] = df["sellingprice"] / 10

# 10分の1くらい低い場合 → 10倍にする
df.loc[
    (df["ratio_before"] >= 0.08) & (df["ratio_before"] <= 0.12),
    "sellingprice"
] = df["sellingprice"] * 10

# 修正後ratio
df["ratio_after"] = df["sellingprice"] / df["mmr"]

# フラグ作成
df["flag_price_corrected"] = df["sellingprice"] != df["sellingprice_original"]

df["flag_outlier"] = (
    (df["ratio_after"] < 0.5) |
    (df["ratio_after"] > 3)
)

# 確認
print(df[["mmr", "sellingprice_original", "sellingprice", "ratio_before", "ratio_after", "flag_price_corrected", "flag_outlier"]].head())

print(df["flag_price_corrected"].value_counts())
print(df["flag_outlier"].value_counts())

df["ratio_before"] = df["ratio_before"].round(3)
df["ratio_after"] = df["ratio_after"].round(3)

# いらない列を消す
df = df.drop(columns=["sellingprice_original"], errors="ignore")

# trim列も消したい場合
df = df.drop(columns=["trim"], errors="ignore")
df = df.drop(columns=["vin"], errors="ignore")
# 新しいCSVとして保存
df.to_csv("car_prices_clean_final.csv", index=False)

print("Saved: car_prices_clean_final.csv")


##############################
import pandas as pd

# すでに整形済みのCSVを読む
df = pd.read_csv("Cleaned Car Final.csv")

# stateをきれいにする
df["state"] = df["state"].astype(str).str.upper().str.strip()

# カナダ州コード
canada_states = ["AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT"]

# country列を作る
df["country"] = "United States"
df.loc[df["state"].isin(canada_states), "country"] = "Canada"


# 確認（これ重要）
print(df[["state","country"]].head(20))

# 同じファイル名で上書き
df.to_csv("Cleaned Car Final.csv", index=False)

print("Updated country column successfully.")