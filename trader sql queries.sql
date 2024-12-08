--SELECT * from tick_price WHERE name='LAST' AND recv_time > '2024-04-26'


-- Extract the DAY from the timestamp and filter rows for a specific day
--SELECT * FROM tick_price WHERE EXTRACT(DAY FROM recv_time) = 29 AND WHERE EXTRACT(HOUR FROM recv_time) = 14


-- Calculate the difference in days between two timestamps
--SELECT event_time - '2024-01-01' AS days_since_start FROM events;


SELECT * FROM tbt_all_last

-- how do I get a list of tables inteh database
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

--how do I get a list of columns in a table
SELECT column_name FROM information_schema.columns WHERE table_name = 'tick_price';

--how do I get a list of colmns from reqid_list table
SELECT column_name FROM information_schema.columns WHERE table_name = 'reqid_list';

--how do I select timestamp data from today?
SELECT * FROM tick_price WHERE recv_time::date = current_date;

--how do I select data from a column with timestamp data from today?
SELECT * FROM reqid_list WHERE send_time::date = current_date;


-- how do I select all prices from tick_price with date equals today and reqid equals 103 and name equals LAST sorted by recv_time
SELECT * FROM tick_price WHERE recv_time::date = current_date AND reqid = 103 AND name = 'LAST' ORDER BY recv_time;

SELECT * FROM tick_price WHERE recv_time::date = current_date AND reqid = 103 AND name = 'LAST';

SELECT * FROM tick_price WHERE recv_time::date = current_date AND reqid = 103;

