#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import requests

from tvst_functions import add_show, create_table, update_tvshow, search_show,\
    menu, delete_show, display_tvshows, filter_by_day, banner,\
    create_connection


def main():
    """ Main program"""

    # Clear the screen
    os.system('clear')

    db = 'series.db'
    conn = create_connection(db)
    create_table(conn)
    url = 'http://www.omdbapi.com'
    api_key = '50e91ed2'

    banner()

    while True:
        menu()
        try:
            choice = int(input('tvst> '))
            if choice == 0:
                print('See you later o/')
                sys.exit()

            # If choice equal 1, rpompt the user to add a show
            elif choice == 1:
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
                        add_show(conn, (show_infos))
                except KeyError:
                    print("This show doesn't exist!")

            elif choice == 2:
                title = input('Title: ').title()
                airing_day = input('Airing day: ')
                season = input('Season: ')
                episode = input('Episode: ')
                update_tvshow(conn, (airing_day, season, episode, title))

            elif choice == 3:
                title = input('Title: ')
                delete_show(conn, (title,))

            elif choice == 4:
                tvshows = display_tvshows(conn)
                print(tvshows)

            elif choice == 5:
                title = input('Title: ').title()
                tvshow = search_show(conn, title)
                print(tvshow)

            elif choice == 6:
                airing_day = input('Airing day: ')
                tvshows = filter_by_day(conn, airing_day)
                print(tvshows)

            else:
                print('Please type a number between 0 and 6.')
        except ValueError as e:
            print('You did not enter a valid number!')
            print(e)
            continue


if __name__ == '__main__':
    main()
