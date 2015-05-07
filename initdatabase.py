import sqlite3
import sys

def main():
    if len(sys.argv) > 1:
        dbname = sys.argv[1]
    else:
        dbname = "tamapro_database.db"
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    
    with open("init_queries.sql") as f:
        for line in f:
            if not line:
                continue
            print "Executing line:", line.strip()
            c.execute(line)
            print "Done executing line.\n"
    conn.commit()
    
if __name__ == "__main__":
    main()
