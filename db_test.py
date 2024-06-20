import psycopg

print("test")
print("1")
print("2")
print("3")

def connection():
    config = {'user':'jeffrey',
          'password':'strawberries',
              'host':'127.0.0.1',
              'port':'5432',
            'dbname':'trader',
        'autocommit':True} #this resolve the problem "InternalError: CREATE DATABASE cannot run inside a transaction block"
    try:
        cnx = psycopg.connect(**config)
    except psycopg.Error as err:
        print(err)
        exit(1)
    else:
        return cnx
    
db_connection = connection()  # this worked!!

with psycopg.connect("host=localhost port=5432 user=jeffrey password=strawberries dbname=trader") as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        print("")

        #cur.execute("\conninfo")
        # Execute a command: this creates a new table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS test (
                id serial PRIMARY KEY,
                num integer,
                data text)
            """)

        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no SQL injections!)
        cur.execute(
            "INSERT INTO test (num, data) VALUES (%s, %s)",
            (100, "abc'def"))

        cur.execute(
            "INSERT INTO test (num, data) VALUES (%s, %s)",
            (200, "ghi'jkl"))

        # Query the database and obtain data as Python objects.
        cur.execute("SELECT * FROM test")
        #cur.fetchone()
        # will return (1, 100, "abc'def")

        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        #for record in cur:
        #    print(record)

        print(cur.fetchall())

        # Make the changes to the database persistent
        conn.commit()

