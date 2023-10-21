import psycopg2
from sql_queries import create_table_queries, drop_table_queries

    
# Establish database connection and return the connection and cursor references
def create_database():

    # connect to default database (because cannot drop a database on which we're connected. Need to connect to another database first)
    conn = psycopg2.connect("host=127.0.0.1 dbname=postgres user=postgres password=118218")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS musicdb")
    cur.execute("CREATE DATABASE musicdb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()    
    
    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=musicdb user=postgres password=118218")
    cur = conn.cursor()
    
    return cur, conn


# Runs all the drop table queries defined in sql_queries.py
def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


# Runs all the create table queries defined in sql_queries.py
def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()



def main():

    cur, conn = create_database()

    drop_tables(cur, conn)
    print("Table dropped successfully!!")

    create_tables(cur, conn)
    print("Table created successfully!!")

    conn.close()
    "If need to execute things on Jupyter at this point, need to connect on the sparkifydb from Jupyter as well"


if __name__ == "__main__":
    main()