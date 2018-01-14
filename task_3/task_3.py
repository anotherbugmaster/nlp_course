import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor

texts = []

with open('texts_train.txt', 'r') as reader:
    for line in reader:
        texts.append(line)

scores = []

with open('scores_train.txt', 'r') as reader:
    for line in reader:
        scores.append(int(line))

X_train = pd.Series(texts, name='text')
y_train = pd.Series(scores, name='score')

pipeline = Pipeline([
    ('vect', TfidfVectorizer(min_df=3, max_df=0.95)),
    ('clf', XGBRegressor()),
])

parameters = {
    'vect__ngram_range': [(1, 2)],
    'clf__n_estimators': [1000, 2000],
    'clf__max_depth': [3, 5, 10],
}

grid_search = GridSearchCV(
    pipeline, parameters, scoring='neg_mean_squared_error', n_jobs=-1
)
grid_search.fit(X_train, y_train)

n_candidates = len(grid_search.cv_results_['params'])
for i in range(n_candidates):
    print(i, 'params - %s; mean - %0.2f; std - %0.2f'
          % (grid_search.cv_results_['params'][i],
             grid_search.cv_results_['mean_test_score'][i],
             grid_search.cv_results_['std_test_score'][i]))

test_texts = []

with open('dataset_40757_1.txt', 'r') as reader:
    for line in reader:
        test_texts.append(line)

X_pred = pd.Series(test_texts, name='text')

y_pred = grid_search.predict(X_pred)
y_pred = [int(round(score)) for score in y_pred]
y_pred = [score if score >= 1 else 0 for score in y_pred]
y_pred = [score if score <= 10 else 10 for score in y_pred]

with open('result.txt', 'w+') as writer:
    writer.writelines([str(score) + '\n' for score in y_pred])
