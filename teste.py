import sqlite3

db_file = "C:/Users/pinix/OneDrive/Ambiente de Trabalho/Solent/Year 1/2 Semester/" \
          "COM417 - Databases/Assessment/Assessment.db"
db = sqlite3.connect(db_file)
cursor = db.cursor()
category = "SELECT category_id, category_description\
                FROM categories\
                ORDER BY category_description Asc"
cursor.execute(category)
all_rows = cursor.fetchall()
print(all_rows[2-1][0])

db.close()
