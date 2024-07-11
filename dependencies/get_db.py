from database import data

def get_db():
    database = data
    try:
        yield database
    finally:
        database.close()
        