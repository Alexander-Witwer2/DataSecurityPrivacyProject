from cryptography.fernet import Fernet
import mysql.connector

def generate_key():
    return Fernet.generate_key()

def initialize_cipher(key):
    return Fernet(key)

def encrypt_data(cipher, data):
    if isinstance(data, int):
        data = str(data)
    data_bytes = str(data).encode('utf-8')
    return cipher.encrypt(data_bytes)


def decrypt_data(cipher, encrypted_data):
    if isinstance(encrypted_data, (bytes, str)):
        try:
            if isinstance(encrypted_data, str):
                encrypted_data = encrypted_data.encode('utf-8')

            decrypted_data_bytes = cipher.decrypt(encrypted_data)
            decrypted_data = decrypted_data_bytes.decode('utf-8')

            # Try converting to int if it looks like an integer
            if decrypted_data.isdigit():
                decrypted_data = int(decrypted_data)

            return decrypted_data
        except Exception as e:
            print(f"Error decrypting data: {e}")
            return None
    else:
        raise TypeError("Encrypted data must be bytes or str")



def encrypt_sensitive_data(connection, table_name, sensitive_columns):
    key = generate_key()
    cipher_suite = initialize_cipher(key)

    # Update the table with encrypted sensitive attributes
    set_placeholders = ', '.join([f'`{col}` = %s' for col in sensitive_columns])
    update_query = f"UPDATE {table_name} SET {set_placeholders}"

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()

        for row in result:
            updated_values = []
            for col in row:
                if col in sensitive_columns:
                    updated_values.append(encrypt_data(cipher_suite, col))
                else:
                    updated_values.append(col)

            # Use execute() with a tuple containing the updated values
            cursor.execute(update_query, tuple(updated_values[:len(sensitive_columns)]))  # Use only the relevant values

    connection.commit()









def decrypt_sensitive_data(connection, table_name, sensitive_columns):
    key = generate_key()
    cipher_suite = initialize_cipher(key)

    # Select all data from the specified columns
    select_query = f"SELECT * FROM {table_name}"

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        result = cursor.fetchall()

        # Print column names
        column_names = [desc[0] for desc in cursor.description]
        print("Column Names:", column_names)

        for row in result:
            decrypted_data = [decrypt_data(cipher_suite, col) if col in sensitive_columns else col for col in row]
            print("Decrypted Data Before Update:", decrypted_data)

    connection.commit()


# Example usage
try:
    # Replace these with your actual MySQL connection parameters
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="projectdb"
    )

    table_name = "projectdatabase"
    sensitive_columns = ["gender", "age"]

    # Encrypt sensitive data in the specified columns
    encrypt_sensitive_data(connection, table_name, sensitive_columns)
    

    # Retrieve and decrypt sensitive data from the specified columns
    decrypt_sensitive_data(connection, table_name, sensitive_columns)

finally:
    if connection.is_connected():
        connection.close()
