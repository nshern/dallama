import sqlalchemy


def _get_engine():
    engine = sqlalchemy.create_engine("sqlite:///db.db")

    return engine


def _get_prompt_table():
    engine = _get_engine()
    metadata = sqlalchemy.MetaData()
    prompt_table = sqlalchemy.Table("prompt", metadata, autoload_with=engine)

    return prompt_table


def retrieve_all_prompts():
    engine = _get_engine()
    table = _get_prompt_table()
    select_statement = sqlalchemy.select(table)

    with engine.connect() as connection:
        result = connection.execute(select_statement)
        for row in result:
            print(row)


def retrieve_prompt(id) -> dict:
    engine = _get_engine()
    prompt_table = _get_prompt_table()

    # Create a select statement to query the entire 'prompt' table
    select_statement = sqlalchemy.select(prompt_table).where(
        prompt_table.c.title == id
    )
    # Execute the query and fetch the results
    with engine.connect() as connection:
        result = connection.execute(select_statement)
        row = result.fetchone()

        if row:
            title = row[0]
            content = row[1]

            return {"title": title, "content": content}

        else:
            return {}


def delete_prompt(prompt_id):
    pass


class Prompt:
    """
    Represents a writing prompt with a title and content.

    Attributes:
        title (str): The title of the prompt.
        content (str): The content or body of the prompt.
    """

    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content

    # Write prompt to database
    def save_prompt(self):
        # Create engine
        engine = sqlalchemy.create_engine("sqlite:///db.db")

        metadata = sqlalchemy.MetaData()

        prompt = sqlalchemy.Table(
            "prompt",
            metadata,
            sqlalchemy.Column("title", sqlalchemy.String, primary_key=True),
            sqlalchemy.Column("content", sqlalchemy.Text),
        )

        metadata.create_all(engine)

        with engine.connect() as conn:
            insert_statement = sqlalchemy.insert(prompt)
            records = [
                {
                    "title": f"{self.title}",
                    "content": f"{self.content}",
                },
            ]

            conn.execute(insert_statement, records)
            conn.commit()


if __name__ == "__main__":
    # prompt = Prompt("foo", "this is a gdpr text whatever")
    # prompt.save_prompt()
    retrieve_all_prompts()
