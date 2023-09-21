import sqlite3
from datetime import datetime
import pandas as pd

crash_data = pd.read_csv('Crash Statistics Victoria.csv')



# Create a table in the database if it doesn't exist
def create_table_if_not_exists(conn):
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS crash_data (
        OBJECTID INTEGER PRIMARY KEY,
        ACCIDENT_NO TEXT,
        ABS_CODE TEXT,
        ACCIDENT_STATUS TEXT,
        ACCIDENT_DATE DATE,
        ACCIDENT_TIME TIME,
        ALCOHOLTIME TEXT,
        ACCIDENT_TYPE TEXT,
        DAY_OF_WEEK TEXT,
        DCA_CODE TEXT,
        HIT_RUN_FLAG TEXT,
        LIGHT_CONDITION TEXT,
        POLICE_ATTEND TEXT,
        ROAD_GEOMETRY TEXT,
        SEVERITY TEXT,
        SPEED_ZONE TEXT,
        RUN_OFFROAD TEXT,
        NODE_ID INTEGER,
        LONGITUDE REAL,
        LATITUDE REAL,
        NODE_TYPE TEXT,
        LGA_NAME TEXT,
        REGION_NAME TEXT,
        VICGRID_X REAL,
        VICGRID_Y REAL,
        TOTAL_PERSONS INTEGER,
        INJ_OR_FATAL INTEGER,
        FATALITY INTEGER,
        SERIOUSINJURY INTEGER,
        OTHERINJURY INTEGER,
        NONINJURED INTEGER,
        MALES INTEGER,
        FEMALES INTEGER,
        BICYCLIST INTEGER,
        PASSENGER INTEGER,
        DRIVER INTEGER,
        PEDESTRIAN INTEGER,
        PILLION INTEGER,
        MOTORIST INTEGER,
        UNKNOWN INTEGER,
        PED_CYCLIST_5_12 INTEGER,
        PED_CYCLIST_13_18 INTEGER,
        OLD_PEDESTRIAN INTEGER,
        OLD_DRIVER INTEGER,
        YOUNG_DRIVER INTEGER,
        ALCOHOL_RELATED TEXT,
        UNLICENCSED TEXT,
        NO_OF_VEHICLES INTEGER,
        HEAVYVEHICLE INTEGER,
        PASSENGERVEHICLE INTEGER,
        MOTORCYCLE INTEGER,
        PUBLICVEHICLE INTEGER,
        DEG_URBAN_NAME TEXT,
        DEG_URBAN_ALL TEXT,
        LGA_NAME_ALL TEXT,
        REGION_NAME_ALL TEXT,
        SRNS TEXT,
        SRNS_ALL TEXT,
        RMA TEXT,
        RMA_ALL TEXT,
        DIVIDED TEXT,
        DIVIDED_ALL TEXT,
        STAT_DIV_NAME TEXT
    )
    ''')
    conn.commit()



# Search for records within a date range
def count_vsads_by_date_range(conn, start_date, end_date):
    cursor = conn.cursor()

    try:
        datetime.strptime(start_date, '%d/%m/%Y')
        datetime.strptime(end_date, '%d/%m/%Y')

    except ValueError:
        return "Invalid date Range"

    query = "SELECT COUNT(*) FROM crash_data WHERE ACCIDENT_DATE >= ? AND ACCIDENT_DATE <= ?"
    cursor.execute(query, (start_date, end_date))
    count = cursor.fetchone()[0]  # Retrieve the count value
    # cursor.close()
    return count

def calculate_average_by_hour_of_day(conn):
    cursor = conn.cursor()
    query = ("SELECT strftime('%H', ACCIDENT_TIME) AS hour, AVG(INJ_OR_FATAL) AS "
             "avg_injuries FROM crash_data GROUP BY hour")
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data

def filter_vsads_by_keywords(conn, keywords):
    cursor = conn.cursor()
    # Build a parameterized query for multiple keywords
    query = "SELECT * FROM crash_data WHERE ACCIDENT_TYPE IN ({})".format(",".join(["?"] * len(keywords)))
    cursor.execute(query, keywords)
    data = cursor.fetchall()
    cursor.close()
    return data

def filter_vsads_by_alcohol(conn, alcohol_related):
    cursor = conn.cursor()
    # A parameterized query for alcohol-related filter
    query = "SELECT * FROM crash_data WHERE ALCOHOL_RELATED = ?"
    cursor.execute(query, (alcohol_related,))
    data = cursor.fetchall()
    cursor.close()
    return data

if __name__ == "__main__":
    # Create a connection to the database
    with sqlite3.connect('crash_data.db') as conn:
        create_table_if_not_exists(conn)  # Create the table if it doesn't exist

        start_date = "4/10/2013"   # Use the correct date format '4/10/2013'
        end_date = "2/01/2016"     # Use the correct date format '2/01/2016'

        print("Start Date:", start_date)
        print("End Date:", end_date)

        count = count_vsads_by_date_range(conn, start_date, end_date)
        if isinstance(count, str):
            print(count)
        else:
            print("Number of accidents within date range:", count)

        """
        average_injuries_by_hour = calculate_average_by_hour_of_day(conn)
        print("Average injuries by hour of day:", average_injuries_by_hour)

        selected_keywords = ["Collision", "Rollover"]
        filtered_data = filter_vsads_by_keywords(conn, selected_keywords)
        print("Filtered data by keywords:", len(filtered_data), "records found.")

        alcohol_related_data = filter_vsads_by_alcohol(conn, "Yes")
        print("Alcohol-related data:", len(alcohol_related_data), "records found.")
        """
