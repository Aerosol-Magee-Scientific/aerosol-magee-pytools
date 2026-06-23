import datetime

import pandas as pd
import numpy as np

DOTNET_EPOCH_OFFSET_SECONDS = 62135596800
DOTNET_EPOCH_OFFSET_MILLISECONDS = 62135596800000
DOTNET_EPOCH_OFFSET_TICKS = 621355968000000000


def parsing_datetime(text):
    if isinstance(text, datetime.datetime) or isinstance(text, pd.Timestamp):
        return text

    if isinstance(text, str):
        # solution when \n is in the string from argparse
        text = text.replace('\n', '').strip()

    for fmt in ('%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError(f'No valid date format found for parsing.\n{text}, {type(text)}')


def dotnet_seconds_to_datetime(series):
    values = pd.Series(pd.to_numeric(series, errors='coerce'), index=series.index)
    valid_values = values.dropna()
    if valid_values.empty:
        return pd.Series(pd.NaT, index=series.index, dtype='datetime64[ns]')

    sample_value = float(valid_values.iloc[0])

    if sample_value >= 1e17:
        unix_values = (values.astype('Int64') - DOTNET_EPOCH_OFFSET_TICKS) * 100
        converted = pd.to_datetime(np.asarray(unix_values, dtype='float64'),
                                   unit='ns',
                                   errors='coerce')
    elif sample_value >= 1e13:
        converted = pd.to_datetime(np.asarray(values, dtype='float64') - DOTNET_EPOCH_OFFSET_MILLISECONDS,
                                   unit='ms',
                                   errors='coerce')
    else:
        converted = pd.to_datetime(np.asarray(values, dtype='float64') - DOTNET_EPOCH_OFFSET_SECONDS,
                                   unit='s',
                                   errors='coerce')

    converted = converted.floor('min')
    return pd.Series(converted, index=series.index)


def datetime_to_dotnet_nanoseconds(series):
    timestamps = pd.to_datetime(series, errors='coerce')
    unix_ns = timestamps.astype('int64')  # nanoseconds since Unix epoch
    ticks = unix_ns // 100 + DOTNET_EPOCH_OFFSET_TICKS
    ticks[timestamps.isna()] = pd.NA
    return pd.array(ticks, dtype='Int64')


class Seasons:
    SEASON_NAMES = {1: 'Winter (DJF)',
                    2: 'Spring (MAM)',
                    3: 'Summer (JJA)',
                    4: 'Autumn (SON)'}

    SEASON_NAMES_SLO = {1: 'Zima (DJF)',
                        2: 'Pomlad (MAM)',
                        3: 'Poletje (JJA)',
                        4: 'Jesen (SON)'}

    SEASON_MONTHS = {1: [12, 1, 2],
                     2: [3, 4, 5],
                     3: [6, 7, 8],
                     4: [9, 10, 11]}

    @staticmethod
    def add_seasons(df, column_time='EndTimeUTC'):
        df['season'] = df[column_time].dt.month % 12 // 3 + 1
        return df

    @staticmethod
    def add_year_seasons(df, column_time='EndTimeUTC'):
        df = Seasons.add_seasons(df, column_time)

        df['year_season'] = df[column_time].dt.year
        # december is part of the winter next year
        df['year_season'][df[column_time].dt.month == 12] += 1
        df['year_season'] = \
            df['year_season'].astype(str) + '_' + df['season'].astype(str)

        year_seasons = df['year_season'].unique()
        year_season_names = []
        for s in year_seasons:
            year, season = s.split('_')
            year_season_names.append(
                f'{year} {Seasons.SEASON_NAMES[int(float(season))]}')

        return df, list(year_seasons), list(year_season_names)