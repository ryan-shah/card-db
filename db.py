import sqlite3

cards = []
deck = []

# connect to sqlite databse
conn = sqlite3.connect('2024_Nov_29_17-37_backup.dlens')

# create a cursor object
cursor = conn.cursor()

# execute a query
q = """
select name
from cards INNER join (
	select data_cards._id, data_names.name
	from data_cards inner join data_names on data_cards.name = data_names._id
) as names on cards.card=names._id
where list not in (
	SELECT _id 
	from lists 
	WHERE category=2
)
--limit 10
"""

cursor.execute(q)

# fetch all the rows
result = cursor.fetchall()

# print the table names
for card in result:
    cards.append(card[0])

# close the connection
conn.close()

with open('decklist.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        deck.append(line.strip())

owned = open('owned.txt', 'w')
not_owned = open('not_owned.txt', 'w')

for card in deck:
    if card in cards:
        print(card)
        owned.write(card + '\n')
    else:
        not_owned.write("1 " + card + '\n')

owned.close()
not_owned.close()