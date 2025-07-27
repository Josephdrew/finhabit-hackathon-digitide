# alembic/env.py

import asyncio
from logging.config import fileConfig
import os

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Alembic Config
config = context.config
fileConfig(config.config_file_name)

# Import your models and Base (sync-compatible metadata)

import pkgutil
import importlib

import app.models  # root of your models package

models_path = app.models.__path__

# Dynamically import all modules in app.models
for _, module_name, _ in pkgutil.iter_modules(models_path):
    try:
        importlib.import_module(f"app.models.{module_name}")
    except Exception as e:
        print(f"Failed to import {module_name}: {e}")

from app.core.database import Base
target_metadata = Base.metadata


# DB URL (async format: postgresql+asyncpg://user:pass@host/db)
DATABASE_URL = os.getenv("DATABASE_URL")

# Async engine for migrations
engine = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

# ------------------------
# OFFLINE MODE
# ------------------------
def run_migrations_offline():
    """Run migrations in 'offline' mode (no DB connection)."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# ------------------------
# ONLINE MODE
# ------------------------
def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode (with async engine)."""
    async with engine.connect() as conn:
        await conn.run_sync(do_run_migrations)

    await engine.dispose()

# Run appropriate migration mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
