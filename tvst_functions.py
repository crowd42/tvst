#!/sur/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3

from colorama import init, Fore, Style
from prettytable import from_db_cursor


def banner():

    init()
    print(Fore.GREEN + """
_________          _______ _________
\__   __/|\     /|(  ____ \\__   __/
   ) (   | )   ( || (    \/   ) (
   | |   | |   | || (_____    | |
   | |   ( (   ) )(_____  )   | |
   | |    \ \_/ /       ) |   | |
   | |     \   /  /\____) |   | |
   )_(      \_/   \_______)   )_(

          """ + Style.RESET_ALL + "by crowd42")


def menu():
    """The main menu of tvst."""

    print("""
          1) Add a show.
          2) Update a show.
          3) Delete a show.
          4) List all the tvshows.
          5) Search for a show
          6) Filter by day.
          7) Search for tv show in IMDB site.
          8) Export the database as csv file
          0) Exit TVST
          """)


def create_connection(db_file):
    """ Create a database connection to the SQLite databse specified by
    db_file
    """

    conn = sqlite3.connect(db_file)
    return conn


def create_table(conn):
    """ Create a table in the database."""

    cur = conn.cursor()
    create_table_query = """CREATE TABLE IF NOT EXISTS tvshows(
        id INTEGER PRIMARY KEY,
        title TEXT UNIQUE,
        airing_day TEXT,
        season INTEGER,
        totalSeasons INTEGER,
        genre TEXT,
        episode INTERGER,
        imdbID TEXT,
        imdbRating TEXT)"""

    cur.execute(create_table_query)


def add_show(conn, show_infos):
    """Add  a tv show to the database."""

    cur = conn.cursor()
    insert_query = """INSERT INTO tvshows (title,
              airing_day,
              season,
              totalSeasons,
              genre,
              episode,
              imdbID,
              imdbRating
              ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    cur.execute(insert_query, show_infos)


def update_tvshow(conn, show_details):
    """Update a tvshow."""

    update_query = """UPDATE tvshows
    SET airing_day = ?,
    season = ?,
    episode = ?
    WHERE title = ?"""
    cur = conn.cursor()
    cur.execute(update_query, show_details)


def update_airing_day(conn, airing_day):
    """ Update the airing day of a tvshow"""

    update_query = "UPDATE tvshows SET airing_day = ? WHERE title = ?"
    cur = conn.cursor()
    cur.execute(update_query, airing_day)


def update_last_episode(conn, episode):
    """ Update the last episode been watched"""

    update_query = "UPDATE tvshows SET episode = ? WHERE title = ?"
    cur = conn.cursor()
    cur.execute(update_query, episode)


def update_season(conn, season):
    """ Update the current season been watched"""

    update_query = "UPDATE tvshows SET season = ?WHERE title = ?"
    cur = conn.cursor()
    cur.execute(update_query, season)


def delete_show(conn, title):
    """Detele a tvshow from the database"""

    del_query = "DELETE FROM tvshows WHERE title = ?"
    cur = conn.cursor()
    cur.execute(del_query, title)


def display_tvshows(conn):
    """List all the tvshows in the database"""

    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM tvshows")
    tvshows = from_db_cursor(rows)
    return tvshows


def search_show(conn, title):
    """Search for a tvshow in the database"""

    cur = conn.cursor()
    row = cur.execute("SELECT * FROM tvshows WHERE title = ?", (title,))
    tvshow = from_db_cursor(row)
    return tvshow


def filter_by_day(conn, day):
    """Return all the the tvhsows airing at a given day."""

    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM tvshows where airing_day = ?", (day,))
    tvshows = from_db_cursor(rows)
    return tvshows
