import sqlite3
import os

def remove_duplicate_notes():
    """Function to remove duplicate notes from the database"""
    db_path = 'notas_fiscais.db'
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Fetch the list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            print(f"Processing table: {table_name}")

            # Find duplicate notes
            cursor.execute(f'''
                SELECT numero_nota, empresa, COUNT(*)
                FROM {table_name}
                GROUP BY numero_nota, empresa
                HAVING COUNT(*) > 1
            ''')
            duplicates = cursor.fetchall()

            for numero_nota, empresa, count in duplicates:
                print(f"Found duplicate: {numero_nota} for company {empresa} in table {table_name}")

                # Keep one record and delete the rest
                cursor.execute(f'''
                    DELETE FROM {table_name}
                    WHERE rowid NOT IN (
                        SELECT MIN(rowid)
                        FROM {table_name}
                        WHERE numero_nota = ? AND empresa = ?
                    ) AND numero_nota = ? AND empresa = ?
                ''', (numero_nota, empresa, numero_nota, empresa))

        conn.commit()
        conn.close()
        print("Duplicate notes removed successfully.")
    except Exception as e:
        print(f"An error occurred while removing duplicate notes: {e}")

if __name__ == "__main__":
    remove_duplicate_notes()
