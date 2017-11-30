import random
from urllib import parse
import psycopg2
import config


def sql_command(sql, fetch):
    parse.uses_netloc.append("postgres")
    url = parse.urlparse(config.database_url)
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()
    cursor.execute(sql)
    if fetch:
        rows = cursor.fetchall()
        return rows
    conn.commit()
    conn.close()


def write_to_base(file_id, erase):
    if not erase:
        sql_command("INSERT INTO file_id VALUES({})".format(file_id), fetch=False)
    else:
        sql_command("DELETE FROM file_id WHERE id = {}".format(file_id), fetch=False)


def read_from_base():
    rows = sql_command("SELECT * FROM file_id", fetch=True)
    return rows
