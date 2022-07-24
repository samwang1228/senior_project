SQLITE_DB_PATH = 'backend/test.db'
SQLITE_DB_SCHEMA = 'backend/create_db.sql'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_PATH)
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
    return db


def reset_db():
    with open(SQLITE_DB_SCHEMA, 'r') as f:
        create_db_sql = f.read()
    db = get_db()
    # Reset database
    # Note that CREATE/DROP table are *immediately* committed
    # even inside a transaction
    with db:
        db.execute("DROP TABLE IF EXISTS members")
        db.execute("DROP TABLE IF EXISTS histories")
        db.execute("DROP TABLE IF EXISTS test")
        db.execute("DROP TABLE IF EXISTS temp")
        db.executescript(create_db_sql)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()