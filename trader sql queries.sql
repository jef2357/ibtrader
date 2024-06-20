--SELECT * from tick_price WHERE name='LAST' AND recv_time > '2024-04-26'


-- Extract the DAY from the timestamp and filter rows for a specific day
--SELECT * FROM tick_price WHERE EXTRACT(DAY FROM recv_time) = 29 AND WHERE EXTRACT(HOUR FROM recv_time) = 14


-- Calculate the difference in days between two timestamps
--SELECT event_time - '2024-01-01' AS days_since_start FROM events;


SELECT * FROM tbt_all_last