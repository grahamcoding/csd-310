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
            s.supplier_name,
            sp.supply_name,
            sd.expected_delivery,
            sd.actual_delivery,
            DATEDIFF(sd.actual_delivery, sd.expected_delivery) AS days_late
        FROM supply_delivery sd
        JOIN supply sp ON sd.supply_id = sp.supply_id
        JOIN supplier s ON sp.supplier_id = s.supplier_id
        ORDER BY s.supplier_name, sd.expected_delivery;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print("\n--- Supplier Delivery Performance Report ---")

    current_supplier = None
    for row in results:
        supplier_name, supply_name, expected, actual, days_late = row

        if supplier_name != current_supplier:
            print(f"\nSupplier: {supplier_name}")
            current_supplier = supplier_name

        print(f"  - Supply: {supply_name:<8} | Expected: {expected} | Actual: {actual} | Days Late: {days_late}")

    cursor.close()
    db.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")