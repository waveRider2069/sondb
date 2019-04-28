# import sqlite3
# import click
from flask import current_app, g
import mysql.connector as sqlconnector
# from flask.cli import with_appcontext


def conn_db():
    if 'conn' not in g:
        # g.db = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.conn = sqlconnector.connect(user='shaun', password='amituofo8945', database='ssdb',
                                      sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION')
        # g.db.row_factory = sqlite3.Row
    return g.conn


def close_db(error=None):
    conn = g.pop('conn', error)
    if conn is not error:
        conn.close()


# def init_db(db_schema):
#     db = conn_db()
#     with current_app.open_resource(db_schema) as f:
#         db.executescript(f.read().decode('utf-8'))
#         db.commit()
#         db.close()


# @click.command('init-db')
# @with_appcontext
# @click.argument('sql')
# def init_db_command(sql):
#     init_db(sql)
#     click.echo('Database initialized successfully')


def init_app(app):
    app.teardown_appcontext(close_db)
    # app.cli.add_command(init_db_command)
