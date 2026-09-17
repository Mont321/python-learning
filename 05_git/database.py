import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER
    )
""")

# Добавляем поле city (если его нет)
try:
    cursor.execute("ALTER TABLE users ADD COLUMN city TEXT")
except sqlite3.OperationalError:
    pass

# Вставка данных (только если их нет)
for name, age in [("Иван", 25), ("Мария", 30), ("Петр", 22)]:
    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))

conn.commit()

# Обновляем города
cursor.execute("UPDATE users SET city = ? WHERE name = ?", ("Москва", "Иван"))
cursor.execute("UPDATE users SET city = ? WHERE name = ?", ("Санкт-Петербург", "Мария"))
cursor.execute("UPDATE users SET city = ? WHERE name = ?", ("Ростов-на-Дону", "Петр"))
conn.commit()

# 1. Все пользователи
print("Все пользователи:")
cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Имя: {row[1]}, Возраст: {row[2]}, Город: {row[3]}")

# 2. WHERE
print("\nИз Москвы:")
cursor.execute("SELECT * FROM users WHERE city = ?", ("Москва",))
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Имя: {row[1]}, Возраст: {row[2]}, Город: {row[3]}")

# 3. ORDER BY
print("\nСортировка по городу:")
cursor.execute("SELECT * FROM users ORDER BY city")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Имя: {row[1]}, Возраст: {row[2]}, Город: {row[3]}")

# 4. UPDATE
cursor.execute("UPDATE users SET age = ? WHERE name = ?", (26, "Иван"))
conn.commit()

# 5. DELETE
cursor.execute("DELETE FROM users WHERE name = ?", ("Петр",))
conn.commit()

# 6. Финальный SELECT
print("\nПосле удаления Петра:")
cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Имя: {row[1]}, Возраст: {row[2]}, Город: {row[3]}")




cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        product TEXT,
        total REAL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
""")

cursor.execute("INSERT INTO orders (user_id, product, total) VALUES (?, ?, ?)", (1, "Книга", 500))
cursor.execute("INSERT INTO orders (user_id, product, total) VALUES (?, ?, ?)", (2, "Вейп", 2300))
cursor.execute("INSERT INTO orders (user_id, product, total) VALUES (?, ?, ?)", (3, "Самокат", 10000))

conn.commit()

print("\nЗаказы пользователей:")
cursor.execute("""SELECT users.name, orders.product, orders.total FROM users JOIN orders ON users.id = orders.user_id""")
for row in cursor.fetchall():
    print(f"Пользователь: {row[0]}, Товар: {row[1]}, Сумма: {row[2]}")


print("\nВсе пользователи (после всех операций):")
cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Имя: {row[1]}, Возраст: {row[2]}, Город: {row[3]}")

conn.close()
