import sqlite3

cards = []
deck = []

# connect to sqlite databse
conn = sqlite3.connect('2024_Dec_01_13-12_backup.dlens')

# create a cursor object
cursor = conn.cursor()

# execute a query
q = """
SELECT lst.name from (
	select names.name, sum(quantity) as quant
	from (cards INNER join (
		select data_cards._id, data_names.name
		from data_cards inner join data_names on data_cards.name = data_names._id
	 ) as names on cards.card=names._id) inner join lists on cards.list = lists._id
	where category = 1
	group by names.name
) as lst left outer join (select names.name, sum(quantity) as quant
	from (cards INNER join (
		select data_cards._id, data_names.name
		from data_cards inner join data_names on data_cards.name = data_names._id
	 ) as names on cards.card=names._id) inner join lists on cards.list = lists._id
	where category = 2
	group by names.name
) as dck on lst.name=dck.name
where dck.quant IS NULL OR lst.quant > dck.quant
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