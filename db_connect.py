import sqlite3
import config


def sql_command(sql, fetch):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    if fetch:
        rows = cursor.fetchall()
        return rows
    conn.commit()
    conn.close()


def write_to_base(table_id, file_id, erase):
    if not erase:
        sql_command("INSERT INTO {} VALUES ('{}')".format(table_id, file_id), fetch=False)
    else:
        sql_command("DELETE FROM {} WHERE id = '{}'".format(table_id, file_id), fetch=False)


def create_table(bot, update):
    chat_id = config.chat_id
    for c in chat_id:
        sql_command("CREATE TABLE {} (id text PRIMARY KEY)".format(c[1:]), fetch=False)


def read_from_base(table_id):
    rows = sql_command("SELECT * FROM {}".format(table_id), fetch=True)
    return rows


def truncate_all(bot, update):
    chat_id = config.chat_id
    for c in chat_id:
        sql_command("TRUNCATE {}".format(c[1:]), fetch=False)


def delete_all(bot, update):
    chat_id = config.chat_id
    for c in chat_id:
        sql_command("DROP TABLE {}".format(c[1:]), fetch=False)
