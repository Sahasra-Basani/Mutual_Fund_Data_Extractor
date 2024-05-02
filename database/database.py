import psycopg2


def connect_to_db(dbname, user, password, host, port):
    """Connection to PostgreSQL database """

    try:
        con = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Connected to database successfully")
        return con

    except psycopg2.Error as e:
        print("Error connecting to the database", e)
        return None



