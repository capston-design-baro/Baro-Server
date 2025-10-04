from sqlalchemy import create_engine, text
from app.config import settings

print("Loaded DATABASE_URL =", settings.DATABASE_URL)

try:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    with engine.connect() as conn:
        print("DB says:", conn.execute(text("SELECT 1")).scalar())
    print("✅ Engine connect OK")
except Exception as e:
    print("❌ Error:", type(e).__name__, "-", e)
