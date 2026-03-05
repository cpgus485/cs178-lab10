# name: YOUR NAME HERE
# date:
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 0 (out of 5) -- if I don't change this, I agree to get 0 points.

import boto3

# -------------------------------------------------------
# Configuration — update REGION if your table is elsewhere
# -------------------------------------------------------
REGION = "us-east-1"
TABLE_NAME = "Movies"

def get_table():
    """Return a reference to the DynamoDB Movies table."""
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)

def create_movie():
    table = get_table()

    movie_title = input("Title: ")
    movie_genre = input("Genre: ")
    movie_year = input("Year: ")
    ratings_input = input("Ratings (space separated): ")
    movie_ratings = [int(r) for r in ratings_input.split()]
    movie = {'Title' : movie_title, 'Genre' : movie_genre, 'Ratings' : movie_ratings, 'Year' : movie_year}
    table.put_item(Item = movie)
    print("creating a movie")

def print_movie(movie):
    print("Title: ", movie["Title"], end=" ")
    print("Ratings: ", end=" ")
    for rating in movie["Ratings"]:
        print(rating, end=" ")
    print("Year: ", movie["Year"], end=" ")
    print("Genre: ", movie["Genre"], end=" ")
    print()
    
def print_all_movies():
    """Scan the entire Movies table and print each item."""
    table = get_table()
    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No movies found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} movie(s):\n")
    for movie in items:
        print_movie(movie)

def update_rating():
    try:
        table=get_table()
        title = input("What is the movie title? ")
        rating = int(input("What is the rating (integer): "))
        table.update_item(
        Key={"Title": title},
        UpdateExpression="SET Ratings = list_append(Ratings, :r)",
        ExpressionAttributeValues={':r': [rating]}
        )
    except:
        print("error in updating movie rating")


def delete_movie():
    """
    Prompt user for a Movie Title.
    Delete that item from the database.
    """
    print("deleting movie")

def query_movie():
    """
    Prompt user for a Movie Title.
    Print out the average of all ratings in the movie's Ratings list.
    """
    print("query movie")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to QUERY a movie's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
