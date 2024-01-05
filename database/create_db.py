import sqlite3
from pathlib import Path

# cursor.execute("""DROP TABLE IF EXISTS base_model""")
# cursor.execute("""DROP TABLE IF EXISTS prompt""")
# cursor.execute("""DROP TABLE IF EXISTS custom_model""")
#
#
# TODO: allow for specification of path so that it can be used in test folder


def create_db(path=""):
    path = ""
    path_obj = Path(path)

    db = sqlite3.connect("overview.db")
    cursor = db.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS base_model(
                        id INTEGER PRIMARY KEY,
                        Name TEXT unique
                )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS prompt(
                        id INTEGER PRIMARY KEY,
                        text TEXT
                )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS custom_model(
                        id INTEGER PRIMARY KEY,
                        Temperature TEXT,
                        Modelfile TEXT,
                        PromptId INTEGER,
                        BaseModelId INTEGER,
                        FOREIGN KEY(PromptId) REFERENCES prompt(id),
                        FOREIGN KEY(BaseModelId) REFERENCES base_model(id)
                )"""
    )

    db.commit()


if __name__ == "__main__":
    create_db()
