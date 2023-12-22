import sqlalchemy


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
    prompt = Prompt("gdpr", "this is a gdpr text whatever")
    prompt.save_prompt()
