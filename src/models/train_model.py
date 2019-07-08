import logging
import click
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

x_cols = ['trip_distance', 'driver_gps_accuracy', 'pickup_distance', 'is_peak', 'total_failed', 'total_completed']

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())

def main(input_filepath, output_filepath):
    # load processed data 
    df = pd.read_csv(input_filepath + '/train_model.csv')

    # select features for modelling 
    X = df[x_cols]
    y = df['output']

    # train
    lr_final = LogisticRegression(random_state=42, solver='lbfgs', penalty = 'l2')
    lr_final.fit(X, y)

    # output a pickle file for the model
    joblib.dump(lr_final, output_filepath + '/lr.pkl') 

    logger = logging.getLogger(__name__)
    logger.info('save trained model')

  
if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
    



    


