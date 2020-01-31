
import os
import sqlite3

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "rpg_db.sqlite3")
#conn = sqlite3.connect('rpg_db.sqlite3')

conn = sqlite3.connect(DB_FILEPATH) #instantiate connection
# h/t: https://kite.com/python/examples/3884/sqlite3-use-a-row-factory-to-access-values-by-column-name

conn.row_factory = sqlite3.Row

curs = conn.cursor() #open cursor

query = """SELECT count(distinct character_id) as character_amount FROM charactercreator_character;"""
#curs.execute(query)

results = curs.execute(query).fetchone()

breakpoint()

####1.2 How many characters per sub class

query1_2 = """
SELECT
  subquery1.char_type
  ,count(distinct subquery1.character_id) as char_count
from (
    -- row per character (302 total)
    select 
      ch.character_id
      ,ch.name
      ,CASE 
      WHEN cl.character_ptr_id is not null THEN "cleric"
      WHEN f.character_ptr_id is not null THEN "fighter"
      WHEN n.mage_ptr_id is not null THEN "mage-necro"
      WHEN m.character_ptr_id is not null THEN "mage"
      WHEN th.character_ptr_id is not null THEN "thief"
      ELSE "todo"
      END as char_type
    from charactercreator_character as ch
    left join charactercreator_cleric as cl on ch.character_id = cl.character_ptr_id
    left join charactercreator_fighter as f on ch.character_id = f.character_ptr_id
    left join charactercreator_mage as m on ch.character_id = m.character_ptr_id
    left join charactercreator_thief as th on ch.character_id = th.character_ptr_id
    left join charactercreator_necromancer as n on m.character_ptr_id = n.mage_ptr_id
) subquery1
group by subquery1.char_type;"""

results12 = curs.execute(query1_2).fetchall()

breakpoint()


query1_3 = "SELECT count(distinct item_id) as item_total FROM armory_item;"

results13 = curs.execute(query1_3).fetchone()


breakpoint()


query1_4 = "SELECT count(distinct item_ptr_id) as item_weapon_total FROM armory_weapon;"

results14 = curs.execute(query1_3).fetchone()
#print(f'Question 1.4 How many items are weapons? ', results14)
#print(f'The number that are not weapons are', results13[0]-results14[0])

breakpoint()

query1_5 = "SELECT character_id ,count(item_id) as item_counts FROM charactercreator_character_inventory group by character_id limit 20;"
results15 = curs.execute(query1_5[20]).fetchall()


breakpoint()

query1_6 = "select cc.name,count(cc.name) as weapons from charactercreator_character as cc, armory_item as ai, charactercreator_character_inventory as cci, armory_weapon as aw where ai.item_id = cci.id and cc.character_id = cci.character_id and ai.item_id = aw.item_ptr_id group by cc.character_id order by cc.name limit 20;"
results16 = curs.execute(query1_6).fetchall()


breakpoint()

query1_7 = "select cast(count(distinct inv.id) as float) / count(distinct inv.character_id) as item_per_char from charactercreator_character_inventory inv join armory_item ai on ai.item_id = inv.item_id;"
results17 = curs.execute(query1_7).fetchall()


breakpoint()

query1_8 = "select cast(count(distinct inv.id) as float) / count(distinct inv.character_id) as weapons_per_char from charactercreator_character_inventory inv join armory_weapon aw on aw.item_ptr_id = inv.item_id;"
results18 = curs.execute(query1_8).fetchall()


breakpoint()



# ### 1.1 How many characters are there
# SELECT count(distinct character_id) as character_amount
# FROM charactercreator_character
# ###returns 302


# ### 1.2 How many of each subclass
# SELECT count(distinct character_ptr_id) as character_subclass_amount
# FROM charactercreator_cleric
# #returns 75 for cleric

# SELECT count(distinct character_ptr_id) as character_subclass_amount
# FROM charactercreator_fighter
# #returns 68 for fighter

# SELECT count(distinct character_ptr_id) as character_subclass_amount
# FROM charactercreator_mage
# #returns 108 for mage

# SELECT count(distinct character_ptr_id) as character_subclass_amount
# FROM charactercreator_thief
# #returns 51 for thief

# ### this totals 302 so thats a good check

select
  subquery1.char_type
  ,count(distinct subquery1.character_id) as char_count
from (
    -- row per character (302 total)
    select 
      ch.character_id
      ,ch.name
      --,cl.*
      --,f.*
      --,m.*
      --,th.*
      -- ,if(cl.character_ptr_id is not null, "cleric", "todo") as char_type
      ,CASE 
      WHEN cl.character_ptr_id is not null THEN "cleric"
      WHEN f.character_ptr_id is not null THEN "fighter"
      WHEN n.mage_ptr_id is not null THEN "mage-necro"
      WHEN m.character_ptr_id is not null THEN "mage"
      WHEN th.character_ptr_id is not null THEN "thief"
      ELSE "todo"
      END as char_type
    from charactercreator_character as ch
    left join charactercreator_cleric as cl on ch.character_id = cl.character_ptr_id
    left join charactercreator_fighter as f on ch.character_id = f.character_ptr_id
    left join charactercreator_mage as m on ch.character_id = m.character_ptr_id
    left join charactercreator_thief as th on ch.character_id = th.character_ptr_id
    -- left join charactercreator_necromancer as n on ch.character_id = n.character_ptr_id
    left join charactercreator_necromancer as n on m.character_ptr_id = n.mage_ptr_id
) subquery1
group by subquery1.char_type







# ### 1.3 How many total items
# SELECT count(distinct item_id) as item_total
# FROM armory_item
# #returns 174 for items


# ###1.4 How many of the Items are weapons? How many are not?
# SELECT count(distinct item_ptr_id) as item_weapon_total
# FROM armory_weapon
# #returns 37 for weapons
# #that means 174-34 = 140 non weapons in items

###1.5 How many Items does each character have? (Return first 20 rows)
# SELECT
# 	character_id
# 	,count(item_id) as item_counts
# FROM charactercreator_character_inventory
# group by character_id
# limit 20


# ###1.6 How many Weapons does each character have? (Return first 20 rows)
# select 
# 	cc.name
# 	,count(cc.name) as weapons 
# from charactercreator_character as cc, armory_item as ai, charactercreator_character_inventory as cci, armory_weapon as aw 
# where ai.item_id = cci.id and cc.character_id = cci.character_id and ai.item_id = aw.item_ptr_id 
# group by cc.character_id 
# order by cc.name
# limit 20



# ###1.7 On average, how many Items does each Character have?
# select
#   -- inv.id
#   -- ,inv.character_id
#   -- ,inv.item_id as weapon_id
#   cast(count(distinct inv.id) as float) / count(distinct inv.character_id) as item_per_char
# from charactercreator_character_inventory inv
# join armory_item ai on ai.item_id = inv.item_id


# ###1.8 On average, how many Weapons does each character have?
# SELECT AVG(item_count)
# FROM(SELECT COUNT(item_id) AS item_count
# FROM charactercreator_character_inventory
# INNER JOIN armory_weapon
# ON item_id = item_ptr_id
# GROUP BY character_id);



# --On average how many weapons does each character have?
# -- how many weapons per character? (not including characters that don't have weapons)
# select
#   -- inv.id
#   -- ,inv.character_id
#   -- ,inv.item_id as weapon_id
#   cast(count(distinct inv.id) as float) / count(distinct inv.character_id) as weapons_per_char
# from charactercreator_character_inventory inv
# join armory_weapon aw on aw.item_ptr_id = inv.item_id
