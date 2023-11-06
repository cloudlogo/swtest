import requests

# Base URL for the Star Wars API
base_url = "https://swapi.dev/api"


def make_api_request(endpoint, params=None):
    temp = list()
    page = 1
    next_url = f"{base_url}/{endpoint}/?page={page}"  # Remove one question mark here
    if params:
        next_url += '&' + '&'.join([f'{key}={value}' for key, value in params.items()])
    while next_url:
        query_results = requests.get(next_url).json()
        temp.extend(query_results['results'])
        next_url = query_results['next']
    return temp

# Exercise 1: Find all ships that appeared in Return of the Jedi
def find_ships_in_return_of_the_jedi(film_title):
    film_data = make_api_request("films", params={"search": film_title})

    if not film_data or not isinstance(film_data, list):
        return []

    film = film_data[0]  # The first item in the list
    starships = make_api_request("starships")

    if starships and isinstance(starships, list):
        starships_in_jedi = [ship for ship in starships if film["url"] in ship.get("films", [])]
        return starships_in_jedi
    else:
        return []


# Exercise 2: Find all ships that have a hyperdrive rating >= 1.0
def find_ships_with_hyperdrive_rating(min_hyperdrive_rating):
    starships = make_api_request("starships")

    if not starships or not isinstance(starships, list):
        return []

    hyperdrive_ships = [ship for ship in starships if ship["hyperdrive_rating"] != 'unknown' and float(ship["hyperdrive_rating"]) >= min_hyperdrive_rating]
    return hyperdrive_ships


# Exercise 3: Find all ships that have crews between 3 and 100
def find_ships_with_crew_size(min_crew_size, max_crew_size):
    starships = make_api_request("starships")

    if not starships or not isinstance(starships, list):
        return []

    def is_valid_crew(crew):
        try:
            crew_count = int(crew.replace(',', ''))
            return min_crew_size <= crew_count <= max_crew_size
        except ValueError:
            return False

    crew_ships = [ship for ship in starships if is_valid_crew(ship.get("crew", "0"))]
    return crew_ships


if __name__ == "__main__":
    # Exercise 1
    film_title = "Return of the Jedi"
    print("Exercise 1: Ships that appeared in Return of the Jedi")
    ships_in_return_of_the_jedi = find_ships_in_return_of_the_jedi(film_title)
    for ship in ships_in_return_of_the_jedi:
        print(ship["name"], ship["url"])

    # Exercise 2
    min_hyperdrive_rating = 1.0
    print(f"\nExercise 2: Ships with hyperdrive rating >= {min_hyperdrive_rating}")
    ships_with_hyperdrive_rating = find_ships_with_hyperdrive_rating(min_hyperdrive_rating)
    for ship in ships_with_hyperdrive_rating:
        print(ship["name"], ship["url"])

    # Exercise 3
    min_crew_size = 3
    max_crew_size = 100
    print(f"\nExercise 3: Ships with crews between {min_crew_size} and {max_crew_size}")
    ships_with_crew_size = find_ships_with_crew_size(min_crew_size, max_crew_size)
    for ship in ships_with_crew_size:
        print(ship["name"], ship["url"])
