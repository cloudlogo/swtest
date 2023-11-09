from requests import sessions

# Base URL for the Star Wars API
base_url = "https://swapi.dev/api"


def get_all_data(endpoint, session, params=None):
    url = f"{base_url}/{endpoint}"
    resp = session.get(url, params=params).json()
    for result in resp["results"]:
        yield result
    next_url = resp["next"]
    while next_url:
        resp = session.get(next_url, params=params).json()
        next_url = resp['next']
        for result in resp["results"]:
            yield result


# Exercise 1: Find all ships that appeared in Return of the Jedi
def find_ships_in_return_of_the_jedi(film_title, session):
    for film in get_all_data("films", session, params={"search": film_title}):
        print(f"Exercise 1: Ships that appeared in {film['title']}")
        for starship in film["starships"]:
            yield session.get(starship).json()


# Exercise 2: Find all ships that have a hyperdrive rating >= 1.0
def find_ships_with_hyperdrive_rating(min_hyperdrive_rating, session):
    for ship in get_all_data("starships", session):
        if ship["hyperdrive_rating"] != 'unknown' and float(ship["hyperdrive_rating"]) >= min_hyperdrive_rating:
            yield ship


# Exercise 3: Find all ships that have crews between 3 and 100
def find_ships_with_crew_size(min_crew_size: int, max_crew_size: int, session: sessions.Session):
    for starship in get_all_data("starships", session):
        if is_valid_crew(min_crew_size, starship["crew"], max_crew_size):
            yield starship


def is_valid_crew(min: int, crew: str, max: int) -> bool:
    crew_size = 0
    try:
        return min <= int(crew) <= max
    except ValueError:
        if crew == "unknown":
            return False
        if "-" in crew:
            interval = crew.split("-")
            return min <= int(interval[0]) and int(interval[1]) <= max
        if "," in crew:
            return min <= int(crew.replace(",", "")) <= max
        return False


if __name__ == "__main__":
    session = sessions.Session()
    # Exercise 1
    for ship in find_ships_in_return_of_the_jedi("Return of the Jedi", session):
        print(ship["name"], ship["url"])

    # Exercise 2
    min_hyperdrive_rating = 1.0
    print(f"\nExercise 2: Ships with hyperdrive rating >= {min_hyperdrive_rating}")
    for ship in find_ships_with_hyperdrive_rating(min_hyperdrive_rating, session):
        print(ship["name"], ship["url"], f"Hyperdrive rating: {ship['hyperdrive_rating']}")

    # Exercise 3
    min_crew_size = 3
    max_crew_size = 100
    print(f"\nExercise 3: Ships with crews between {min_crew_size} and {max_crew_size}")
    for ship in find_ships_with_crew_size(min_crew_size, max_crew_size, session):
        print(ship["name"], ship["url"], f"Crew size: {ship['crew']}")
