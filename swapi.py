import requests

# Base URL for the Star Wars API
base_url = "https://swapi.dev/api"


def make_api_request(endpoint, params=None):
    try:
        response = requests.get(f"{base_url}/{endpoint}/", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None


# Exercise 1: Find all ships that appeared in Return of the Jedi
def find_ships_in_return_of_the_jedi(film_title):
    film_data = make_api_request("films", params={"search": film_title})

    if not film_data or not film_data.get("results"):
        return []

    film = film_data["results"][0]
    starships = make_api_request("starships")

    if starships and starships.get("results"):
        starships_in_jedi = [ship for ship in starships["results"] if film["url"] in ship["films"]]
        return starships_in_jedi


# Exercise 2: Find all ships that have a hyperdrive rating >= 1.0
def find_ships_with_hyperdrive_rating(min_hyperdrive_rating):
    starships = make_api_request("starships")

    if not starships or not starships.get("results"):
        return []
    hyperdrive_ships = [ship for ship in starships["results"] if
                        float(ship["hyperdrive_rating"]) >= min_hyperdrive_rating]
    return hyperdrive_ships


def count_ship_crew_members(starships):
    for ship in starships["results"]:
        crew = ship["crew"]

        # Remove commas from the crew value
        crew = crew.replace(",", "")

        # Check if the crew value is a range (e.g., "30-165")
        if '-' in crew:
            min_range, max_range = map(int, crew.split('-'))
            if min_crew_size <= min_range <= max_crew_size or min_crew_size <= max_range <= max_crew_size:
                yield ship
        else:
            crew_count = int(crew)
            if min_crew_size <= crew_count <= max_crew_size:
                yield ship


# Exercise 3: Find all ships that have crews between 3 and 100
def find_ships_with_crew_size(min_crew_size, max_crew_size):
    starships = make_api_request("starships")

    if starships and starships.get("results"):
        return list(count_ship_crew_members(starships))
    else:
        return []


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
