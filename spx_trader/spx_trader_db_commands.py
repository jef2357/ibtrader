def table_creation_commands():
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


