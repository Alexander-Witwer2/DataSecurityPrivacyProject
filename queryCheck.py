import mysql.connector
import hashlib

def calculate_checksum(data):
    # Calculate the SHA-256 checksum of the data
    sha256 = hashlib.sha256()
    sha256.update(data.encode('utf-8'))
    return sha256.hexdigest()

def verify_data_integrity(connection, table_name, column_name):
    query = f"SELECT age FROM maindata"

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    # Combine all values into a single string for checksum calculation
    concatenated_data = ''.join(str(row[0]) for row in result)

    # Calculate the checksum of the concatenated data
    original_checksum = calculate_checksum(concatenated_data)

    # Simulate the removal of one or more data items
    # (replace this with actual data manipulation in your use case)
    modified_data = concatenated_data.replace('72', '')

    # Calculate the checksum of the modified data
    modified_checksum = calculate_checksum(modified_data)

    # Compare the original and modified checksums
    return original_checksum == modified_checksum

try:
    # Replace these with your actual MySQL connection parameters
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="projectdb"
    )

    #Replace these with data you would like to simulate
    table_name = "maindata"
    column_name = "Age"

    if verify_data_integrity(connection, table_name, column_name):
        print("Data integrity is maintained.")
    else:
        print("Data integrity violation detected!")

finally:
    # Close the connection when done
    if connection.is_connected():
        connection.close()
