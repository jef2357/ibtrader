import psycopg
from psycopg import sql, ClientCursor
import threading
import time
import queue
import logging

logger = logging.getLogger(__name__)

class ibDBConn(threading.Thread):
    def __init__(self, config) -> None:
          super().__init__(name= 'db')
          self.db_config= config
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
        try:
            self.db_conn = psycopg.connect(**self.db_config)
            self.db_cur = self.db_conn.cursor()
            #self.cl_cur = ClientCursor(self.db_cur)
            pass
        except psycopg.Error as err:
            print(err)
            exit(1)

    def run(self) -> None:
        logger.debug("database thread: thread starting")
        self.stop_event.clear()
        _commands = []
        _cnt = 0
        self.unset_stop_event()
        try:
            while not self.stop_event.is_set():
                time.sleep(1)    # writing to db every 1 second (time.sleep() call waits for 1 second)
                # print("queue sizes - reqid:",self.reqid_list_queue.qsize(),
                #       "tbt:", self.tbt_all_last_queue.qsize(),
                #       "generic:", self.tick_generic_queue.qsize(),
                #       "price:", self.tick_price_queue.qsize(),
                #       "size:", self.tick_size_queue.qsize(),
                #       "string:", self.tick_string_queue.qsize()
                #       )
                #TODO: measure time it takes to write to db
                #_timer1_ = time.perf_counter()
                self.write_all()        
                #_timer2_ = time.perf_counter()
                # if _timer2_ - _timer1_ > .1:
                #     logger.warning("database thread: writing to database required %s seconds", str(_timer2_ - _timer1_))    
                #     print("database thread: writing to database required %s seconds", str(_timer2_ - _timer1_))
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

    def test(self):
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



    def _db_setup(self) -> None:
        pass
        create_tick_generic_table = """
            CREATE TABLE IF NOT EXISTS tick_generic (
                source TEXT,
                reqid INT,
                recv_time TIMESTAMP WITHOUT TIME ZONE,
                field INT,
                name TEXT,
                value NUMERIC
            )"""
        self.db_cur.execute(create_tick_generic_table)

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
        self.db_cur.execute(create_tick_price_table)

        create_tick_size_table = """
            CREATE TABLE IF NOT EXISTS tick_size (
                source TEXT,
                reqid INT,
                recv_time TIMESTAMP WITHOUT TIME ZONE,
                field INT,
                name TEXT,
                size NUMERIC
            )"""
        self.db_cur.execute(create_tick_size_table)

        create_tick_string_table = """
            CREATE TABLE IF NOT EXISTS tick_string (
                source TEXT,
                reqid INT,
                recv_time TIMESTAMP WITHOUT TIME ZONE,
                field INT,
                name TEXT,
                string TEXT
            )"""
        self.db_cur.execute(create_tick_string_table)

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
        self.db_cur.execute(create_reqid_list_table)

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
        self.db_cur.execute((create_tick_by_tick_all_last_table))

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
        self.db_cur.execute((create_real_time_bars))

        

