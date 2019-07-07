# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import pandas_gbq

def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    project_id='ds-assignments'

    #### load data from google cloud platform ######
    booking_log = pandas_gbq.read_gbq('SELECT * FROM go_ride_allocation.booking_log', project_id=project_id, dialect='legacy')
    driver_log = pandas_gbq.read_gbq('SELECT * FROM go_ride_allocation.participant_log', project_id=project_id, dialect='legacy')
    test_data = pandas_gbq.read_gbq('SELECT * FROM go_ride_allocation.test_data', project_id=project_id, dialect='legacy')

    #### preprocessing #####
    # remove duplicates
    # handle records with same key but different values
    # fillna for empty driver_id of booking_log.booking_status=='CREATED'
    
    ## train
    agg_booking = {'event_timestamp': 'min', 'trip_distance': 'mean', 'pickup_latitude': 'mean', 'pickup_longitude': 'mean'}
    booking = booking_log.drop_duplicates().fillna('').groupby(['order_id', 'booking_status', 'customer_id', 'driver_id'], as_index=False).agg(agg_booking)
    
    agg_driver = {'driver_latitude': 'mean', 'driver_longitude': 'mean', 'driver_gps_accuracy': 'mean'}
    driver = driver_log.drop_duplicates().groupby(['order_id', 'driver_id'], as_index=False).agg(agg_driver)

    # test
    agg_test = {'event_timestamp': 'min', 'trip_distance': 'mean', 'pickup_latitude': 'mean', 'pickup_longitude': 'mean', 'driver_latitude': 'mean', 'driver_longitude': 'mean', 'driver_gps_accuracy': 'mean'}
    test = test_data.drop_duplicates().groupby(['order_id', 'customer_id', 'driver_id'], as_index=False).agg(agg)

    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
