from database import engine

try:
    with engine.connect() as conn:
        print("✅ Connected to PostgreSQL!")
except Exception as e:
    print(e)