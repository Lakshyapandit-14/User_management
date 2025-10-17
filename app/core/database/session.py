from app.core.connections.database import SessionLocal

# Dependency — gets a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
