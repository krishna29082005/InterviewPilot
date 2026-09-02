import logging

from app.db.database import Base, engine

# Import all models so SQLAlchemy knows about them
from app.models.user import User

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

logger.info("Database initialized successfully!")