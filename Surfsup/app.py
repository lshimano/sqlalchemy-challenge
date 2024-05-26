# Import the dependencies.
# SQLAlchemy
from pathlib import Path
from sqlalchemy import create_engine, text

# Path to sqlite
database_path = Path("../Resources/hawaii.sqlite")


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine(f"sqlite:///{database_path}")

# Query All Records in the the Database
data = engine.execute(text("SELECT * FROM wdi_2018"))

for record in data:
    print(record)

# Declare a Base using `automap_base()`

# Use the Base class to reflect the database tables