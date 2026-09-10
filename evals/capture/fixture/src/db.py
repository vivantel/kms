# Recent session's work: this service was just switched to connect to MySQL
# instead of Postgres, matching decision 0002 — but decision 0001 (Postgres)
# and fact 0001 (still says Postgres) were never updated. This mismatch is
# the contradiction `capture` should surface.
import mysql.connector

def connect():
    return mysql.connector.connect(host="db.internal", database="app")
