# name: Clayton Gustafson
# date: 3/5/2026
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# part 2: Music table

import boto3

# -------------------------------------------------------
# Configuration — update REGION if your table is elsewhere
# -------------------------------------------------------
REGION = "us-east-1"
TABLE_NAME = "Music"

def get_table():
    """Return a reference to the DynamoDB Music table."""
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)

def create_song():
    table = get_table()

    song_title = input("Title: ")
    song_artist = input("Artist: ")
    song_length = input("Seconds: ")
    song = {"Title" : song_title, "Artist" : song_artist, "Seconds" : song_length}
    table.put_item(Item = song)
    print("creating a song")

def print_music(music):
    title = music.get("Title", "Unknown Title")
    artist = music.get("Artist", "Unknown Year")
    seconds = music.get("Seconds", "No ratings")
    
    print(f"  Title             : {title}")
    print(f"  Artist           : {artist}")
    print(f"  Duration (sec)    : {seconds}")
    
def print_all_songs():
    """Scan the entire Music table and print each item."""
    table = get_table()
    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No songs found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} songs(s):\n")
    for song in items:
        print_music(song)

def update_length():
    try:
        table=get_table()
        title = input("What is the song title? ")
        length = int(input("What is the length (in seconds): "))
        table.update_item(
        Key={"Title": title},
        UpdateExpression="SET Seconds = :sec",
        ExpressionAttributeValues={':sec' : length}
        )
    except:
        print("error in updatings song length")


def delete_song():
    table=get_table()
    title = input("What is the song title? ")
    table.delete_item(
        Key={
            "Title":title
        }
    )
    print("deleting song")

def query_song():
    table=get_table()
    title = input("What is the song title? ")
    response = table.get_item(Key={"Title": title})

    if "Item" not in response:
        print("song not found")
        return
    
    song = response.get("Item")

    if "Seconds" not in song:
        print("song is not recorded")

    length = song["Seconds"]  # a normal Python list of numbers
    print("Length of song: ", length, "seconds")
    
def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new song")
    print("Press R: to READ all songs")
    print("Press U: to UPDATE a song (change length)")
    print("Press D: to DELETE a song")
    print("Press Q: to QUERY a song's length")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_song()
        elif input_char.upper() == "R":
            print_all_songs()
        elif input_char.upper() == "U":
            update_length()
        elif input_char.upper() == "D":
            delete_song()
        elif input_char.upper() == "Q":
            query_song()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
