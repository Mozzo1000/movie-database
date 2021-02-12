"""
TODO: Move all this to Rackfocus
"""

import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))


def create_index():
    conn = sqlite3.connect(os.path.join(basedir, '../movies.db'))
    cursor = conn.cursor()
    index = "CREATE INDEX index_movie ON title_basics(tconst, primaryTitle)"
    cursor.execute(index)
    conn.commit()
    conn.close()


create_index()
