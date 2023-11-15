import os
import time

import psycopg2
from psycopg2 import OperationalError

from dotenv import load_dotenv


load_dotenv()


def wait_for_db():
    dbname = os.getenv("POSTGRES_NAME")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    conn = None
    while conn is None:
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
        except OperationalError:
            print("Database unavailable, waiting 1 second...")
            time.sleep(1)
    conn.close()
    print("Database available!")


if __name__ == "__main__":
    wait_for_db()
