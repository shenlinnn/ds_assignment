import logging
import click
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

from src.features.build_features import cal_dist, is_peak
from src.models.train_model import x_cols

@click.command()
@click.argument('data_folder', type=click.Path(exists=True))
@click.argument('model_folder', type=click.Path())

def main(data_folder, model_folder):
    # load test data
    test = pd.read_csv(data_folder + '/processed/test_model.csv')
    X_test = test[x_cols]

    # load trained model
    lr_final = joblib.load(model_folder + '/lr.pkl') 

    # calculate probability of each candidate driver, choose the one with highest p
    y_prob = pd.DataFrame(lr_final.predict_proba(X_test)).rename(columns={1: 'prob'})['prob']
    test_df = pd.concat([test, y_prob], axis=1)

    idx = test_df.groupby(['order_id'])['prob'].transform(max) == test_df['prob']
    result = test_df[idx][['order_id', 'driver_id']]

    result.to_csv(data_folder + '/final/phase2.csv', index=False)
    logger = logging.getLogger(__name__)
    logger.info('predict test data')

  
if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
    

