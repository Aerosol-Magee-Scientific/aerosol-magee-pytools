# Copyright (c) 2026 Aerosol d.o.o.
# Licensed under the Aerosol Magee Scientific Software License
# (see LICENSE file for details)
import pandas as pd
import requests

from aerosol_magee_pytools.tools import parsing_datetime


def parse_date_uidep(timestamp):
    return (f'{timestamp.year:4d}-{timestamp.month:02d}-'
            f'{timestamp.day:02d}-{timestamp.hour:02d}-'
            f'{timestamp.minute:02d}-{timestamp.second:02d}')

def uidep_url(ip, start=None, end=None, components=None, values_typ='complex'):
    if values_typ not in ['complex', 'simple']:
        raise ValueError(f'UIDEP value type should be "complex" or "simple", not {values_typ}.')
    _url = f'http://{ip}:8080/values/{values_typ}/'

    if start is not None:
        _url += f'?start={parse_date_uidep(parsing_datetime(start))}'

    if end is not None:
        if start is None:
            raise ValueError("End parameter without Start parameter can not be used.")

        if parsing_datetime(end) < parsing_datetime(start):
            raise ValueError("End parameter can not be earlier than Start parameter.")

        _url += f'&end={parse_date_uidep(parsing_datetime(end))}'

    if components is not None:
        _components_url_end = ''
        if type(components) is int:
            _components_url_end += f'&component={components}'
        elif type(components) is list:
            for _c in components:
                _components_url_end += f'&component={_c}'
        else:
            raise ValueError(f'UIDEP components should be an integer or a list of integers, not {type(components)}.')

        # if start is None, then replace first '&' with '?'
        if start is None:
            _components_url_end = '?' + _components_url_end[1:]

        _url += _components_url_end

    return _url


def uidep_get_data(ip, start=None, end=None, components=None, values_typ='complex'):

    # get uidep data works only for complex value type;
    # for simple, you can generate only url, but you have to parse data yourself!
    if values_typ not in ['complex']:
        raise ValueError(f'UIDEP value type for parsing should be "complex", not {values_typ}.')

    _url = uidep_url(ip, start, end, components, values_typ)

    _auth_response = requests.get(_url)
    _data = _auth_response.json()

    if "ErrorDescription" in _data:
        raise ValueError(f'UIDEP returned an error: {_data["ErrorDescription"]}')

    _data_dict = {}
    for component in _data['Components']:

        # print(component['ID'], component['Component'], len(component['MeasuredValues']))
        if 'MeasuredValues' in component:
            if component['MeasuredValues']:
                _data_dict[component['Component']] = (
                    pd.DataFrame(
                        component['MeasuredValues'])['Value'].values)

    if _data_dict:
        return pd.DataFrame(_data_dict)
    else:
        return _data_dict
