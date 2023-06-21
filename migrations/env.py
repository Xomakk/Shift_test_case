import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src import config as cfg
from src.database import Base

from src.auth.api.v1.models import Token, User
from src.salary.api.v1.models import Salary


sys.path.append(os.path.join(sys.path[0], 'src'))

config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB_HOST", cfg.DB_HOST)
config.set_section_option(section, "DB_PORT", cfg.DB_PORT)
config.set_section_option(section, "DB_USER", cfg.DB_USER)
config.set_section_option(section, "DB_NAME", cfg.DB_NAME)
config.set_section_option(section, "DB_PASS", cfg.DB_PASS)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
