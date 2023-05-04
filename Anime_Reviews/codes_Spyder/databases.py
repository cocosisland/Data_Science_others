import psycopg2
from creat_tables import 


# Create database while being connected to default database, then connect to the new one
def create_db():
    
    try:
        # connect to default database - because cannot drop a database on which we are already connected
        print("Connecting to default database...")
        conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=118218")
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        print("Connected.")
        
    except:
        print("Connection failed.")
        
    
    try:
        # create anime database
        cur.execute("DROP DATABASE IF EXISTS anime")    
        cur.execute("CREATE DATABASE anime WITH ENCODING 'utf8' TEMPLATE template0")
        print("anime database created.")

        # close connection to default database
        conn.close()
        print("Disconnect default database.")
        
    except:
        print("anime database creation failed.")
    
    
    try:
        # connect to anime database
        print("Connecting to anime database...")
        conn = psycopg2.connect("host=localhost dbname=anime user=postgres password=118218")
        cur = conn.cursor()
        print("Connected.")
        
        return cur, conn
        
    except:
        print("Connection failed.")    
    
    
    #return cur, conn



def drop_tables(cur, conn, table_list):

# =============================================================================
#     anime_table_drop = "DROP TABLE  IF EXISTS anime"
#     rating_table_drop = "DROP TABLE  IF EXISTS rating"
#     flagged_users_table_drop = "DROP TABLE  IF EXISTS flagged_users"
#     fav_animes_table_drop = "DROP TABLE  IF EXISTS fav_animes_per_user"
#     fav_genres_table_drop = "DROP TABLE  IF EXISTS fav_genres_per_user" 
#     fav_type_table_drop = "DROP TABLE  IF EXISTS fav_type_per_user"
# =============================================================================
       
    for tablename in table_list:
        
        query_drop = f'DROP TABLE  IF EXISTS {tablename}'
        
        cur.execute(query_drop)
        conn.commit()
        #print(tablename + ' Table dropped successfully')
    
    print("Tables dropped successfully")




def main():
    
    # connect to the database (anime)
    cur, conn = create_db()
    
    table_list = ['animes', 'user_ratings', 'flagged_users', 'best_rated_per_user',\
                  'fav_genres_per_user', 'fav_type_per_user']
        
        
    # drop tables if already exist
    drop_tables(cur, conn, table_list)


    # create tables    
    for query in table_list:
        cur.execute(query)
        conn.commit()
        
    anime_table_create = ("""CREATE TABLE IF NOT EXISTS anime(
    	anime_id SERIAL PRIMARY KEY,
    	name VARCHAR NOT NULL,
    	genres TEXT [],
        type VARCHAR,
        episodes INT,
        rating REAL,
        members INT
    )""") 
    cur.execute(anime_table_create)
    conn.commit()