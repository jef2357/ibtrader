--SELECT * FROM tick_price WHERE recv_time::date = current_date AND reqid = 103 AND name = 'LAST';
--SELECT * FROM tick_price WHERE recv_time::date = current_date AND reqid = 103;


SELECT * FROM tick_price WHERE recv_time::date = current_date AND reqid = 103 AND name = 'LAST' ORDER BY recv_time;

-- select all unique values of  


SELECT DISTINCT reqid
FROM tick_price
WHERE DATE(recv_time) = CURRENT_DATE;


SELECT symbol
FROM reqid_list
WHERE reqid = 103 AND DATE(send_time) = CURRENT_DATE;

SELECT symbol, reqid
FROM reqid_list
WHERE DATE(send_time) = CURRENT_DATE;

SELECT DISTINCT reqid, symbol
FROM reqid_list
WHERE DATE(send_time) = CURRENT_DATE;

