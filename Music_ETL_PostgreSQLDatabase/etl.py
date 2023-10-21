import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from IPython.display import display


# Process songs files and insert records into the Postgres database
def process_song_file(cur, filepath):
   
    # open song file
    df = pd.DataFrame([pd.read_json(filepath, typ='series', convert_dates=False)])

    for value in df.values:
        num_songs, artist_id, artist_latitude, artist_longitude, artist_location, artist_name, song_id, title, duration, year = value

        # insert artist record
        artist_data = (artist_id, artist_name, artist_location, artist_latitude, artist_longitude)
        cur.execute(artist_table_insert, artist_data)

        # insert song record
        song_data = (song_id, title, artist_id, year, duration)
        '''if songs are inserted while having a Fk from a table that has no records yet:
        Disable Foreign key constraints, to add records into 'songs' table that has a Fk (artist_ID is Pk in 
        'artists' table and Fk in 'songs' table)'''
        #cur.execute("SET session_replication_role = 'replica';")
        cur.execute(song_table_insert, song_data)        
        # Re-enable Foreign key constraints
        #cur.execute("SET session_replication_role = 'origin';")
    
    print(f"Records inserted for file {filepath}")



# Process Event log files and insert records into the Postgres database
def process_log_file(cur, filepath):
    
    # open log file
    df = pd.read_json(filepath, convert_dates=False, lines=True, encoding='utf-8-sig')  #'encoding='utf-8-sig' for the display on console
    #pd.set_option('display.max_columns', None)
    #display(df.head(1))

    # filter by NextSong action
    df = df[df['page'] == "NextSong"].astype({'ts': 'datetime64[ns]'})

    timestamp = df['ts']
    time_hour = df['ts'].dt.hour
    time_day = df['ts'].dt.day
    time_week = df['ts'].dt.week
    time_month = df['ts'].dt.month
    time_year = df['ts'].dt.year
    time_weekday = df['ts'].dt.weekday

    time_data = (timestamp, time_hour, time_day, time_week, time_month, time_year, time_weekday)
    column_labels = ('timestamp', 'hour', 'day', 'week of year', 'month', 'year', 'weekday')

    data_dict = dict(zip(column_labels, time_data))
    time_df = pd.DataFrame(data_dict) 
    #print(time_df)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))


    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)


    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = ( row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)
      
        

# Load data from songs and event log files into Postgres database
def process_data(cur, conn, filepath, func):
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))



def main():
    
    #Driver function for loading songs and log data into Postgres database
    
    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname=musicdb user=postgres password=118218")
        #conn.autocommit = True
    except:
        print("Cannot connect to db")

    cur = conn.cursor()  # allows us to execute the SQL query once we’ve written it

    filepath = 'C:/Users/camib/Desktop/DATASCIENCE_PERSOPROJECTS/Music_ETL/data/song_data'
    process_data(cur, conn, filepath, process_song_file)
    conn.commit()
    
    filepath = 'C:/Users/camib/Desktop/DATASCIENCE_PERSOPROJECTS/Music_ETL/data/log_data'
    process_data(cur, conn, filepath, process_log_file)
    conn.commit()

    conn.close()


if __name__ == "__main__":
    main()
    print("\n\nFinished processing!!!\n\n")