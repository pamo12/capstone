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

CREATE_TABLE_DIM_VEHICLES = """
    CREATE TABLE public.dim_vehicles (
        vehicle_sk INT IDENTITY(0,1) PRIMARY KEY,
        vehicle_nk INT NOT NULL,
        vehicle_model_fk INT NOT NULL,
        company_fk INT NOT NULL,
        vehicle_type_name VARCHAR(255),
        vehicle_identification_number VARCHAR(50),
        registration_plate VARCHAR(25),
        serial_number VARCHAR(50),
        kw INT,
        fuel_type_name VARCHAR(25),
        ownership_type VARCHAR(50),
        capacity_amount INT,
        access_control_component_type VARCHAR(50)
    );
"""

CREATE_TABLE_DIM_VEHICLE_MODELS = """
    CREATE TABLE public.dim_vehicle_models (
        vehicle_model_sk INT IDENTITY(0,1) PRIMARY KEY,
        vehicle_manufacturer VARCHAR(50),
        vehicle_model_type VARCHAR(50),
        vehicle_model_name VARCHAR(50)
    );
"""

CREATE_TABLE_DIM_RENTAL_ZONES = """
    CREATE TABLE public.dim_rental_zones (
        rental_zone_sk INT IDENTITY(0,1) PRIMARY KEY,
        rental_zone_nk INT NOT NULL,
        rental_zone_src VARCHAR(50),
        company_fk INT NOT NULL,
        name VARCHAR(255),
        code VARCHAR(255),
        type VARCHAR(50),
        city VARCHAR(50),
        country VARCHAR(50),
        latitude DECIMAL,
        longitude DECIMAL,
        is_airport_x BOOLEAN,
        is_long_distance_trains_x BOOLEAN,
        is_suburban_trains_x BOOLEAN,
        is_underground_x BOOLEAN,
        is_active BOOLEAN
    );
"""

CREATE_TABLE_DIM_COMPANIES = """
    CREATE TABLE public.dim_companies (
        company_sk INT IDENTITY(0,1) PRIMARY KEY,
        company VARCHAR(255),
        company_group VARCHAR(255)
    );
"""

CREATE_TABLE_DIM_CATEGORIES = """
    CREATE TABLE public.dim_categories (
        category_sk INT IDENTITY(0,1) PRIMARY KEY,
        category_nk INT NOT NULL,
        company_fk INT NOT NULL,
        category VARCHAR(255)
    );
"""

CREATE_TABLE_DIM_DATE = """
    CREATE TABLE public.dim_date (
        date_sk INT PRIMARY KEY
    );
"""