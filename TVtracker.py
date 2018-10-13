import requests
import json
import os

API_KEY = "6196d2e11723c3b287d1ce400d57469e"
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2MTk2ZDJlMTE3MjNjM2IyODdkMWNlNDAwZDU3NDY5ZSI" \
            "sInN1YiI6IjViNzgwYzUxYzNhMzY4NjBkZjAxMTg0YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.q" \
            "JU1hZ7ivhVfhfu2KvgskV8s7b2MHnyTsjjjpwBy8O0"
MAIN_FILE = "./series_follower.json"


def create_json():
    data = {
        "Watchlist": {
            "TV Shows": [],
            "Movies": []
        },
        "Favorites": {
            "TV Shows": [],
            "Movies": []
        },
        "Current Episodes": {}
    }
    # write to new file
    with open(MAIN_FILE, 'w+') as fp:
        json.dump(data, fp)


def update_data(new_data):
    with open(MAIN_FILE, 'w') as fp:
        json.dump(new_data, fp)


# gets a string to search for, and returns the search results in json format.
def search_multi(search_for_string):
    response = \
        requests.get("https://api.themoviedb.org/3/search/multi?api_key={}&query={}".format(API_KEY, search_for_string))
    content = response.content
    return json.loads(content)


# updates current episode of the result.
def update_episode(tv_name):
    new_num = input("What's your current episode on {}?\n".format(tv_name))
    with open(MAIN_FILE) as fp:
        data = json.load(fp)
    # change episode number
    current_episodes = data.get('Current Episodes')
    current_episodes[tv_name] = new_num
    update_data(data)
    print("Action done successfully.\n")


def get_episode(tv_name):
    with open(MAIN_FILE) as fp:
        data = json.load(fp)
    # change episode number
    episodes = data.get('Current Episodes')
    current = episodes[tv_name]
    print("Your current episode on {} is {}.\n".format(tv_name, current))


def add_to_watchlist(title, title_name):
    with open(MAIN_FILE) as fp:
        data = json.load(fp)
    # add to watchlist
    watchlist = data.get('Watchlist')
    if title.get('media_type') == 'movie':
        watchlist.get("Movies").append(title_name)
    else:
        watchlist.get("TV Shows").append(title_name)
    update_data(data)
    print("Action done successfully.\n")


def remove_from_watchlist(title, title_name):
    with open(MAIN_FILE) as fp:
        data = json.load(fp)
    # remove from watchlist
    watchlist = data.get('Watchlist')
    if title.get('media_type') == 'movie':
        watchlist.get("Movies").remove(title_name)
    else:
        watchlist.get("TV Shows").remove(title_name)
    update_data(data)
    print("Action done successfully.\n")


def add_to_fav(title, title_name):
    with open(MAIN_FILE) as fp:
        data = json.load(fp)
    # add to favorites
    faves = data.get('Favorites')
    if title.get('media_type') == 'movie':
        faves.get("Movies").append(title_name)
    else:
        faves.get("TV Shows").append(title_name)
    update_data(data)
    print("Action done successfully.\n")


def remove_from_fav(title, title_name):
    with open(MAIN_FILE) as fp:
        data = json.load(fp)
    # remove from favorites
    faves = data.get('Favorites')
    if title.get('media_type') == 'movie':
        faves.get("Movies").remove(title_name)
    else:
        faves.get("TV Shows").remove(title_name)
    update_data(data)
    print("Action done successfully.\n")


def print_faves():
    with open(MAIN_FILE) as fp:
        data = json.load(fp)
    faves = data.get('Favorites')
    fave_tv = faves.get('TV Shows')
    fave_movies = faves.get('Movies')
    print("***Favorite TV Shows:***")
    print(*fave_tv, sep='\n')
    print("***Favorite Movies:***")
    print(*fave_movies, sep='\n')


def print_watchlist():
    with open(MAIN_FILE) as fp:
        data = json.load(fp)
    watchlist = data.get('Watchlist')
    tv = watchlist.get('TV Shows')
    movies = watchlist.get('Movies')
    print("~~~Watchlist:~~~")
    print("***TV Shows:***")
    print(*tv, sep='\n')
    print("***Movies:***")
    print(*movies, sep='\n')


def get_title_and_name():
    search_for = input("Search for a TV show or a movie.\n")
    search_result = search_multi(search_for)

    # ask user which search result they meant.
    results = search_result.get('results')
    result = {}
    answer = 'no'

    if len(results) == 0:  # no result found
        print("Error. Please try again with a different title.")
        return None, None

    for result in results:
        if result.get('media_type') == 'movie':
            title_name = result.get('original_title')
        else:
            title_name = result.get('original_name')
        overview = result.get('overview')
        answer = input("Did you mean \"{}\" - \"{}\"\ny/n? \n".format(title_name, overview))
        if answer == 'y':
            return result, title_name

    if answer != 'y' or (len(result) == 0):  # no result found, or answer was never yes.
        print("Error. Please try again with a different title.")
        return None, None


def add_or_remove_titles():
    title, name = get_title_and_name()

    # check if there was an error.
    if title is None or name is None:
        return

    while True:
        choice = input("What would you like to do with {}?\n"
                       "a - update current episode\n"
                       "b - add to watchlist\n"
                       "c - remove from watchlist\n"
                       "d - add to favorites\n"
                       "e - remove from favorites\n"
                       "f - get current episode\n"
                       "r - return\n"
                       "q - quit\n".format(name))
        if choice == 'a':
            update_episode(name)
            break
        elif choice == 'b':
            add_to_watchlist(title, name)
            break
        elif choice == 'c':
            remove_from_watchlist(title, name)
            break
        elif choice == 'd':
            add_to_fav(title, name)
            break
        elif choice == 'f':
            get_episode(name)
        elif choice == 'e':
            remove_from_fav(title, name)
            break
        elif choice == 'r':
            break
        elif choice == 'q':
            exit()
        else:
            print("Please choose again. \n")


def run():
    print("Welcome to TVtracker, your ultimate binge helper.")
    while True:
        choice = input("What would you like to do?\n"
                       "a - print watchlist\n"
                       "b - print favorites\n"
                       "c - add or remove a title\n"
                       "h - help!\n"
                       "q - quit\n")
        if choice == 'a':
            print_watchlist()
        elif choice == 'b':
            print_faves()
        elif choice == 'c':
            add_or_remove_titles()
        elif choice == 'h':
            print("TVtracker (all rights reserved) is your ultimate binge helper.\n"
                  "You can use it to keep track on your current episode state on TV shows you're watching,\n"
                  "manage a watchlist for later watch or add movies and TV shows to your favorites list.\n"
                  "Enjoy!\n")
        elif choice == 'q':
            exit()
        else:
            print("Sorry, I didn't quite get that. Please choose again.")


# create file if it doesn't exist, then run the program.
if not os.path.isfile(MAIN_FILE):  # file doesn't exist
    create_json()
run()
