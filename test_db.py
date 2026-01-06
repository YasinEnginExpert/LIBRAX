import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="Postgres123",
    database="librax_db"
)

print("CONNECTED")
conn.close()
