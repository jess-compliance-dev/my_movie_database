import json

# File where the movies are stored
MOVIES_STORAGE_FILE = "data.json"


def get_movies():
    """
    Returns a list of movie dictionaries loaded from the JSON file.
    """
    with open(MOVIES_STORAGE_FILE, "r") as file:
        movies = json.load(file)
    return movies


def save_movies(movies):
    """
    Saves the given list of movies to the JSON file.
    """
    with open(MOVIES_STORAGE_FILE, "w") as file:
        json.dump(movies, file, indent=3)


def add_movie(title, year, rating, director, actors):
    """
    Adds a movie to the movie database.
    Loads the information from the JSON file, adds the movie,
    and saves it.
    """
    movies = get_movies()

    new_movie = {
        "title": title,
        "rating": rating,
        "year": year,
        "director": director,
        "actors": actors
    }

    movies.append(new_movie)
    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movie database.
    Loads the information from the JSON file, deletes the movie,
    and saves it.
    """
    movies = get_movies()
    updated_movies = []

    for movie in movies:
        if movie["title"].lower() != title.lower():
            updated_movies.append(movie)

    save_movies(updated_movies)


def update_movie(title, rating=None, year=None, director=None, actors=None):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it.
    """
    movies = get_movies()

    for movie in movies:
        if movie["title"].lower() == title.lower():
            if rating is not None:
                movie["rating"] = rating
            if year is not None:
                movie["year"] = year
            if director is not None:
                movie["director"] = director
            if actors is not None:
                movie["actors"] = actors
            break

    save_movies(movies)
