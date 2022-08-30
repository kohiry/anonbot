import sqlite3

conn = sqlite3.connect('BASE.db', check_same_thread=False)
cur = conn.cursor()
cur.execute(f"SELECT userid FROM users")
one_result = tuple(cur.fetchall())
conn.commit()
print(one_result)
with open("spam.txt", "r") as f:
    pair_id_spambool = tuple(f.readlines())
    print(pair_id_spambool)

with open("spam.txt", "w") as f:
    for i in one_result:
        if i[0] not in pair_id_spambool:
            f.write(str(i[0])+'\n')


#нужно добавлять юзеро по одному
