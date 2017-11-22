#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import pandas.io.sql as sql
import requests

from tvst_functions import add_show, create_table, update_tvshow, search_show,\
    menu, delete_show, display_tvshows, filter_by_day, banner,\
    create_connection, update_airing_day, update_last_episode, update_season


def main():
    """ Main program"""

    # Clear the screen
    os.system('clear')

    db = 'series.db'
    conn = create_connection(db)
    # create the sql table if it doesn't exist.
    create_table(conn)
    url = 'http://www.omdbapi.com'
    # api key from omdbapi.com, you can get one for free.
    api_key = '50e91ed2'

    banner()

    while True:
        menu()

        choice = input('tvst> ')
        if choice == '0' or choice == 'exit' or choice == 'quit':
            print('See you later o/')
            sys.exit()

        # If choice equal 1, rpompt the user to add a show
        elif choice == '1':
            title = input('Title: ')

            # We need to specify the show type (movie or serie)to construct
            # our url and get the exact we'relooking for, for exmaple
            # there's a movie and tvshow calledMe, Myself and I.
            show_type = input('show type (series/movies): ')
            airing_day = input('Airing day: ')

            # The current season you're watching
            season = input('Season: ')
            # Last episode you watched.
            episode = input('Episode: ')

            payloads = {'t': title, 'type': show_type, 'apikey': api_key}
            resp = requests.get(url, params=payloads)
            data = resp.json()

            # Catch an error if the Tvshow's title entered by the user is
            # valid and does exist at IMDB.
            try:
                show_infos = (data['Title'],
                              airing_day,
                              season,
                              data['totalSeasons'],
                              data['Genre'],
                              episode,
                              data['imdbID'],
                              data['imdbRating'])
                with conn:
                    add_show(conn, show_infos)
            except KeyError:
                print("This show doesn't exist!")

        elif choice == '2':
            print("""Choose an option:
      1) Update all the infos
      2) Update the airing day
      3) Update the last episode watched
      4) update the current season you're watching
      0) Return back to the main menu""")
            update_options = input('option: ')
            if update_options == '0':
                continue

            # Update the airing day, the last epsiode been watched and
            # the last season
            elif update_options == '1':
                title = input('Title: ').title()
                airing_day = input('Airing day: ')
                season = input('Season: ')
                episode = input('Episode: ')

                with conn:
                    update_tvshow(
                        conn, (airing_day, season, episode, title))
            # Update the airing day of tvshow

            elif update_options == '2':
                title = input('Title: ').title()
                airing_day = input('Airinf day: ').capitalize()
                with conn:
                    update_airing_day(conn, (airing_day, title))

            # Update the last episode been watched
            elif update_options == '3':
                title = input('Title: ').title()
                episode = input('Episode: ')
                with conn:
                    update_last_episode(conn, (episode, title))

            # Update the current season been watched
            elif update_options == '4':
                title = input('Title: ').title()
                season = input('Season: ')
                with conn:
                    update_season(conn, (season, title))

        # Delete a tvshow.
        elif choice == '3':
            title = input('Title: ').title()
            delete_show(conn, (title,))

        # Display all the tvshows stored in the database.
        elif choice == '4':
            with conn:
                tvshows = display_tvshows(conn)
                print(tvshows)

        # Search for a show in the database
        elif choice == '5':
            title = input('Title: ').title()
            with conn:
                tvshow = search_show(conn, title)
                print(tvshow)

        # Search for the tvshows airing a given day
        elif choice == '6':
            airing_day = input('Airing day: ').capitalize()
            with conn:
                tvshows = filter_by_day(conn, airing_day)
                print(tvshows)

        elif choice == '7':
            title = input('Title: ')
            show_type = input('Tvshow type: ')
            search_payloads = {
                't': title,
                'type': show_type,
                'plot': 'full',
                'apikey': api_key}
            resp = requests.get(url, params=search_payloads)
            data = resp.json()
            print(
                '* Title: ' +
                data['Title'] +
                '\n* Genre: ' +
                data['Genre'] +
                ' \n* Seasons: ' +
                data['totalSeasons'] +
                '\n* IMDB ratings: ' +
                data['imdbRating'] +
                '\n* Plot: ' +
                data['Plot'])
        # Export the the tvshows as a csv file.
        elif choice == '8':
            with conn:
                table = sql.read_sql("SELECT * FROM tvshows", conn)
                table.to_csv('output.csv')
                if os.path.exists('output.csv'):
                    print('The export executed with success!')
                else:
                    print('The export failed.')

        else:
            print('Please type a number between 0 and 6.')


if __name__ == '__main__':
    main()
