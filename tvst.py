#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import requests

from tvst_functions import add_show, create_table, update_tvshow, search_show,\
    menu, delete_show, display_tvshows, filter_by_day, banner


def main():
    """ Main program"""

    url = 'http://www.omdbapi.com'
    api_key = '50e91ed2'

    os.system('clear')
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
                # We need this to construct our url and get the exact we're
                # looking for, for exmaple there's a movie and tvshow called
                # Me, Myself and I
                show_type = input('show type (series/movies): ')
                airing_day = input('Airing day: ')
                season = input('Season: ')
                episode = input('Episode: ')
                payloads = {'t': title, 'type': show_type, 'apikey': api_key}
                resp = requests.get(url, params=payloads)
                data = resp.json()
                add_show(data['Title'],
                         airing_day,
                         season,
                         data['totalSeasons'],
                         data['Genre'],
                         episode,
                         data['imdbID'],
                         data['imdbRating'])

            elif choice == 2:
                title = input('Title: ').title()
                airing_day = input('Airing day: ')
                season = input('Season: ')
                episode = input('Episode: ')
                update_tvshow((airing_day, season, episode, title))

            elif choice == 3:
                title = input('Title: ')
                delete_show((title,))

            elif choice == 4:
                tvshows = display_tvshows()
                print(tvshows)

            elif choice == 5:
                title = input('Title: ').title()
                tvshow = search_show(title)
                print(tvshow)

            elif choice == 6:
                airing_day = input('Airing day: ')
                tvshows = filter_by_day(airing_day)
                print(tvshows)

            else:
                print('Please type a number between 0 and 6.')
        except ValueError:
            print('You did not enter a valid number!')
            continue


if __name__ == '__main__':
    create_table()
    main()
