import sqlite3
import datetime
import pandas as pd

# Read the CSV file into a DataFrame
crash_data = pd.read_csv('Crash Statistics Victoria.csv')
crash_data['ACCIDENT_DATE'] = pd.to_datetime(crash_data['ACCIDENT_DATE'], format='%d/%m/%Y')
crash_data['ACCIDENT_TIME'] = pd.to_datetime(crash_data['ACCIDENT_TIME'], format='%H.%M.%S')
#     print(crash_data.head())

# Create a connection to the database
with sqlite3.connect('crash_data.db') as conn:
    # Create the table if it doesn't exist
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS crash_data (
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
    )''')
    conn.commit()

    # Insert data from the DataFrame into the database
    insertData = crash_data
    insertData.to_sql('crash_data', conn, if_exists='replace', index=False)

    start_date = datetime.datetime(2013, 10, 4)   # Use the correct date format '4/10/2013'
    end_date = datetime.datetime(2016, 1, 2)     # Use the correct date format '2/01/2016'

    print("Start Date:", start_date)
    print("End Date:", end_date)

    # Search for records within a date range
    def count_vsads_by_date_range(start_date, end_date):

        # try:
        #     # Convert start_date and end_date to the correct format 'yyyy-mm-dd'
        #     # start_date = datetime.date(start_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        #     # end_date = datetime.date(end_date, '%d/%m/%Y').strftime('%Y-%m-%d')
        # except ValueError:
        #     return "Invalid date Range"

        query = "SELECT COUNT(*) FROM crash_data WHERE ACCIDENT_DATE BETWEEN ? AND ?"
        cursor.execute(query, (start_date, end_date))
        count = cursor.fetchone()[0]  # Retrieve the count value

        return count

    def calculate_average_by_hour_of_day():
        query = ("SELECT strftime('%H', ACCIDENT_TIME) AS hour, AVG(INJ_OR_FATAL) AS "
                 "avg_injuries FROM crash_data GROUP BY hour")
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def filter_vsads_by_keywords(keywords):
        # Build a parameterized query for multiple keywords
        query = "SELECT * FROM crash_data WHERE ACCIDENT_TYPE IN ({})".format(",".join(["?"] * len(keywords)))
        cursor.execute(query, keywords)
        data = cursor.fetchall()
        cursor.close()
        return data

    def fetch_latitude():
        # Build a parameterized query for multiple keywords
        query = "SELECT Latitude FROM crash_data"
        cursor.execute(query)
        data = cursor.fetchall()
        # cursor.close()
        return data

    def fetch_longitude():
        # Build a parameterized query for multiple keywords
        query = "SELECT Latitude FROM crash_data"
        cursor.execute(query)
        data = cursor.fetchall()
        # cursor.close()
        return data

    def filter_vsads_by_alcohol(alcohol_related):
        # A parameterized query for alcohol-related filter
        query = "SELECT * FROM crash_data WHERE ALCOHOL_RELATED = ?"
        cursor.execute(query, (alcohol_related,))
        data = cursor.fetchall()
        cursor.close()
        return data

    if __name__ == "__main__":
        """
        ----------------------Testing Functions----------------------
        # Check the number of rows in the DataFrame
        print("Number of rows in crash_data DataFrame:", len(crash_data))

        # Check the number of rows in the crash_data table in the database
        cursor.execute("SELECT COUNT(*) FROM crash_data")
        row_count = cursor.fetchone()[0]
        print("Number of rows in crash_data table:", row_count)

        count = count_vsads_by_date_range(conn, start_date, end_date)
        if isinstance(count, str):
            print(count)
        else:
            print("Number of accidents within date range:", count)

        average_injuries_by_hour = calculate_average_by_hour_of_day(conn)
        print("Average injuries by hour of day:", average_injuries_by_hour)

        selected_keywords = ["Collision with vehicle", "Struck animal"]
        filtered_data = filter_vsads_by_keywords(conn, selected_keywords)
        print("Filtered data by keywords:", len(filtered_data), "records found.")


        alcohol_related_data = filter_vsads_by_alcohol(conn, False)
        print("Alcohol-related data:", len(alcohol_related_data), "records found.")
        """
