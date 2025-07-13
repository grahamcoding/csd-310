# Daniel Graham, Aidan Jacoby, Stephanie Ramos
# Date: 7/13/25
# Display data from all tables in the winery database

""" import statements """
import mysql.connector  # to connect
from mysql.connector import errorcode

from dotenv import dotenv_values

#using our .env file
secrets = dotenv_values(".env")

# Database config
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}

# List of tables to query
tables = [
    "Department",
    "Employee",
    "Work_Hours",
    "Supplier",
    "Supply",
    "Supply_Delivery",
    "Wine",
    "Distributor",
    "Wine_Distribution",
    "Wine_Order",
    "Wine_Order_Item"
]

try:
    # Connect to the database
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    # Loop through tables and display contents
    for table in tables:
        print(f"\n-- DISPLAYING {table.upper()} RECORDS --")
        cursor.execute(f"SELECT * FROM {table};")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

        if rows:
            for row in rows:
                for col_name, value in zip(columns, row):
                    print(f"{col_name}: {value}")
                print()
        else:
            print("No records found.\n")

    input("\n\n  Press any key to continue...")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
    else:
        print(err)

finally:
    if 'db' in locals() and db.is_connected():
        db.close()
