import sqlite3 as sql
with open("error.txt",'r') as r,\
    sql.connect("website.cdb") as connection:
    cur = connection.cursor()
    for line in r.readlines():
        cur.execute('DELETE FROM card_info WHERE name=?',(line.split()[0],))
        print(cur.rowcount)
    connection.commit()