from flask import g
DATABASE = 'D:\\Licenta Proiect Practic\\fuzzing.sqlite'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
	
cursor = get_db().cursor()
sqlite_select_query = """SELECT * from Stats"""	