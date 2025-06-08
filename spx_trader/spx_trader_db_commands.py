def table_creation_commands():
    table_creation_commands = []
    # TODO:
    #    can put timescale customization commands into this list
    table_initialization_commands = []
    table_names = []

    create_database_audit_table = """
        CREATE TABLE IF NOT EXISTS database_audit (
            id BIGSERIAL PRIMARY KEY,
            datname TEXT,
            created_on TIMESTAMPTZ DEFAULT NOW()
        )""";
    table_names.append(['database_audit'])
    table_creation_commands.append(create_database_audit_table)

    query_database_creation_timestamp = """
        INSERT INTO database_audit (datname, created_on)
        VALUES (current_database(), NOW())
    """
    table_initialization_commands.append(query_database_creation_timestamp)
    # query_database_creation_timestamp = """
    #     INSERT INTO database_audit (datname, created_on)
    #     VALUES (current_database(), NOW())
    #     ON CONFLICT (datname) DO NOTHING
    # """

    create_contract_table = """
        CREATE TABLE IF NOT EXISTS contract (
            id BIGSERIAL PRIMARY KEY,
            source TEXT,
            reqid INT,
            recv_time TIMESTAMP WITHOUT TIME ZONE,
            conid INT,
            symbol TEXT,
            sec_type TEXT,
            exchange TEXT,
            primary_exchange TEXT,      
            currency TEXT,
            last_trade_date_or_contract_month TEXT,
            strike NUMERIC,
            right_ TEXT,
            trading_class TEXT
        )"""
    table_names.append(['contract'])
    table_creation_commands.append(create_contract_table)
            
    create_tick_generic_table = """
        CREATE TABLE IF NOT EXISTS tick_generic (
                id BIGSERIAL PRIMARY KEY,
                source TEXT,
                reqid INT,
                recv_time TIMESTAMPTZ,
                field INT,
                name TEXT,
                value NUMERIC
        )"""
    table_names.append(['tick_generic'])
    table_creation_commands.append(create_tick_generic_table)
    
    create_tick_price_table = """
        CREATE TABLE IF NOT EXISTS tick_price (
            id BIGSERIAL PRIMARY KEY,
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
            id BIGSERIAL PRIMARY KEY,
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
            id BIGSERIAL PRIMARY KEY,
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
            id BIGSERIAL PRIMARY KEY,
            source TEXT,
            reqid INT,
            send_time TIMESTAMP WITHOUT TIME ZONE,
            caller_func TEXT,
            caller_id INT,
            symbol TEXT,
            security_type TEXT,
            exchange TEXT,
            currency TEXT
        )"""
    table_names.append(['reqid_list'])
    table_creation_commands.append(create_reqid_list_table)
    
    create_tick_by_tick_all_last_table = """
        CREATE TABLE IF NOT EXISTS tbt_all_last (
            id BIGSERIAL PRIMARY KEY,
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
            id BIGSERIAL PRIMARY KEY,
            source TEXT,
            reqid INT,
            recv_time TIMESTAMP WITHOUT TIME ZONE,
            bar_time NUMERIC,
            bar_open_ NUMERIC,
            bar_high NUMERIC,
            bar_low NUMERIC,
            bar_close NUMERIC,
            bar_volume NUMERIC,
            bar_wap NUMERIC,
            bar_count INT
        )"""
    table_names.append(['rtb'])  
    table_creation_commands.append(create_real_time_bars)
    #rtb_table_initialization = "ALTER TABLE your_table ADD COLUMN id BIGSERIAL PRIMARY KEY;"
    #table_initialization_commands.append(rtb_table_initialization)

    # type = right from contract objecy
    create_positions_table = """
        CREATE TABLE IF NOT EXISTS positions (
            id BIGSERIAL PRIMARY KEY,
            source TEXT,
            recv_time TIMESTAMP WITHOUT TIME ZONE,
            account TEXT,
            position NUMERIC,
            avg_cost NUMERIC,
            symbol TEXT,
            sec_type TEXT,
            last_trade_date_or_contract_month TEXT,
            strike NUMERIC,
            type TEXT,
            multiplier TEXT,
            sec_id_type TEXT,
            sec_id TEXT,
            description TEXT
        )"""
    # not doing anything with these yet
    #ComboLegsDescription
    #ComboLegs	List
    #DeltaNeutralContract
    table_names.append(['positions'])
    table_creation_commands.append(create_positions_table)
    #position_table_initialization = "ALTER TABLE your_table ADD COLUMN id BIGSERIAL PRIMARY KEY;"
    #table_initialization_commands.append(position_table_initialization)

    return table_names, table_creation_commands, table_initialization_commands



    # # type = right from contract objecy
    # create_positions_table = """
    #     CREATE TABLE IF NOT EXISTS positions (
    #         id BIGSERIAL PRIMARY KEY,
    #         source TEXT,
    #         recv_time TIMESTAMP WITHOUT TIME ZONE,
    #         account TEXT,
    #         position NUMERIC,
    #         avg_cost NUMERIC,
    #         symbol TEXT,
    #         sec_type TEXT,
    #         last_trade_date_or_contract_month TEXT,
    #         strike NUMERIC,
    #         type TEXT,
    #         multiplier TEXT,
    #         sec_id_type TEXT,
    #         sec_id TEXT,
    #         description TEXT
    #     )"""
    

    # create_position_table = """
    #     CREATE TABLE IF NOT EXISTS position (
    #         source TEXT,
    #         account TEXT,
    #         position NUMERIC,
    #         avg_cost NUMERIC,
    #         conid INT,
    #         Symbol TEXT,
    #         SecType TEXT,
    #         LastTradeDateOrContractMonth TEXT,
    #         LastTradeDate TEXT,
    #         Strike NUMERIC,
    #         Right TEXT,
    #         Multiplier TEXT,
    #         Exchange TEXT,
    #         Currency TEXT,
    #         LocalSymbol TEXT,
    #         PrimaryExch TEXT,
    #         TradingClass TEXT,
    #         IncludeExpired BOOLEAN,
    #         SecIdType TEXT,
    #         SecId TEXT,
    #         Description TEXT,
    #         IssuerId TEXT,
    #     )"""
    # # not doing anything with these yet
    # #ComboLegsDescription
    # #ComboLegs	List
    # #DeltaNeutralContract



