# backend/alembic/env.py
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# 1. Look one folder up (..) to find the backend root directory
current_dir = os.path.dirname(os.path.abspath(__file__)) # inside backend/alembic/
backend_dir = os.path.abspath(os.path.join(current_dir, "..")) # up to backend/
sys.path.insert(0, backend_dir)

# 2. Tell dotenv exactly where your .env file is
env_path = os.path.join(backend_dir, ".env")
load_dotenv(dotenv_path=env_path)

config = context.config

# 3. Pull the database URL from the loaded environment variables
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError(f"DATABASE_URL could not be loaded! Checked path: {env_path}")

config.set_main_option("sqlalchemy.url", db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 4. Import your database structures so Alembic can track changes
from database import Base
from models.poker_models import GameSession, HandHistory, OpponentProfile
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    
    # 1. Grab the configuration dictionary
    connect_args = config.get_section(config.config_file_name, {})
    
    # 2. FORCE the URL we fetched from your .env file into the connection arguments
    connect_args["sqlalchemy.url"] = config.get_main_option("sqlalchemy.url")

    connectable = engine_from_config(
        connect_args,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()