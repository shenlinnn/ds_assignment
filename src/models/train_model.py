lr_final = LogisticRegression(random_state=42, solver='lbfgs', penalty = 'l2')
lr_final.fit(X, y)