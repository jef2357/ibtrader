import psycopg
import datetime
#from psycopg import sql, ClientCursor

# Hypertable creation command
#    SELECT create_hypertable('tbt_all_last', by_range('recv_time', INTERVAL '1 day'));
# Unique index command
#    CREATE UNIQUE INDEX tbt_all_last_id ON tbt_all_last(id, recv_time);


def tables():
    table_creation_commands = []
    table_names = []

    create_tick_price_table = """
        CREATE TABLE IF NOT EXISTS tick_price (
            source TEXT,
            reqid INT,
            recv_time TIMESTAMP WITHOUT TIME ZONE,
            field INT,
            name TEXT, 
            price NUMERIC, 
            attributes TEXT
        )"""
    table_names.append(['tick_price'])
    table_creation_commands.append(create_tick_price_table)

    create_tick_size_table = """
        CREATE TABLE IF NOT EXISTS tick_size (
            source TEXT,
            reqid INT,
            recv_time TIMESTAMP WITHOUT TIME ZONE,
            field INT,
            name TEXT,
            size NUMERIC
        )"""
    table_names.append(['tick_size'])
    table_creation_commands.append(create_tick_size_table)
    
    create_tick_string_table = """
        CREATE TABLE IF NOT EXISTS tick_string (
            source TEXT,
            reqid INT,
            recv_time TIMESTAMP WITHOUT TIME ZONE,
            field INT,
            name TEXT,
            string TEXT
        )"""
    table_names.append(['tick_string'])
    table_creation_commands.append(create_tick_string_table)
    
    create_reqid_list_table = """
        CREATE TABLE IF NOT EXISTS reqid_list (
            source TEXT,
            reqid INT,
            send_time TIMESTAMP WITHOUT TIME ZONE,
            req_func TEXT,
            symbol TEXT,
            security_type TEXT,
            exchange TEXT,
            currency TEXT
        )"""
    table_names.append(['reqid_list'])
    table_creation_commands.append(create_reqid_list_table)
    
    create_tick_by_tick_all_last_table = """
        CREATE TABLE IF NOT EXISTS tbt_all_last (
            source TEXT,
            reqid INT,
            recv_time TIMESTAMP WITHOUT TIME ZONE,
            tick_type INT,
            tick_name TEXT,
            ib_time INT,
            price NUMERIC,
            size NUMERIC,
            exchange TEXT,
            spec_cond TEXT,
            past_limit TEXT,
            unreported TEXT
        )"""
    table_names.append(['tbt_all_last'])
    table_creation_commands.append(create_tick_by_tick_all_last_table)
    
    create_real_time_bars = """
        CREATE TABLE IF NOT EXISTS rtb (
            source TEXT,
            reqid INT,
            recv_time TIMESTAMP WITHOUT TIME ZONE,
            open NUMERIC,
            high NUMERIC,
            low NUMERIC,
            close NUMERIC,
            volume NUMERIC,
            wap NUMERIC,
            count INT
        )"""
    table_names.append(['rtb'])  
    table_creation_commands.append(create_real_time_bars)

    return table_names, table_creation_commands


def db_setup(db_config) -> None:
    table_names, table_commands = tables()
    
    # today = datetime.date.today()
    # today_str = today.strftime("%Y-%m-%d")
    # today_db_name = today_str + "_trader"
    # today_db_name = today_db_name.replace("-", "")
    today_db_name = "trader_" + datetime.date.today().strftime("%Y_%m_%d")

    try:
        db_conn = psycopg.connect(**db_config)
        db_cur = db_conn.cursor()
    except psycopg.Error as err:
        # print error to console? print error to message window in ui?
        print(err)
        exit(1)

    db_cur.execute("SELECT datname from pg_database;")
    db_list = db_cur.fetchall()


    if (today_db_name,) in db_list:
        #print(f"Database {today_db_name} exists.")
        db_config['dbname'] = today_db_name
        db_conn.close()
        try:
            db_conn = psycopg.connect(**db_config)
            db_cur = db_conn.cursor()
        except psycopg.Error as err:
            print(err)
            exit(1)
    else:
        db_cur.execute(f"CREATE DATABASE {today_db_name}")
        #print(f"Database {today_db_name} created.")     

    return db_config

    

    # db_conn.close()

    # db_config['dbname'] = today_db_name
    # try:
    #     db_conn = psycopg.connect(**db_config)
    #     db_cur = db_conn.cursor()
    # except psycopg.Error as err:
    #     print(err)
    #     exit(1)


    #    NOT MESSING WITH HYPERTABLES FOR NOW
    #
    # get tables that are hypertables
    # db_cur.execute("SELECT * FROM timescaledb_information.hypertables;")
    # hypertables = db_cur.fetchall()
    # hypertables_list = []
    # for row in hypertables:
    #     hypertables_list.append(row[1])
    
    # check for table existence.  if not existsing, create.  If existing, check if hypertable.
    for table_name, table_command in zip(table_names, table_commands):
        db_cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)", table_name)
        if db_cur.fetchone()[0]:
            # print(f"Table {table_name} exists.")
            # if table_name[0] in hypertables_list:
            #     print(f"Table {table_name} is a hypertable.")
            # else:
            #     print(f"Table {table_name} is not a hypertable.")
            pass
        else:
            db_cur.execute(table_command)

            

if __name__ == "__main__":
    db_config = {'user':'jeffrey',
                  'password':'strawberries',
                  'host':'127.0.0.1',
                  'port':'5432',
                  'dbname':'trader',
                  'autocommit':True} #this resolve the problem "InternalError: CREATE DATABASE cannot run inside a transaction block"
    db_setup(db_config)
    print("Database setup complete.")
    exit(0)





    
    
    

