import statsapi
import mysql.connector
from mysql.connector import Error
import pandas as pd

# id 136 for mariners
# team = statsapi.lookup_team('sea')
# print('The M\'s won %s games in 2022.' % sum(1 for x in statsapi.schedule(team=136,start_date='04/07/2022',end_date='10/31/2022') if x.get('winning_team','')=='Seattle Mariners'))

#print( statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',{'season':2022,'gameType':'W'})['people'] if x['fullName']=='Julio Rodriguez'), 'hitting', 'career') )
mariners_40_man = statsapi.roster(136).strip().split("\n")
player_1 = mariners_40_man[0].split()[2] + " " + mariners_40_man[0].split()[3]
player_stats_str = statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',{'season':2022,'gameType':'W'})['people'] if x['fullName']== player_1), 'hitting', 'career')
player_stats_arr = player_stats_str.split("Career Hitting")[1].strip().split("\n")

# player table: attributes: player name, number, position, age
# stats table: season, stats (GP, 1B, 2B, 3B, HR, BA, BB, hits, etc.)
# coaches table: name, role, years with team
# team table: name, owner, info (year founded, stadium, etc.)

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

connection = create_server_connection("localhost", "root", "bayview12")
create_database_query = "CREATE DATABASE BaseballWorld"
create_database(connection, create_database_query )