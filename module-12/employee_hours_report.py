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
            e.first_name,
            e.last_name,
            d.department_name,
            SUM(w.hours_worked) AS total_hours
        FROM work_hours w
        JOIN employee e ON w.employee_id = e.employee_id
        JOIN department d ON e.department_id = d.department_id
        WHERE w.year = 2024
        GROUP BY e.employee_id
        ORDER BY total_hours DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    print("\n--- Employee Work Hours for 2024 ---")
    for row in results:
        first, last, dept, total = row
        print(f"{first} {last:<12} | Dept: {dept:<15} | Total Hours: {total}")

    cursor.close()
    db.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")