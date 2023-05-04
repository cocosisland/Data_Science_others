

anime_table_create = ("""CREATE TABLE IF NOT EXISTS animes(
	anime_id SERIAL PRIMARY KEY,
	name VARCHAR NOT NULL,
	genres TEXT [],
    type VARCHAR,
    episodes INT,
    rating_mean REAL,
    members INT
)""")    
    


user_ratings_table_create = ("""CREATE TABLE IF NOT EXISTS user_ratings(
	user_id SERIAL PRIMARY KEY,
    anime_id SERIAL,
    rating_given INT
)""")




anime_tb = ['anime_id', 'name', 'genres', 'type', 'episodes', 'rating', 'members']
user_ratings = ['user_id', 'anime_id', 'rating']



# ['animes', 'user_ratings', 'flagged_users', 'best_rated_per_user',\
#                  'fav_genres_per_user', 'fav_type_per_user']



# =============================================================================
# def drop_tables(cur, conn, table_list):
#        
#     for tablename in table_list:
#         
#         query_drop = f'CREATE TABLE  IF NOT EXISTS {tablename} \
#             anime_id SERIAL CONSTRAINT anime_pk PRIMARY KEY,
# =============================================================================
            
            
            '




def create_tables():
    
    
    