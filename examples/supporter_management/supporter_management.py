import argparse
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_suffix('.db')

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS supporters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
"""


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(CREATE_TABLE_SQL)
    conn.commit()


def add_supporter(conn: sqlite3.Connection, name: str, email: str) -> None:
    conn.execute("INSERT INTO supporters (name, email) VALUES (?, ?)", (name, email))
    conn.commit()


def remove_supporter(conn: sqlite3.Connection, supporter_id: int) -> None:
    conn.execute("DELETE FROM supporters WHERE id = ?", (supporter_id,))
    conn.commit()


def list_supporters(conn: sqlite3.Connection) -> None:
    rows = conn.execute("SELECT id, name, email FROM supporters ORDER BY id").fetchall()
    for row in rows:
        print(f"{row[0]}: {row[1]} <{row[2]}>")


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple supporter management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new supporter")
    add_parser.add_argument("name")
    add_parser.add_argument("email")

    remove_parser = subparsers.add_parser("remove", help="Remove a supporter")
    remove_parser.add_argument("id", type=int)

    subparsers.add_parser("list", help="List all supporters")

    args = parser.parse_args()

    with sqlite3.connect(DB_PATH) as conn:
        init_db(conn)
        if args.command == "add":
            add_supporter(conn, args.name, args.email)
        elif args.command == "remove":
            remove_supporter(conn, args.id)
        elif args.command == "list":
            list_supporters(conn)


if __name__ == "__main__":
    main()
