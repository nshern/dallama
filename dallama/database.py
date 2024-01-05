import sqlalchemy


def retrieve_prompt(id):
    engine = sqlalchemy.create_engine("sqlite:///db.db")
    metadata = sqlalchemy.MetaData()

    # Define the structure of the 'prompt' table
    prompt_table = sqlalchemy.Table("prompt", metadata, autoload_with=engine)

    # Create a select statement to query the entire 'prompt' table
    select_statement = sqlalchemy.select(prompt_table).where(prompt_table.c.title == id)
    # Execute the query and fetch the results
    with engine.connect() as connection:
        result = connection.execute(select_statement)
        row = result.fetchone()

        if row:
            # title = row[0]
            content = row[1]

            return content

        else:
            print("NO content found")


if __name__ == "__main__":
    content = retrieve_prompt("gdpr")
    print(content)
