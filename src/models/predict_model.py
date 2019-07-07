## transform test data

test['pickup_distance'] = test.apply(cal_dist, axis=1)
test['is_peak'] = test.apply(is_peak, axis=1)
test = pd.merge(test, failed, on='driver_id', how='left').fillna(0)
test = pd.merge(test, completed, on='driver_id', how='left').fillna(0)
X_test = test[x_cols]

## calculate probability of each candidate driver, choose the one with highest p
y_prob = pd.DataFrame(lr_final.predict_proba(X_test)).rename(columns={1: 'prob'})['prob']
test_df = pd.concat([test, y_prob], axis=1)

idx = test_df.groupby(['order_id'])['prob'].transform(max) == test_df['prob']
result = test_df[idx][['order_id', 'driver_id']]

result.to_csv('gojek_ds_assignment.csv', index=False)