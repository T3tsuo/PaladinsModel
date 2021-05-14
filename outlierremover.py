import numpy as np
import matplotlib.pyplot as plt
from pandas import read_csv
from scipy import stats

df = read_csv("data_rank.csv")

plt.hist(df.cdfdif)
plt.show()

z_scores = stats.zscore(df)
abs_z_scores = np.abs(z_scores)
filtered_entries = (abs_z_scores < 3).all(axis=1)

new_df = df[filtered_entries]

plt.hist(new_df.cdfdif)
plt.show()

# new_df.to_csv("data_rank_new.csv", mode='wb', header=True, index=False)
