import pandas_gbq
import pandas as pd
import numpy as np
import geopy.distance
import datetime
import pytz
import seaborn as sb
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings("ignore")

##### data transformation #####
# create base dataset, each row represents one booking allocation
# output indicates whether the allocation trip is completed
# having the same columns as test, except output (to be predicted for test data)

created_booking_cols = ['event_timestamp', 'order_id','trip_distance', 'pickup_latitude', 'pickup_longitude']
created = booking[booking.booking_status =='CREATED'][created_booking_cols]

completed_booking_cols = ['order_id', 'driver_id']
completed = booking[booking.booking_status == 'COMPLETED'][completed_booking_cols]

booking_base = pd.merge(created, completed, on=['order_id'], how='left').rename(columns={'driver_id':'booking_driver_id'})

driver_cols = ['order_id', 'driver_id', 'driver_latitude', 'driver_longitude', 'driver_gps_accuracy']
driver_base = driver[driver_cols]

dataset = pd.merge(driver_base, booking_base, on=['order_id'], how='left')
dataset['output'] = np.where(dataset['driver_id'] == dataset['booking_driver_id'], 1, 0)
dataset = dataset.drop(columns = "booking_driver_id")

###### feature engineering ######
# create new features
df = dataset.copy()

## distance between pickup and driver location 
def cal_dist(row):
    lat_x, long_x, lat_y, long_y = row['pickup_latitude'], row['pickup_longitude'], row['driver_latitude'], row['driver_longitude']
    coord_x = (lat_x, long_x)
    coord_y = (lat_y, long_y)
    return geopy.distance.distance(coord_x, coord_y).km

df['pickup_distance'] = df.apply(cal_dist, axis=1)

## check is booking CREATED timestamp is in peak hour (defined by gojek official website, considering Jarkata timezone)
local_tz = pytz.timezone('Asia/Jakarta')

def is_peak(row):
    utc_ts = row['event_timestamp']
    local_dt = utc_ts.replace(tzinfo=pytz.utc).astimezone(local_tz)
    
    day = local_dt.isoweekday()
    time = local_dt.time()
    
    if 1 <= day <= 4:
        if ((time >= datetime.time(7, 0)) and (time <= datetime.time(10, 0))) | ((time >= datetime.time(17, 0)) and (time <= datetime.time(20, 0))):
            return 1
        else:
            return 0
    else:
        if ((time >= datetime.time(8, 0)) and (time <= datetime.time(10, 0))) | ((time >= datetime.time(17, 0)) and (time <= datetime.time(23, 59))):
            return 1
        else:
            return 0

df['is_peak'] = df.apply(is_peak, axis=1)

## number of times a driver is allocated but failed to complete trip (regardless failure reason)
df['failed'] = np.where(df['output'] == 1, 0, 1)
failed = df.groupby(['driver_id'], as_index=False)['failed'].sum().rename(columns={'failed': 'total_failed'})
df = pd.merge(df, failed, on ='driver_id')

# number of times a driver completes trip 

df['completed'] = np.where(df['output'] == 1, 1, 0)
completed = df.groupby(['driver_id'], as_index=False)['completed'].sum().rename(columns={'completed': 'total_completed'})
df = pd.merge(df, completed, on ='driver_id')

# features selected for modelling 
x_cols = ['trip_distance', 'driver_gps_accuracy', 'pickup_distance', 'is_peak', 'total_failed', 'total_completed']
X = df[x_cols]
y = df['output']






