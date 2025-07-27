import mysql.connector
from dotenv import dotenv_values

secrets = dotenv_values(".env")

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"]
}
          
try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    query = """
        SELECT 
            w.wine_name,
            d.distributor_name,
            SUM(wd.quantity) AS total_distributed
        FROM wine_distribution wd
        JOIN wine w ON wd.wine_id = w.wine_id
        JOIN distributor d ON wd.distributor_id = d.distributor_id
        GROUP BY w.wine_name, d.distributor_name
        ORDER BY w.wine_name, total_distributed DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print("\n--- Wine Sales & Distribution Overview ---")

    current_wine = None
    for row in results:
        wine_name, distributor_name, total = row

        if wine_name != current_wine:
            print(f"\nWine: {wine_name}")
            current_wine = wine_name

        print(f"  - Distributor: {distributor_name:<20} | Quantity: {total}")

    cursor.close()
    db.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")