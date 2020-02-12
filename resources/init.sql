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

CREATE TABLE public.dim_vehicle_models (
        vehicle_model_sk INT IDENTITY(0,1) PRIMARY KEY,
        vehicle_manufacturer VARCHAR(50) DEFAULT '--',
        vehicle_model_type VARCHAR(50) DEFAULT '--',
        vehicle_model_name VARCHAR(50) DEFAULT '--'
    );

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
        latitude VARCHAR(25) DEFAULT '--',
        longitude VARCHAR(25) DEFAULT '--',
        is_airport_x BOOLEAN DEFAULT 0,
        is_long_distance_trains_x BOOLEAN DEFAULT 0,
        is_suburban_trains_x BOOLEAN DEFAULT 0,
        is_underground_x BOOLEAN DEFAULT 0, 
        is_active BOOLEAN DEFAULT 0
    );

CREATE TABLE public.dim_companies (
        company_sk INT IDENTITY(0,1) PRIMARY KEY,
        company VARCHAR(255) DEFAULT '--',
        company_group VARCHAR(255) DEFAULT '--'
    );

CREATE TABLE public.dim_categories (
        category_sk INT IDENTITY(0,1) PRIMARY KEY,
        category_nk INT NOT NULL DEFAULT 0,
        company_fk INT NOT NULL DEFAULT 0,
        category VARCHAR(255) DEFAULT '--'
    );

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

CREATE TABLE fact_bookings (
        booking_nk INT NOT NULL PRIMARY KEY,
        category_fk INT,
        vehicle_fk INT,
        date_booking_fk INT,
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
