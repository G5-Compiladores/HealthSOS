from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# It's a good practice to load sensitive info like the database URL from environment variables.
# Use environment variables for database credentials (more secure).
SQLALCHEMY_DATABASE_URL = "mysql://user:password@localhost/dbname"  # Ensure you're using a valid MySQL driver

# Create the engine with a connection pool. Use NullPool for short-lived connections.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"charset": "utf8mb4"},  # Specify connection arguments as necessary
)

# SessionLocal will generate database sessions bound to the engine.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions (models)
Base = declarative_base()


# Dependency to get a session to interact with the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Always close the session when done to avoid connection leaks
