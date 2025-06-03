import json
import logging

import pandas as pd

logger = logging.Logger(__name__)

logger.info('loading data')
settlements_df = pd.read_csv('data/settlements.csv', sep=',')
logger.info('loaded settlements data')

settlements_df = settlements_df.groupby('region').agg('sum').reset_index('region')[['region', 'population']]
settlements_df.set_index('region', inplace=True)
logger.info('completed settlements preprocessing')

accidents_df = pd.read_csv('data/accidents.csv', sep=';')
logger.info('loaded accidents data')

accidents_df.rename(columns={'id': 'accident_id'}, inplace=True)
accidents_df.set_index('accident_id', inplace=True)
accidents_df['datetime'] = pd.to_datetime(accidents_df['datetime'])
accidents_df['year'] = accidents_df.apply(lambda row: row['datetime'].year, axis=1)
accidents_df['month'] = accidents_df.apply(lambda row: row['datetime'].month, axis=1)
accidents_df['hour'] = accidents_df.apply(lambda row: row['datetime'].hour, axis=1)
accidents_df = accidents_df[accidents_df['year'] < 2024]
accidents_df = accidents_df.join(settlements_df, on='region', how='left', rsuffix='_settlement')
logger.info('completed accidents preprocessing')

participants_df = pd.read_csv('data/participants.csv', sep=';')
logger.info('loaded participants data')

participants_df = participants_df.join(accidents_df, on='accident_id', how='inner', rsuffix='_accident')

dead_regex = r'\u0421\u043A\u043E\u043D\u0447\u0430\u043B\u0441\u044F.+'
injured_regex = r'\u0420\u0430\u043D\u0435\u043D\u044B\u0439.+'
injured_regex_2 = r'\u041F\u043E\u043B\u0443\u0447\u0438\u043B.+'
long_string = ('Пешеход, перед ДТП находившийся в (на) ТС в качестве водителя или пешеход, перед ДТП находившийся в ('
               'на) ТС в качестве пассажира')

participants_df['health_status'] = participants_df['health_status'].str.replace(dead_regex, 'Скончался', regex=True)
participants_df['health_status'] = participants_df['health_status'].str.replace(injured_regex, 'Раненый', regex=True)
participants_df['health_status'] = participants_df['health_status'].str.replace(injured_regex_2, 'Раненый', regex=True)

participants_df = participants_df[participants_df['role'] != long_string]
participants_df.set_index('region')
logger.info('completed participants preprocessing')

vehicles_df = pd.read_csv('data/vehicles.csv', sep=';')
logger.info('loaded vehicles data')

vehicles_df = vehicles_df.join(accidents_df, on='accident_id', how='inner', rsuffix='_accident')
logger.info('completed vehicles preprocessing')

geojson = json.load(open('data/russia.geojson'))
logger.info('loaded geojson data')
