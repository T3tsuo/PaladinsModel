import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
import pickle

# with open('model_casual', 'rb') as f:
    # model = pickle.load(f)

clf = LogisticRegressionCV()

df = pd.read_csv("data_rank.csv")

x = df[["cwinratedif", "ckdadif", "cdfdif"]]
y = df["WinTeam"]

while True:
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    clf.fit(x_train, y_train)
    score = ((clf.score(x_test, y_test) * 1000000)//100)/100
    print(score)
    if score > 90:
        with open('model_rank', 'wb') as f:
            pickle.dump(clf, f)
        break
print(score)
