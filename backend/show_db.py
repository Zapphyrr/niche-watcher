from sqlalchemy import inspect, text
from database import engine

print("=== DATABASE SCHEMA ===")
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tables found: {tables}")

for table in tables:
    cols = inspector.get_columns(table)
    print(f"\nTable: {table}")
    for col in cols:
        print(f"  - {col['name']}: {col['type']}")

print("\n=== DATABASE DATA ===")
with engine.connect() as conn:
    print("Users table:")
    try:
        result = conn.execute(text("SELECT id, email, subscribed FROM users;"))
        rows = result.fetchall()
        if rows:
            for row in rows:
                print(f"  id={row[0]}, email={row[1]}, subscribed={row[2]}")
        else:
            print("  (no users)")
    except Exception as e:
        print(f"  Error: {e}")
    
    print("\nUser Credentials table:")
    try:
        result = conn.execute(text("SELECT id, user_id, hashed_password FROM user_credentials;"))
        rows = result.fetchall()
        if rows:
            for row in rows:
                pwd = row[2][:20] + "..." if len(row[2]) > 20 else row[2]
                print(f"  id={row[0]}, user_id={row[1]}, password={pwd}")
        else:
            print("  (no credentials)")
    except Exception as e:
        print(f"  Error: {e}")
        
    print('\n\nBest Posts table:')
    try :
        result = conn.execute(text("SELECT id, title, url, source, published_at, content FROM best_hackernew;"))
        rows = result.fetchall()
        if rows:
            for row in rows:
                print(f"  id={row[0]}, title={row[1]}, url={row[2]}, source={row[3]}, published_at={row[4]}, content={row[5]}")
        else:
            print("  (no best posts)")
    except Exception as e:
        print(f"  Error: {e}")