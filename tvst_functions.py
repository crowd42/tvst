#!/sur/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3
import sys

from colorama import init, Fore, Style
from PIL import Image, ImageDraw, ImageFont
from prettytable import from_db_cursor

# Make the connection to the database.
db = sqlite3.connect('tvst.db')
c = db.cursor()


def banner():

    ShowText = 'TVST'

    font = ImageFont.truetype('arialbd.ttf', 15)  # load the font
    size = font.getsize(ShowText)  # calc the size of text in pixels
    image = Image.new('1', size, 1)  # create a b/w image
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), ShowText, font=font)  # render the text to the bitmap
    for rownum in range(size[1]):
        # scan the bitmap:
        # print ' ' for black pixel and
        # print '*' for white one
        line = []
        for colnum in range(size[0]):
            if image.getpixel((colnum, rownum)):
                line.append(' '),
            else:
                line.append('*')

        # strip colors if stdout is redirected
        init(strip=not sys.stdout.isatty())
        print(Fore.RED + ''.join(line) + Style.RESET_ALL)
    print('\n\t\tby crowd42')


def menu():
    """The main menu of tvst."""

    print("""
          1) Add a show.
          2) Update a show.
          3) Delete a show.
          4) List all the tvshows.
          5) Search for a show
          6) Filter by day.
          0) Exit TVST
          """)


def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS tvshows(
        id INTEGER PRIMARY KEY,
        title TEXT UNIQUE,
        airing_day TEXT,
        season INTEGER,
        totalSeasons INTEGER,
        genre TEXT,
        episode INTERGER,
        imdbID TEXT,
        imdbRating TEXT)""")
    db.commit()


def add_show(title, airing_day, season, totalSeasons,
             genre, episode, imdbID, imdbRating):
    """Add  a tv show to the database."""

    c.execute("""INSERT INTO tvshows (title,
              airing_day,
              season,
              totalSeasons,
              genre,
              episode,
              imdbID,
              imdbRating
              ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (title, airing_day, season,
                                                     totalSeasons, genre,
                                                     episode, imdbID,
                                                     imdbRating))
    db.commit()


def update_tvshow(show_details):
    """Update a tvshow."""

    update_query = """UPDATE tvshows
    SET airing_day = ?,
    season = ?,
    episode = ?
    WHERE title = ?"""
    c.execute(update_query, show_details)
    db.commit()


def delete_show(title):
    """Detele a tvshow from the database"""

    del_query = "DELETE FROM tvshows WHERE title = ?"
    c.execute(del_query, title)
    db.commit()


def display_tvshows():
    """List all the tvshows in the database"""

    rows = c.execute("SELECT * FROM tvshows")
    tvshows = from_db_cursor(rows)
    return tvshows


def search_show(title):
    """Search for a tvshow in the database"""

    row = c.execute("SELECT * FROM tvshows WHERE title = ?", (title,))
    tvshow = from_db_cursor(row)
    return tvshow


def filter_by_day(day):
    """Return all the the tvhsows airing at a given day."""

    rows = c.execute("SELECT * FROM tvshows where airing_day = ?", (day,))
    tvshows = from_db_cursor(rows)
    return tvshows
