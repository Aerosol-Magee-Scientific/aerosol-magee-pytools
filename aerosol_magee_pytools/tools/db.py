# Copyright (c) 2026 Aerosol d.o.o.
# Licensed under the Aerosol Magee Scientific Software License
# (see LICENSE file for details)

import sqlite3


def get_db_schema(db_path: str) -> tuple[dict, dict]:
    """
    Inspect a SQLite database and return column names for all tables and views.

    Parameters
    ----------
    db_path : str
        Absolute or relative path to the SQLite database file.

    Returns
    -------
    tables : dict
        {table_name: [column_name, ...]} for every table in the database.
    views : dict
        {view_name: [column_name, ...]} for every view in the database.

    Examples
    --------
    >>> tables, views = get_db_schema(r'C:/data/my_instrument.db')
    >>> tables.keys()
    dict_keys(['Data', 'Setup', ...])
    >>> views['DataView']
    ['ID', 'StartTimeUTC', 'EndTimeUTC', ...]
    """
    tables = {}
    views = {}

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name, type FROM sqlite_master "
            "WHERE type IN ('table', 'view') "
            "ORDER BY type, name"
        )
        objects = cursor.fetchall()

        for name, obj_type in objects:
            cursor.execute(f"PRAGMA table_info('{name}')")
            columns = [row[1] for row in cursor.fetchall()]  # row[1] = column name

            if obj_type == 'table':
                tables[name] = columns
            else:
                views[name] = columns

    return tables, views


