import datetime

import pandas as pd


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