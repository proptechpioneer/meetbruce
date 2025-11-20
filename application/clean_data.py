import os
import django
import sqlite3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

# Clean up the data directly in SQLite
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Update weekly_rent: remove £ symbol and convert to decimal
cursor.execute("UPDATE application_user SET weekly_rent = REPLACE(weekly_rent, '£', '') WHERE weekly_rent LIKE '%£%'")

# Fix empty weekly_rent values - set them to NULL
cursor.execute("UPDATE application_user SET weekly_rent = NULL WHERE weekly_rent = '' OR weekly_rent IS NULL")

# Update bedrooms: extract number from '2 bedrooms' -> 2
cursor.execute("UPDATE application_user SET bedrooms = '2' WHERE bedrooms = '2 bedrooms'")
cursor.execute("UPDATE application_user SET bedrooms = '1' WHERE bedrooms = '1 bedroom'")
cursor.execute("UPDATE application_user SET bedrooms = NULL WHERE bedrooms = ''")

# Update bathrooms: extract number from '1 bathroom' -> 1  
cursor.execute("UPDATE application_user SET bathrooms = '1' WHERE bathrooms = '1 bathroom'")
cursor.execute("UPDATE application_user SET bathrooms = '2' WHERE bathrooms = '2 bathrooms'")
cursor.execute("UPDATE application_user SET bathrooms = NULL WHERE bathrooms = ''")

# Update has_lounge: convert to boolean
cursor.execute("UPDATE application_user SET has_lounge = 1 WHERE has_lounge IN ('Yes', 'yes', 'True', 'true')")
cursor.execute("UPDATE application_user SET has_lounge = 0 WHERE has_lounge IN ('No', 'no', 'False', 'false', '')")

conn.commit()

# Check the results
cursor.execute('SELECT username, weekly_rent, bedrooms, bathrooms, has_lounge FROM application_user')
rows = cursor.fetchall()
print('Updated database values:')
for row in rows:
    print(f'User: {row[0]}, rent: {repr(row[1])}, beds: {repr(row[2])}, baths: {repr(row[3])}, lounge: {row[4]}')

conn.close()
print('Data cleaned successfully!')