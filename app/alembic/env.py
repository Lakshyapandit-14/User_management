# alembic/env.py (only the minimal part shown below)
# Purpose: Hook SQLAlchemy models into Alembic autogenerate.
# This file is used by alembic CLI - keep it in alembic/ directory.

from logging.config import fileConfig
from sqlalchemy import engine_from_config # type: ignore
from alembic import context
import os
import sys

# Make project package visible to alembic env
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_dir)

from core.config import settings
from core.connections.database import Base  # Base with metadata
import services.users.models  # Ensure models are imported

# Alembic config and target_metadata
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# The rest of the standard alembic env.py (connection handling + run_migrations) should be here.
# Use DATABASE_URL environment variable (or alembic.ini) for DB connection.