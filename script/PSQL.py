import psycopg2
import datetime

# user = "postgres"
# password = "sL6IpcVZKv57HcZZTX3x"
# host = "package-picker-test.c7etfrntf9yq.us-east-1.rds.amazonaws.com"
# conn_string = str("host=%s user=%s password=%s", (host, user, password))

conn_string = "host='localhost' dbname='postgres' user='postgres' password='secret'"
def connectToDB():
    # Connect to the database
    db = psycopg2.connect(conn_string)
    return db

def insertToApplication(db, url, followers, appName):
    # Get a cursor for executing queries
    cur = db.cursor()
    # Upsert a row into the applications table
    cur.execute("INSERT INTO applications (url, name, followers, retrieved) VALUES (%s, %s, %s, %s) ON CONFLICT ON CONSTRAINT unique_url_and_hash DO UPDATE SET (url, name, followers, retrieved) = (EXCLUDED.url, EXCLUDED.name, EXCLUDED.followers, EXCLUDED.retrieved) RETURNING id;", (url, appName, followers, datetime.datetime.now()))
    # print("%s, %s, %s", (url, appName, followers))
    id = cur.fetchone()[0]
    # Commit the transaction
    db.commit()
    # Get the row you just inserted
    cur.execute("SELECT * FROM applications;")
    # return cur.fetchall()
    return id

def insertToPackages(db, name):
    cur = db.cursor()
    cur.execute("INSERT INTO packages (name, retrieved) VALUES (%s, %s) ON CONFLICT(name) DO UPDATE SET name=EXCLUDED.name RETURNING id;", (name, datetime.datetime.now()))
    id = cur.fetchone()[0]
    db.commit()
    cur.execute("SELECT * FROM packages;")
    # return cur.fetchall()
    return id

def insertToDependencies(db,application_id,package_id):
    cur = db.cursor()
    cur.execute("INSERT INTO dependencies (application_id, package_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (application_id, package_id))
    db.commit()
    cur.execute("SELECT * FROM dependencies;")
    return cur.fetchall()