import sqlite3
import os

db_path = 'agent_memory.db'

if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Delete entries starting with "Error"
        cursor.execute("DELETE FROM solutions WHERE solution LIKE 'Error%'")
        deleted_count = cursor.rowcount
        
        # Also delete entries that are just "Maximum iterations reached..."
        cursor.execute("DELETE FROM solutions WHERE solution LIKE 'Maximum iterations%'")
        deleted_count += cursor.rowcount
        
        conn.commit()
        conn.close()
        print(f"Successfully cleaned {deleted_count} bad entries from memory.")
    except Exception as e:
        print(f"Error cleaning memory: {e}")
else:
    print("No memory database found.")
