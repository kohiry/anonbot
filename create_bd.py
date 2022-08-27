import sqlite3
from os import remove

if __name__ == '__main__':
    conn = sqlite3.connect('BASE.db', check_same_thread=False)
    cur = conn.cursor()
    if input("Удалить или создать? Del/Cre") == "Del":
        # созданию таблицу
        remove("BASE.db")
    else:
        # созданию таблицу
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
           userid INT PRIMARY KEY,
           status INT,
           black_list TEXT,
           coord TEXT);
        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS queue(
           userid INT PRIMARY KEY);
        """) # queue - типа очередь

    conn.commit()
    conn.close()
