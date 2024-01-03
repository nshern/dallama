from sqlalchemy import MetaData, Table, create_engine, select

# Define the path to the SQLite database file
database_path = "db.db"
# Create an SQLAlchemy engine
engine = create_engine(f"sqlite:///{database_path}")
# Initialize metadata object
metadata = MetaData()
# Define the structure of the 'prompt' table
prompt_table = Table(
    "prompt", metadata, autoload_with=engine
)  # autoload the columns from the existing table
# Create a select statement to query the entire 'prompt' table
select_statement = select(prompt_table).where(prompt_table.c.title == "gdpr")
# Execute the query and fetch the results
with engine.connect() as connection:
    result = connection.execute(select_statement)
    row = result.fetchone()

    if row:
        title = row[0]
        content = row[1]

    else:
        print("NO content found")
