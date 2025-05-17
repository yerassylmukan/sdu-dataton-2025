import psycopg2
import psycopg2.extras

def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="team_twentyseven",
        password="gQ7$rN3@kP",
        host="3.74.122.135",      # or IP
        port="5432"               # or other port
    )
