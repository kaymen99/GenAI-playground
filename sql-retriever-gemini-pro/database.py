import sqlite3

# Connect/create to local sqlite3 database
connection = sqlite3.connect("Database.db")

# Create cursor for interacting with DB
cursor = connection.cursor()

# Create example table
table = """
CREATE TABLE IF NOT EXISTS PLAYER (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    nationality TEXT NOT NULL,
    age INTEGER NOT NULL
)
"""

# Execute the table creation SQL command
cursor.execute(table)

# Choose some players for examples
players_data = [
    (1, 'Lionel Messi', 'Forward', 'Argentina', 34),
    (2, 'Cristiano Ronaldo', 'Forward', 'Portugal', 37),
    (3, 'Neymar Jr.', 'Forward', 'Brazil', 30),
    (4, 'Virgil van Dijk', 'Defender', 'Netherlands', 31),
    (5, 'Kevin De Bruyne', 'Midfielder', 'Belgium', 30),
    (6, 'Kylian Mbappé', 'Forward', 'France', 24)
]

# SQL statement to insert data
insert_query = "INSERT INTO PLAYER (id, name, position, nationality, age) VALUES (?, ?, ?, ?, ?)"

# Insert data into the table
cursor.executemany(insert_query, players_data)

# Commit changes 
connection.commit()

# Fetch all players
cursor.execute("SELECT * FROM PLAYER")
players = cursor.fetchall()

# Print the players
for player in players:
    print(player)

# Close connection
connection.close()
