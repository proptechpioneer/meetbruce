import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Check current property_condition values
cursor.execute("SELECT username, property_condition FROM application_user")
rows = cursor.fetchall()
print('Current property condition values:')
for row in rows:
    print(f'User: {row[0]}, condition: {repr(row[1])}')

# Update user 'as' property condition
cursor.execute("UPDATE application_user SET property_condition = 'Good' WHERE username = 'as'")
conn.commit()

# Check updated values
cursor.execute("SELECT username, property_condition FROM application_user WHERE username = 'as'")
row = cursor.fetchone()
print(f'Updated user as: condition = {repr(row[1])}')

conn.close()
print('Property condition updated!')