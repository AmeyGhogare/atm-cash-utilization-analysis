import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

load_dotenv(override=True)


def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            port=3306
        )

        print("Connected to MySQL successfully.")

        return connection

    except mysql.connector.Error as error:
        print("Error while connecting to MySQL:")
        print(error)

        return None


def create_table(connection):

    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS atm_data (
        ATM_ID VARCHAR(20),
        Date DATE,
        Day_of_Week VARCHAR(20),
        Time_of_Day VARCHAR(30),

        Total_Withdrawals INT,
        Total_Deposits INT,

        Location_Type VARCHAR(50),

        Holiday_Flag TINYINT,
        Special_Event_Flag TINYINT,

        Previous_Day_Cash_Level INT,

        Weather_Condition VARCHAR(50),

        Nearby_Competitor_ATMs INT,

        Cash_Demand_Next_Day INT,

        Year INT,
        Month INT,
        Month_Name VARCHAR(20),
        Quarter INT,

        Net_Cash_Flow INT,
        Cash_Utilization_Rate DECIMAL(10,2),

        Cash_Risk VARCHAR(20)
    )
    """

    cursor.execute(create_table_query)

    connection.commit()

    cursor.close()

    print("ATM table created successfully.")


def clear_table(connection):

    cursor = connection.cursor()

    cursor.execute("TRUNCATE TABLE atm_data")

    connection.commit()

    cursor.close()

    print("Existing ATM records cleared successfully.")


def load_data_to_mysql(connection):

    file_path = "data/processed/atm_cleaned.csv"

    df = pd.read_csv(file_path)

    cursor = connection.cursor()

    insert_query = """
    INSERT INTO atm_data (
        ATM_ID,
        Date,
        Day_of_Week,
        Time_of_Day,
        Total_Withdrawals,
        Total_Deposits,
        Location_Type,
        Holiday_Flag,
        Special_Event_Flag,
        Previous_Day_Cash_Level,
        Weather_Condition,
        Nearby_Competitor_ATMs,
        Cash_Demand_Next_Day,
        Year,
        Month,
        Month_Name,
        Quarter,
        Net_Cash_Flow,
        Cash_Utilization_Rate,
        Cash_Risk
    )
    VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s
    )
    """

    records = []

    for _, row in df.iterrows():

        values = (
            row["ATM_ID"],
            row["Date"],
            row["Day_of_Week"],
            row["Time_of_Day"],
            int(row["Total_Withdrawals"]),
            int(row["Total_Deposits"]),
            row["Location_Type"],
            int(row["Holiday_Flag"]),
            int(row["Special_Event_Flag"]),
            int(row["Previous_Day_Cash_Level"]),
            row["Weather_Condition"],
            int(row["Nearby_Competitor_ATMs"]),
            int(row["Cash_Demand_Next_Day"]),
            int(row["Year"]),
            int(row["Month"]),
            row["Month_Name"],
            int(row["Quarter"]),
            int(row["Net_Cash_Flow"]),
            float(row["Cash_Utilization_Rate"]),
            row["Cash_Risk"]
        )

        records.append(values)

    cursor.executemany(insert_query, records)

    connection.commit()

    print(f"{cursor.rowcount} records inserted successfully.")

    cursor.close()


def verify_data(connection):

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM atm_data")

    total_records = cursor.fetchone()[0]

    print("Total records in MySQL:", total_records)

    cursor.close()


def close_connection(connection):

    if connection.is_connected():

        connection.close()

        print("MySQL connection closed.")


if __name__ == "__main__":

    connection = connect_to_mysql()

    if connection is not None:

        create_table(connection)

        clear_table(connection)

        load_data_to_mysql(connection)

        verify_data(connection)

        close_connection(connection)

    else:

        print("MySQL connection failed. Data loading skipped.")