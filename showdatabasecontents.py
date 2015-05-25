import sqlite3


def main():
    dbname = "tamapro_database.db"
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    
    query = "SELECT * FROM tamas"
    c.execute(query)
    tamaList  = c.fetchall()
    print "c.execute(%s):" % query, tamaList
    


if __name__ == "__main__":
    main()
