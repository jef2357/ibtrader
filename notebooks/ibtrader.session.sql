--SELECT id FROM reqid_list WHERE symbol = 'SPX' AND EXTRACT(DAY FROM send_time) = 29;

--SELECT * from reqid_list WHERE id = '243';

--SELECT * from reqid_list


--SELECT id FROM reqid_list WHERE symbol = 'SPX' AND EXTRACT(MONTH FROM send_time) = 05 AND EXTRACT(DAY FROM send_time) = 31;

--SELECT reqid FROM reqid_list WHERE id = 258


SELECT * from tick_price WHERE reqid = 103 AND name = 'LAST' AND EXTRACT(MONTH FROM recv_time) = 05 AND EXTRACT(DAY FROM recv_time) = 31