from app.core.connections.database import Base, engine
from app.services.users.models import User
from app.services.users.profile.models import UserProfile

Base.metadata.create_all(bind=engine)
print("Tables created!")