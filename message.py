import sqlite3
import csv
import os

# Read the database path from an environment variable
db_path = os.getenv('IMESSAGE_DB_PATH')

if not db_path:
    raise ValueError("Environment variable IMESSAGE_DB_PATH not set")

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Replace CONTACT_NAME with the phone number or email of the contact as it appears in iMessage
contact_identifier = os.getenv('CONTACT_NAME')

query = """
SELECT 
    message.ROWID, 
    text, 
    is_from_me, 
    datetime(message.date/1000000000 + 978307200, 'unixepoch', 'localtime') as date 
FROM message 
JOIN handle ON message.handle_id = handle.ROWID 
WHERE handle.id = ?
ORDER BY message.date
"""

# Execute the query
cursor.execute(query, (contact_identifier,))

# Fetch messages
messages = cursor.fetchall()

# Specify the CSV file name
csv_file = 'imessage_export.csv'

# Write messages to a CSV file
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Writing the header
    writer.writerow(['RowID', 'Text', 'Is From Me', 'Date'])
    
    # Writing the message data
    for msg in messages:
        writer.writerow(msg)

# Close the cursor and connection
cursor.close()
conn.close()

print(f"Messages exported to {csv_file}")
