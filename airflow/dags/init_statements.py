DROP_TABLE_STAGE_VEHICLES = """
    DROP TABLE IF EXISTS public.stage_vehicles;
"""

DROP_TABLE_STAGE_RENTAL_ZONES = """
    DROP TABLE IF EXISTS public.stage_rental_zones;
"""

DROP_TABLE_STAGE_CATEGORIES = """
    DROP TABLE IF EXISTS public.stage_categories;
"""

DROP_TABLE_STAGE_BOOKINGS = """
    DROP TABLE IF EXISTS public.stage_bookings;
"""

CREATE_TABLE_STAGE_VEHICLES = """
    CREATE TABLE public.stage_vehicles (
        vehicle_hal_id INT,
        vehicle_model_type VARCHAR(50),
        vehicle_manufacturer_name VARCHAR(50),
        vehicle_model_name VARCHAR(50),
        vehicle_type_name VARCHAR(255),
        vin VARCHAR(50),
        registration_plate VARCHAR(25),
        serial_number VARCHAR(50),
        kw VARCHAR(5),
        fuel_type_name VARCHAR(25),
        ownership_type VARCHAR(50),
        capacity_amount VARCHAR(50),
        access_control_component_type VARCHAR(50),
        company VARCHAR(255),
        company_group VARCHAR(255)
    );
"""

CREATE_TABLE_STAGE_RENTAL_ZONES = """
    CREATE TABLE public.stage_rental_zones (
        rental_zone_hal_id INT,
        rental_zone_hal_src VARCHAR(50),
        name VARCHAR(255),
        code VARCHAR(255),
        type VARCHAR(50),
        city VARCHAR(50),
        country VARCHAR(50),
        latitude VARCHAR(25),
        longitude VARCHAR(25),
        poi_airport_x VARCHAR(5),
        poi_long_distance_trains_x VARCHAR(5),
        poi_suburban_trains_x VARCHAR(5),
        poi_underground_x VARCHAR(5),
        active_x VARCHAR(5),
        company VARCHAR(255),
        company_group VARCHAR(255)
    );
"""

CREATE_TABLE_STAGE_CATEGORIES = """
    CREATE TABLE public.stage_categories (
        hal_id INT,
        category VARCHAR(255),
        company VARCHAR(255),
        company_group VARCHAR(255)
    );
"""

CREATE_TABLE_STAGE_BOOKINGS = """
    CREATE TABLE public.stage_bookings (
        booking_hal_id INT,
        category_hal_id INT,
        vehicle_hal_id INT,
        customer_hal_id VARCHAR(50),
        date_booking DATETIME,
        date_from DATETIME,
        date_until DATETIME,
        compute_extra_booking_fee VARCHAR(5),
        traverse_use VARCHAR(5),
        distance INT,
        start_rental_zone VARCHAR(255),
        start_rental_zone_hal_id INT,
        end_rental_zone VARCHAR(255),
        end_rental_zone_hal_id INT,
        rental_zone_hal_src VARCHAR(50),
        city_rental_zone VARCHAR(50),
        technical_income_channel VARCHAR(50)
    );
"""

DROP_TABLE_DIM_VEHICLES = """
    DROP TABLE IF EXISTS public.dim_vehicles;
"""

DROP_TABLE_DIM_VEHICLE_MODELS = """
    DROP TABLE IF EXISTS public.dim_vehicle_models;
"""

DROP_TABLE_DIM_RENTAL_ZONES = """
    DROP TABLE IF EXISTS public.dim_rental_zones;
"""

DROP_TABLE_DIM_COMPANIES = """
    DROP TABLE IF EXISTS public.dim_companies;
"""

DROP_TABLE_DIM_CATEGORIES = """
    DROP TABLE IF EXISTS public.dim_categories;
"""

DROP_TABLE_DIM_DATE = """
    DROP TABLE IF EXISTS public.dim_date;
"""

DROP_TABLE_DIM_WEATHER = """
    DROP TABLE IF EXISTS public.dim_weather;
"""

CREATE_TABLE_DIM_VEHICLES = """
    CREATE TABLE public.dim_vehicles (
        vehicle_sk INT IDENTITY(0,1) PRIMARY KEY,
        vehicle_nk INT NOT NULL DEFAULT 0,
        vehicle_model_fk INT NOT NULL DEFAULT 0,
        company_fk INT NOT NULL DEFAULT 0,
        vehicle_type_name VARCHAR(255) DEFAULT '--',
        vehicle_identification_number VARCHAR(50) DEFAULT '--',
        registration_plate VARCHAR(25) DEFAULT '--',
        serial_number VARCHAR(50) DEFAULT '--',
        kw INT DEFAULT 0,
        fuel_type_name VARCHAR(25) DEFAULT '--',
        ownership_type VARCHAR(50) DEFAULT '--',
        capacity_amount VARCHAR(10) DEFAULT '--',
        access_control_component_type VARCHAR(50) DEFAULT '--'
    );
"""

CREATE_TABLE_DIM_VEHICLE_MODELS = """
    CREATE TABLE public.dim_vehicle_models (
        vehicle_model_sk INT IDENTITY(0,1) PRIMARY KEY,
        vehicle_manufacturer VARCHAR(50) DEFAULT '--',
        vehicle_model_type VARCHAR(50) DEFAULT '--',
        vehicle_model_name VARCHAR(50) DEFAULT '--'
    );
"""

CREATE_TABLE_DIM_RENTAL_ZONES = """
    CREATE TABLE public.dim_rental_zones (
        rental_zone_sk INT IDENTITY(0,1) PRIMARY KEY,
        rental_zone_nk INT NOT NULL DEFAULT 0,
        rental_zone_src VARCHAR(50) DEFAULT '--',
        company_fk INT NOT NULL DEFAULT 0,
        name VARCHAR(255) DEFAULT '--',
        code VARCHAR(255) DEFAULT '--',
        type VARCHAR(50) DEFAULT '--',
        city VARCHAR(50) DEFAULT '--',
        country VARCHAR(50) DEFAULT '--',
        latitude VARCHAR(25) DEFAULT '0',
        longitude VARCHAR(25) DEFAULT '0',
        is_airport_x BOOLEAN DEFAULT 0,
        is_long_distance_trains_x BOOLEAN DEFAULT 0,
        is_suburban_trains_x BOOLEAN DEFAULT 0,
        is_underground_x BOOLEAN DEFAULT 0, 
        is_active BOOLEAN DEFAULT 0
    );
"""

CREATE_TABLE_DIM_COMPANIES = """
    CREATE TABLE public.dim_companies (
        company_sk INT IDENTITY(0,1) PRIMARY KEY,
        company VARCHAR(255) DEFAULT '--',
        company_group VARCHAR(255) DEFAULT '--'
    );
"""

CREATE_TABLE_DIM_CATEGORIES = """
    CREATE TABLE public.dim_categories (
        category_sk INT IDENTITY(0,1) PRIMARY KEY,
        category_nk INT NOT NULL DEFAULT 0,
        company_fk INT NOT NULL DEFAULT 0,
        category VARCHAR(255) DEFAULT '--'
    );
"""

CREATE_TABLE_DIM_DATE = """
    CREATE TABLE public.dim_date (
        date_sk INT IDENTITY(0,1) PRIMARY KEY,
        date_value Date NOT NULL DEFAULT '1900-01-01',
        year_number SMALLINT NOT NULL DEFAULT 0,
        year_week_number SMALLINT NOT NULL DEFAULT 0,
        year_day_number SMALLINT NOT NULL DEFAULT 0,
        quarter_number SMALLINT NOT NULL DEFAULT 0,
        month_number SMALLINT NOT NULL DEFAULT 0,
        month_name CHAR(9) NOT NULL DEFAULT '--',
        month_day_number SMALLINT NOT NULL DEFAULT 0,
        week_day_number SMALLINT NOT NULL DEFAULT 0,
        day_name CHAR(9) NOT NULL DEFAULT '--',
        is_weekend SMALLINT NOT NULL DEFAULT 0
    );
"""

CREATE_TABLE_DIM_WEATHER = """
    CREATE TABLE public.dim_weather (
        weather_sk INT IDENTITY(0,1) PRIMARY KEY,
        date_value INT NOT NULL DEFAULT 19000101,
        station_nk INT NOT NULL DEFAULT 0,
        city VARCHAR(50) DEFAULT '--',
        width DECIMAL(8,2) DEFAULT 0.0,
        length DECIMAL(8,2) DEFAULT 0.0,
        temperature DECIMAL(10,2) DEFAULT 0.0
    );
"""

DROP_TABLE_FACT_BOOKINGS = """
    DROP TABLE IF EXISTS fact_bookings;
"""

CREATE_TABLE_FACT_BOOKINGS = """
    CREATE TABLE fact_bookings (
        booking_nk INT NOT NULL PRIMARY KEY,
        category_fk INT,
        vehicle_fk INT,
        date_booking_fk INT,
        weather_fk INT,
        date_from_fk INT,
        date_until_fk INT,
        start_rental_zone_fk INT,
        end_rental_zone_fk INT,
        distance DECIMAL, 
        duration INT,
        is_traverse_use BOOLEAN,
        is_extra_booking_fees BOOLEAN,
        technical_income_channel VARCHAR(50)
    );
"""

DROP_TABLE_STAGE_WEATHER_STATIONS = """
    DROP TABLE IF EXISTS stage_weather_stations;
"""

CREATE_TABLE_STAGE_WEATHER_STATIONS = """
    CREATE TABLE stage_weather_stations (
        station_id INT NOT NULL PRIMARY KEY,
        height INT,
        width DECIMAL(8,2),
        length DECIMAL(8,2),
        name VARCHAR(50),
        country VARCHAR(50)
    );
"""

DROP_TABLE_STAGE_WEATHER_DATA = """
    DROP TABLE IF EXISTS stage_weather_data;
"""

CREATE_TABLE_STAGE_WEATHER_DATA = """
    CREATE TABLE stage_weather_data (
        station_id INT NOT NULL,
        date_value INT NOT NULL,
        vgsl DECIMAL(10,2),
        vpgb DECIMAL(10,2),
        vpgh DECIMAL(10,2),
        ts05 DECIMAL(10,2),
        ts10 DECIMAL(10,2),
        ts20 DECIMAL(10,2),
        ts50 DECIMAL(10,2),
        ts100 DECIMAL(10,2),
        zfumi INT,
        bf10 INT,
        bf20 INT,
        bf30 INT,
        bf40 INT,
        bf50 INT,
        bf60 INT,
        bfgsl INT,
        bfgls INT,
        tsls05 DECIMAL(10,2),
        tssl05 DECIMAL(10,2),
        ztkmi INT,
        ztumi INT,
        vpgpm DECIMAL(10,2),
        vpmb DECIMAL(10,2),
        vpwb DECIMAL(10,2),
        vpzb DECIMAL(10,2),
        vgl DECIMAL(10,2),
        vwls DECIMAL(10,2),
        vwsl DECIMAL(10,2),
        bfwls INT,
        bfwsl INT,
        eor VARCHAR(5)
    );
"""