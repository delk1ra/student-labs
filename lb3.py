import pandas as pd
from catboost import CatBoostClassifier

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

X = train.drop(columns=['id', 'smoking'])
y = train['smoking']
X_test = test.drop(columns=['id'])
test_ids = test['id']

model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.03,
    depth=6,
    eval_metric='AUC',
    random_seed=42,
    verbose=False
)
model.fit(X, y)

y_pred = model.predict_proba(X_test)[:, 1]

submission = pd.DataFrame({'id': test_ids, 'smoking': y_pred}).round(3)
submission.to_csv('submission.csv', index=False)