import os
import importlib
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv  

# Load environment variables from .env file
load_dotenv()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.db.base import Base

def import_all_models():
    # Correct the path to the models directory
    models_dir = os.path.join(os.path.dirname(__file__), "../models")
    models_dir = os.path.abspath(models_dir)  # Ensure it's an absolute path

    for filename in os.listdir(models_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"app.db.models.{filename[:-3]}"
            importlib.import_module(module_name)

# Import all models to register them with Base
import_all_models()

target_metadata = Base.metadata

def get_db_url():
    user = os.getenv("POSTGRES_USER")         
    password = os.getenv("POSTGRES_PASSWORD") 
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("POSTGRES_DB")         
    driver = os.getenv("DB_DRIVER", "postgresql") 

    return f"{driver}://{user}:{password}@{host}:{port}/{dbname}"


def run_migrations_offline() -> None:
    url = get_db_url()  # get URL from env variables
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # override the sqlalchemy.url config with env var URL
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_db_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
