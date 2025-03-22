import psycopg
#from psycopg import sql, ClientCursor
import threading
import time
import datetime
import queue
import logging

from spx_trader_db_commands import table_creation_commands

logger = logging.getLogger(__name__)

class spxTraderDBConn(threading.Thread):
    def __init__(self, config) -> None:
          super().__init__(name= 'db')
          self.db_config= config
          self.db_connected = False
          self._db_connect()
          self._db_setup()
          self.db_lock= threading.Lock()
          self.stop_event= threading.Event()        
          self.db_last_write= time.perf_counter()
          self.reqid_list_queue= queue.Queue()
          self.tbt_all_last_queue= queue.Queue()
          self.tick_generic_queue= queue.Queue()
          self.tick_price_queue= queue.Queue()
          self.tick_size_queue= queue.Queue()
          self.tick_string_queue= queue.Queue()

    def _db_connect(self) -> None:
        if not self.db_connected:
            try:
                self.db_conn = psycopg.connect(**self.db_config)
                self.db_cur = self.db_conn.cursor()
            except psycopg.Error as err:
                # print error to console? print error to message window in ui?
                print(err)
                exit(1)
            else:
                self.db_connected = True
        else:
            pass
    
    def _db_disconnect(self) -> None:
        if self.db_connected:
            self.db_conn.close()
            self.db_connected = False
        else:
            pass

    def _db_setup(self) -> None:
        table_names, table_commands = table_creation_commands()
    
        today_db_name = "trader_" + datetime.date.today().strftime("%Y_%m_%d")

        if not self.db_connected:
            self._db_connect()
        
        # get list of all database names
        self.db_cur.execute("SELECT datname from pg_database;")
        db_list = self.db_cur.fetchall()

        # if today's database does not exist yet, create it
        if (today_db_name,) not in db_list:
            self.db_cur.execute(f"CREATE DATABASE {today_db_name}")

        # get currently connected db name
        self.db_cur.execute("SELECT current_database();")
        current_db_name = self.db_cur.fetchone()[0]

        # if currently connected db is not today's db, close connection and reconnect to today's db
        if current_db_name != today_db_name:
            self._db_disconnect()
            self.db_config['dbname'] = today_db_name
            self._db_connect()

        # connected to today's db, create tables
        #     creation commands have "IF NOT EXISTS" so they will not be created if they already exist
        for table_command in table_commands:
            self.db_cur.execute(table_command)                                
            # TODO: execute hyptertable customizations
        
        # TODO: get tables that are hypertables
        # self.db_cur.execute("SELECT * FROM timescaledb_information.hypertables;")
        # hypertables = self.db_cur.fetchall()
        # hypertables_list = []
        # for row in hypertables:
        #     hypertables_list.append(row[1])


        ########### this command to get the table names is not working
        #
        # self.db_cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        # exisitng_table_names = self.db_cur.fetchall()

        # for table_name, table_command in zip(table_names, table_commands):
        #     if table_name in exisitng_table_names:
        #         pass
        #     else:
        #         self.db_cur.execute(table_command)                
                
        #         # TODO: execute hyptertable customizations



    def run(self) -> None:
        logger.debug("database thread: thread starting")
        self.stop_event.clear()
        _commands = []
        _cnt = 0
        self.unset_stop_event()
        try:
            _loop_timer1 = time.perf_counter()
            while not self.stop_event.is_set():
                _loop_timer2 = time.perf_counter()
                _loop_time = _loop_timer2 - _loop_timer1
                if _loop_time < 1.0:
                    time.sleep(1.0 - _loop_time)
                else:
                    logger.warning("database thread: writing to database required %s seconds", str(_loop_timer2 - _loop_timer1))    
                    print("database thread: writing to database required %s seconds", str(_loop_timer2 - _loop_timer1))
                # writing to db every 1 second (time.sleep() call waits for 1 second)
                # print("queue sizes - reqid:",self.reqid_list_queue.qsize(),
                #       "tbt:", self.tbt_all_last_queue.qsize(),
                #       "generic:", self.tick_generic_queue.qsize(),
                #       "price:", self.tick_price_queue.qsize(),
                #       "size:", self.tick_size_queue.qsize(),
                #       "string:", self.tick_string_queue.qsize()
                _loop_timer1 = time.perf_counter()
                self.write_all()
        except:
            logger.error("databse thread: undhandled exception in database thread")
            self.set_stop_event()
        finally:
            if self.stop_event.is_set() == True:
                logger.info("database thread: thread stopped")
            else:
                self.set_stop_event()
                logger.info("database thread: thread stopped")

    def enqueue(self, table:str, cmd:str, var) -> None:
        match table:
            case "reqid_list":
                self.reqid_list_queue.put((var))
            case "tbt_all_last":
                self.tbt_all_last_queue.put((var))
            case "tick_generic":
                self.tick_generic_queue.put((var))
            case "tick_price":
                self.tick_price_queue.put((var))
            case "tick_size":
                self.tick_size_queue.put((var))
            case "tick_string":
                self.tick_string_queue.put((var))

    def write_all(self) -> None:
        self.reqid_list_copy()
        self.tbt_all_last_copy()
        self.tick_generic_copy()
        self.tick_price_copy()
        self.tick_size_copy()
        self.tick_string_copy()

    def test(self) -> None:
        pass
        # _data = [("ib_api", 103, "2024-04-26 14:57:20.539164-05", 6, "HIGH", 5114.62, "CanAutoExecute: 0, PastLimit: 0, PreOpen: 0"),
        #          ("ib_api", 103, "2024-04-26 14:57:20.596737-05", 7, "LOW", 5073.14,"CanAutoExecute: 0, PastLimit: 0, PreOpen: 0"),
        #          ("ib_api", 103, "2024-04-26 14:57:20.648593-05", 9, "CLOSE", 5048.42, "CanAutoExecute: 0, PastLimit: 0, PreOpen: 0"),
        #          ("ib_api", 103, "2024-04-26 14:57:20.648593-05", 9, "CLOSE", 5048.42, "CanAutoExecute: 0, PastLimit: 0, PreOpen: 0"),
        #          ("ib_api", 103, "2024-04-26 14:57:20.700442-05", 4, "LAST", 5099.89, "CanAutoExecute: 0, PastLimit: 0, PreOpen: 0"),
        # ]

        # #_query = sql.SQL("INSERT INTO {table} VALUES (%s, %s, %s, %s, %s, %s, %s)").format(fields=sql.SQL(',').join([ for _i in _data[0] sql.IDentifier(_i)]),
        # #            table=sql.Identifier('tick_price'))
        
        # #self.db_cur.execute(sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s)").format(sql.Identifier('tick_price')), _data[0])
        # #self.db_cur.execute(sql.SQL("INSERT INTO {} VALUES ").format(sql.Identifier('tick_price')), _data[0])

        # with self.db_cur.copy("COPY tick_price (source,reqid,recv_time,field,name,price,attributes) FROM STDIN") as copy:
        #     for _row in _data:
        #         copy.write_row(_row)

    def reqid_list_copy(self) -> None:
        if self.reqid_list_queue.qsize() > 0:
            _values = []
            while not self.reqid_list_queue.empty():
                 _values.append((self.reqid_list_queue.get()))
            
            with self.db_cur.copy("COPY reqid_list (source,reqid,send_time,req_func,symbol,security_type,exchange,currency) FROM STDIN") as copy:
                for _row in _values:
                    copy.write_row(_row)

    def tbt_all_last_copy(self) -> None:
        if self.tbt_all_last_queue.qsize() > 0:
            _values = []
            while not self.tbt_all_last_queue.empty():
                 _values.append((self.tbt_all_last_queue.get()))
            
            with self.db_cur.copy("COPY tbt_all_last (source, reqid, recv_time, tick_type, tick_name, ib_time, price, size, exchange, spec_cond, past_limit, unreported) FROM STDIN") as copy:
                for _row in _values:
                    copy.write_row(_row)

    def tick_generic_copy(self) -> None:
        if self.tick_generic_queue.qsize() > 0:
            _values = []
            while not self.tick_generic_queue.empty():
                 _values.append((self.tick_generic_queue.get()))
            
            with self.db_cur.copy("COPY tick_generic (source, reqid, recv_time, field, name, value) FROM STDIN") as copy:
                for _row in _values:
                    copy.write_row(_row)

    def tick_price_copy(self) -> None:
        if self.tick_price_queue.qsize() > 0:
            _values = []
            while not self.tick_price_queue.empty():
                 _values.append((self.tick_price_queue.get()))
            
            with self.db_cur.copy("COPY tick_price (source,reqid,recv_time,field,name,price,attributes) FROM STDIN") as copy:
                for _row in _values:
                    copy.write_row(_row)
    
    def tick_size_copy(self) -> None:
        if self.tick_size_queue.qsize() > 0:
            _values = []
            while not self.tick_size_queue.empty():
                 _values.append((self.tick_size_queue.get()))
            
            with self.db_cur.copy("COPY tick_size (source, reqid, recv_time, field, name, size) FROM STDIN") as copy:
                for _row in _values:
                    copy.write_row(_row)

    def tick_string_copy(self) -> None:
        if self.tick_string_queue.qsize() > 0:
            _values = []
            while not self.tick_string_queue.empty():
                 _values.append((self.tick_string_queue.get()))
            
            with self.db_cur.copy("COPY tick_string (source, reqid, recv_time, field, name, string) FROM STDIN") as copy:
                for _row in _values:
                    copy.write_row(_row)

    def set_stop_event(self) -> None:
        if self.stop_event.is_set() == False:
            self.stop_event.set()
            logger.debug("sender thread: stop event set")

    def unset_stop_event(self) -> None:
        if self.stop_event.is_set() == True:
            self.stop_event.clear()
            logger.debug("sender thread: stop event cleared")

    
                

