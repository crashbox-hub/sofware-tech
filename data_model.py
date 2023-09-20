import sqlite3
from datetime import datetime


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
def search_vsads_by_date_range(conn, start_date, end_date):
    cursor = conn.cursor()

    try:
        datetime.strptime(start_date, '%d-%m-%Y')
        datetime.strptime(end_date, '%d-%m-%Y')
    except ValueError:
        return "Invalid date Range"

    query = "SELECT * FROM crash_data WHERE ACCIDENT_DATE BETWEEN ? AND ?"
    cursor.execute(query, (start_date, end_date))
    data = cursor.fetchall()
    return data


def calculate_average_by_hour_of_day(conn):
    cursor = conn.cursor()
    query = "SELECT strftime('%H', ACCIDENT_TIME) AS hour, AVG(INJ_OR_FATAL) AS avg_injuries FROM crash_data GROUP BY hour"
    cursor.execute(query)
    data = cursor.fetchall()
    return data


def filter_vsads_by_keywords(conn, keywords):
    cursor = conn.cursor()
    # Build a parameterized query for multiple keywords
    query = "SELECT * FROM crash_data WHERE ACCIDENT_TYPE IN ({})".format(",".join(["?"] * len(keywords)))
    cursor.execute(query, keywords)
    data = cursor.fetchall()
    return data


def filter_vsads_by_alcohol(conn, alcohol_related):
    cursor = conn.cursor()
    # Build a parameterized query for alcohol-related filter
    query = "SELECT * FROM crash_data WHERE ALCOHOL_RELATED = ?"
    cursor.execute(query, (alcohol_related,))
    data = cursor.fetchall()
    return data


if __name__ == "__main__":
    # Create a connection to the database
    with sqlite3.connect('vsads.db') as conn:
        create_table_if_not_exists(conn)

        # Testing functionality of DB of VSADS

        start_date = "4/10/2013"   # Saying invalid date range, Check tghis in function!!!
        end_date = "2/01/2016"
        # Print results for test
        result = search_vsads_by_date_range(conn, start_date, end_date)
        if isinstance(result, str):
            print(result)
        else:
            print("Data within date range:", len(result), "records found.")

        # Print results for test
        average_injuries_by_hour = calculate_average_by_hour_of_day(conn)
        print("Average injuries by hour of day:", average_injuries_by_hour)

        # Print results for test
        selected_keywords = ["Collision", "Rollover"]
        filtered_data = filter_vsads_by_keywords(conn, selected_keywords)
        print("Filtered data by keywords:", len(filtered_data), "records found.")

        # Print results for test
        alcohol_related_data = filter_vsads_by_alcohol(conn, "Yes")
        print("Alcohol-related data:", len(alcohol_related_data), "records found.")
