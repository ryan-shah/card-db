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