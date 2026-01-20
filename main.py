import random
import movie_storage


class Colors:
    BLUE = '\033[94m'
    LIGHT_BLUE = "\033[94m"
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'


def press_enter_to_continue():
    """
    Pause before returning to menu.
    """
    input(f"{Colors.BLUE}Press Enter to return to menu...{Colors.RESET}")


def print_title():
    """
    Print program title.
    """
    title = r"""
███╗   ███╗██╗   ██╗    ███╗   ███╗ ██████╗ ██╗   ██╗██╗███████╗███████╗
████╗ ████║╚██╗ ██╔╝    ████╗ ████║██╔═══██╗██║   ██║██║██╔════╝██╔════╝
██╔████╔██║ ╚████╔╝     ██╔████╔██║██║   ██║██║   ██║██║█████╗  ███████╗
██║╚██╔╝██║  ╚██╔╝      ██║╚██╔╝██║██║   ██║╚██╗ ██╔╝██║██╔══╝  ╚════██║
██║ ╚═╝ ██║   ██║       ██║ ╚═╝ ██║╚██████╔╝ ╚████╔╝ ██║███████╗███████║
╚═╝     ╚═╝   ╚═╝       ╚═╝     ╚═╝ ╚═════╝   ╚═══╝  ╚═╝╚══════╝╚══════
"""
    print(Colors.BLUE + Colors.LIGHT_BLUE + title + Colors.RESET)


def print_menu():
    """
    Display menu to navigate through program.
    """
    print(f"{Colors.BLUE}Menu:{Colors.RESET}")
    print("0. Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Statistics")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print("9. Filter movies\n")
    return input(f"{Colors.YELLOW}Enter choice (0-9): {Colors.RESET}")


def exit_movie():
    """
    Print 'Good-Bye' title after exiting the program.
    """
    title = r"""
                            _ _                _ 
       __ _  ___   ___   __| | |__  _   _  ___| |
      / _` |/ _ \ / _ \ / _` | '_ \| | | |/ _ \ |
     | (_| | (_) | (_) | (_| | |_) | |_| |  __/_|
      \__, |\___/ \___/ \__,_|_.__/ \__, |\___(_)
      |___/                         |___/        
"""
    print(Colors.BLUE + Colors.LIGHT_BLUE + title + Colors.RESET)


def list_movies():
    """
    List existing movies in the database.
    """
    movies = movie_storage.get_movies()
    print(f"{len(movies)} movies in total:")
    for movie in movies:
        actors_str = ""
        for actor in movie['actors']:
            if actors_str != "":
                actors_str += ", "
            actors_str += actor
        print(f"{movie['title']}, rating: {movie['rating']}, year: {movie['year']}, director: {movie['director']}, actors: {actors_str}")
    print()
    press_enter_to_continue()


def add_movie():
    """
    User can add movie to database.
    """
    new_title = input("Enter movie title: ").strip()
    if new_title == "":
        print(f"{Colors.RED}Title cannot be empty!{Colors.RESET}")
        return

    movies = movie_storage.get_movies()
    for movie in movies:
        if movie['title'].lower() == new_title.lower():
            print(f"{Colors.RED}Movie '{new_title}' already exists!{Colors.RESET}")
            return

    # Rating
    while True:
        rating_input = input("Enter movie rating (0-10, leave empty if unknown): ").strip()
        if rating_input == "":
            rating = "Unknown"
            break
        try:
            rating = float(rating_input)
            if rating < 0 or rating > 10:
                print(f"{Colors.RED}Rating must be between 0 and 10.{Colors.RESET}")
                continue
            break
        except ValueError:
            print(f"{Colors.RED}Please enter a valid number for rating.{Colors.RESET}")

    # Year
    while True:
        year_input = input("Enter release year (leave empty if unknown): ").strip()
        if year_input == "":
            year = "Unknown"
            break
        try:
            year = int(year_input)
            if year < 1888 or year > 2027:
                print(f"{Colors.RED}Please enter a realistic year between 1888 and 2027.{Colors.RESET}")
                continue
            break
        except ValueError:
            print(f"{Colors.RED}Please enter a valid number for year.{Colors.RESET}")

    # Director
    director = input("Enter director (leave empty if unknown): ").strip()
    if director == "":
        director = "Unknown"

    # Actors
    actors_input = input("Enter main actors (leave empty if unknown): ").strip()
    actors = []
    if actors_input == "":
        actors.append("Unknown")
    else:
        for actor in actors_input.split(","):
            actor = actor.strip()
            if actor != "":
                actors.append(actor)
        if not actors:
            actors.append("Unknown")

    movie_storage.add_movie(new_title, year, rating, director, actors)
    print(f"{Colors.YELLOW}Movie '{new_title}' successfully added.{Colors.RESET}")
    print()
    press_enter_to_continue()


def delete_movie():
    """
    User can delete movie from the database. Handles missing movie.
    """
    title_to_delete = input("Enter movie title to delete: ").strip()
    if title_to_delete == "":
        print(f"{Colors.RED}Title cannot be empty!{Colors.RESET}")
        return

    movies = movie_storage.get_movies()
    found = False
    for movie in movies:
        if movie['title'].lower() == title_to_delete.lower():
            found = True
            break

    if not found:
        print(f"{Colors.RED}Movie '{title_to_delete}' not found in the database.{Colors.RESET}")
        print()
        press_enter_to_continue()
        return

    movie_storage.delete_movie(title_to_delete)
    print(f"{Colors.YELLOW}Movie '{title_to_delete}' successfully deleted.{Colors.RESET}")
    print()
    press_enter_to_continue()


def update_movie():
    """
    Existing movie can be edited, e.g., rating, year, director, actors.
    """
    title = input("Enter movie title to update: ").strip()
    if title == "":
        print(f"{Colors.RED}Title cannot be empty!{Colors.RESET}")
        return

    movies = movie_storage.get_movies()
    found = False
    for movie in movies:
        if movie['title'].lower() == title.lower():
            found = True
            break

    if not found:
        print(f"{Colors.RED}Movie '{title}' not found!{Colors.RESET}")
        print()
        press_enter_to_continue()
        return

    # Update fields
    rating_input = input("Enter new rating (leave empty to skip): ").strip()
    year_input = input("Enter new year (leave empty to skip): ").strip()
    director_input = input("Enter new director (leave empty to skip): ").strip()
    actors_input = input("Enter new actors (comma separated, leave empty to skip): ").strip()

    rating = movie['rating'] if rating_input == "" else rating_input
    year = movie['year'] if year_input == "" else year_input
    director = movie['director'] if director_input == "" else director_input

    actors = movie['actors']
    if actors_input != "":
        new_actors = []
        for actor in actors_input.split(","):
            actor = actor.strip()
            if actor != "":
                new_actors.append(actor)
        if new_actors:
            actors = new_actors

    movie_storage.update_movie(title, rating=rating, year=year, director=director, actors=actors)
    print(f"{Colors.YELLOW}Movie '{title}' updated successfully.{Colors.RESET}")
    print()
    press_enter_to_continue()


def calculate_median(numbers):
    """
    Returns the median of a list of numbers.
    """
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    mid = n // 2
    if n % 2 == 1:
        return sorted_numbers[mid]
    else:
        return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2


def stats():
    """
    Analyze movie ratings: average, median, highest, lowest, best/worst movies.
    """
    movies = movie_storage.get_movies()
    ratings = []

    for movie in movies:
        try:
            rating = float(movie['rating'])
            ratings.append(rating)
        except (ValueError, TypeError):
            continue

    if len(ratings) == 0:
        print("No numeric ratings available.")
        press_enter_to_continue()
        return

    average_rating = sum(ratings) / len(ratings)
    median_rating = calculate_median(ratings)
    highest_rating = max(ratings)
    lowest_rating = min(ratings)

    best_movies = []
    worst_movies = []

    for movie in movies:
        try:
            rating = float(movie['rating'])
            if rating == highest_rating:
                best_movies.append(movie['title'])
            if rating == lowest_rating:
                worst_movies.append(movie['title'])
        except (ValueError, TypeError):
            continue

    print("Average rating: {:.2f}".format(average_rating))
    print("Median rating: {:.2f}".format(median_rating))
    print("Highest rating: {} → {}".format(highest_rating, ", ".join(best_movies)))
    print("Lowest rating: {} → {}".format(lowest_rating, ", ".join(worst_movies)))
    print()
    press_enter_to_continue()


def random_movie():
    """
    Gives randomly a movie choice to user from the database.
    """
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies available for recommendation.")
        press_enter_to_continue()
        return
    movie = random.choice(movies)
    print(f"Movie recommendation: {movie['title']} → {movie['rating']}")
    print()
    press_enter_to_continue()


def search_movie():
    """
    Search for movies whose titles contain a user-entered keyword.
    """
    query = input("Enter part of movie name: ").lower()
    movies = movie_storage.get_movies()
    found = False
    for movie in movies:
        if query in movie['title'].lower():
            print(f"{Colors.YELLOW}Movie: '{movie['title']}' -> Rating: {movie['rating']}{Colors.RESET}")
            found = True
            print()
    if not found:
        print(f"{Colors.RED}No movie found matching '{query}'{Colors.RESET}")
        print()
    press_enter_to_continue()


def sort_by_rating():
    """
    Sort movies in descending order by rating and print them.
    """
    movies = movie_storage.get_movies()
    sorted_movies = movies[:]
    for i in range(len(sorted_movies)):
        for j in range(i + 1, len(sorted_movies)):
            try:
                if float(sorted_movies[j]['rating']) > float(sorted_movies[i]['rating']):
                    sorted_movies[i], sorted_movies[j] = sorted_movies[j], sorted_movies[i]
            except (ValueError, TypeError):
                continue
    for movie in sorted_movies:
        print(f"{movie['title']}: {movie['rating']}")
    print()
    press_enter_to_continue()


def filter_movies():
    """
    Filters movies based on minimum rating, start year, and end year.
    Prompts the user for input. Blank inputs are considered as no restriction.
    Displays filtered movies with title, year, and rating.
    """
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies available.")
        press_enter_to_continue()
        return

    # Minimum rating
    while True:
        min_rating_input = input("Enter minimum rating (leave blank for no minimum rating): ").strip()
        if min_rating_input == "":
            min_rating = None
            break
        try:
            min_rating = float(min_rating_input)
            if min_rating < 0 or min_rating > 10:
                print(f"{Colors.RED}Rating must be between 0 and 10.{Colors.RESET}")
                continue
            break
        except ValueError:
            print(f"{Colors.RED}Please enter a valid number for rating.{Colors.RESET}")

    # Start year
    while True:
        start_year_input = input("Enter start year (leave blank for no start year): ").strip()
        if start_year_input == "":
            start_year = None
            break
        try:
            start_year = int(start_year_input)
            break
        except ValueError:
            print(f"{Colors.RED}Please enter a valid number for start year.{Colors.RESET}")

    # End year
    while True:
        end_year_input = input("Enter end year (leave blank for no end year): ").strip()
        if end_year_input == "":
            end_year = None
            break
        try:
            end_year = int(end_year_input)
            break
        except ValueError:
            print(f"{Colors.RED}Please enter a valid number for end year.{Colors.RESET}")

    # Filter movies
    filtered = []
    for movie in movies:
        try:
            movie_rating = float(movie['rating'])
        except (ValueError, TypeError):
            continue
        movie_year = movie['year'] if isinstance(movie['year'], int) else None

        if min_rating is not None and movie_rating < min_rating:
            continue
        if start_year is not None and (movie_year is None or movie_year < start_year):
            continue
        if end_year is not None and (movie_year is None or movie_year > end_year):
            continue
        filtered.append(movie)

    # Display results
    if not filtered:
        print("No movies match your criteria.")
    else:
        print(f"{Colors.YELLOW}\nFiltered Movies: {Colors.RESET}")
        for movie in filtered:
            print(f"{movie['title']} ({movie['year']}): {movie['rating']}")
    print()
    press_enter_to_continue()


def main():
    print_title()
    while True:
        choice = print_menu()
        if choice == "0":
            exit_movie()
            break
        elif choice == "1":
            list_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            update_movie()
        elif choice == "5":
            stats()
        elif choice == "6":
            random_movie()
        elif choice == "7":
            search_movie()
        elif choice == "8":
            sort_by_rating()
        elif choice == "9":
            filter_movies()
        else:
            print(f"{Colors.RED}Invalid choice. Please enter 0-9.{Colors.RESET}")


if __name__ == "__main__":
    main()
