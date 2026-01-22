import sqlite3
import csv
import pandas as pd

#-------- Creamos base de datos ----------
conn = sqlite3.connect("database/ventas.db")#crea o abre
cursor = conn.cursor()#aplica

cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    producto TEXT,
    categoria TEXT,
    cantidad INTEGER,
    precio REAL,
    empleado TEXT
)
""")

conn.commit()
conn.close()
print("Base de datos creada correctamente")

#--------Cargar datos desde csv ---------------
conn = sqlite3.connect("database/ventas.db")
cursor = conn.cursor()
with open("data/ventas.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute("""
        INSERT INTO ventas (fecha, producto, categoria, cantidad, precio, empleado)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row["fecha"],
            row["producto"],
            row["categoria"],
            int(row["cantidad"]),
            float(row["precio"]),
            row["empleado"]
        ))

conn.commit()
conn.close()

print("Datos cargados correctamente")

#---------Reporte---------------------------
conn = sqlite3.connect("database/ventas.db")
cursor = conn.cursor()
query = """
SELECT producto,
        SUM(cantidad * precio) AS total_ventas
FROM ventas
GROUP BY producto
ORDER BY total_ventas DESC
"""

df = pd.read_sql_query(query, conn)
print(df)

conn.close()