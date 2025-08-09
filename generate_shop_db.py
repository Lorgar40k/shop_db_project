import psycopg2
from faker import Faker
import random

conn = psycopg2.connect(
    dbname="shop_db",
    user="shop_user",
    password="shop_pass",
    host="localhost",
    port="5433"
)


cursor = conn.cursor()

fake = Faker()

# Создание таблиц
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price NUMERIC(10, 2)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER
)
""")

# Заполнение таблиц
for _ in range(20):
    cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (fake.word(), round(random.uniform(10, 300), 2)))

for _ in range(10):
    cursor.execute("INSERT INTO customers (name, email) VALUES (%s, %s)", (fake.name(), fake.email()))

for _ in range(30):
    cursor.execute(
        "INSERT INTO orders (customer_id, product_id, quantity) VALUES (%s, %s, %s)",
        (random.randint(1, 10), random.randint(1, 20), random.randint(1, 5))
    )

conn.commit()
cursor.close()
conn.close()

print("Данные успешно сгенерированы в PostgreSQL!")
