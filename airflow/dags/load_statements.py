LOAD_VEHICLE_MODELS = """
    INSERT INTO dim_vehicle_models (vehicle_manufacturer, vehicle_model_type, vehicle_model_name)
    SELECT DISTINCT
        vehicle_manufacturer_name, 
        vehicle_model_type, 
        vehicle_model_name
    FROM stage_vehicles
"""

LOAD_COMPANIES = """
    INSERT INTO dim_companies (company, company_group)
    SELECT DISTINCT company, company_group
    FROM stage_vehicles
"""

LOAD_DATES = """
    INSERT INTO dim_date (date_value, year_number, year_week_number, year_day_number, quarter_number, month_number, month_name,
                        month_day_number, week_day_number, day_name, is_weekend)
    SELECT 
        dat AS date,
        DATE_PART(year,dat) AS year_number,
        DATE_PART(week,dat) AS year_week_number,
        DATE_PART(doy,dat) AS year_day_number,
        DATE_PART(qtr, dat) AS quarter_number,
        DATE_PART(mm,dat) AS month_number,
        TO_CHAR(dat, 'Mon') AS month_name,
        DATE_PART(day,dat) AS month_day_number,
        DATE_PART(dow,dat) AS week_day_number,
        TO_CHAR(dat, 'Day') AS day_name,
        DECODE(DATE_PART(dow,dat),0,true,6,true,false) AS is_weekend
    FROM
        (SELECT
        TRUNC(DATEADD(day, ROW_NUMBER () over ()-1, '2010-01-01')) AS dat
        FROM stage_bookings
        LIMIT 10000
        )
"""

LOAD_CATEGORIES = """
    INSERT INTO dim_categories (category_nk, category, company_fk)
    SELECT ca.hal_id, ca.category, co.company_sk
    FROM stage_categories ca JOIN dim_companies co ON ca.company = co.company AND ca.company_group = co.company_group 
"""

LOAD_VEHICLES = """
    INSERT INTO dim_vehicles (vehicle_nk, vehicle_model_fk, company_fk, vehicle_identification_number, serial_number,
                registration_plate, ownership_type, kw, fuel_type_name, capacity_amount, access_control_component_type)
    SELECT
     v.vehicle_hal_id, vm.vehicle_model_sk, co.company_sk, v.vin, v.serial_number, v.registration_plate, v.ownership_type, 
     CAST(v.kw as INT), v.fuel_type_name, v.capacity_amount, v.access_control_component_type
    FROM stage_vehicles v
    JOIN dim_companies co ON v.company = co.company AND v.company_group = co.company_group
    JOIN dim_vehicle_models vm ON v.vehicle_manufacturer_name = vm.vehicle_manufacturer AND v.vehicle_model_type = vm.vehicle_model_type AND v.vehicle_model_name = vm.vehicle_model_name
"""

LOAD_RENTAL_ZONES = """
    INSERT INTO dim_rental_zones (rental_zone_nk, rental_zone_src, company_fk, name, code, type, city, country,
                latitude, longitude, is_airport_x, is_long_distance_trains_x, is_suburban_trains_x, is_underground_x, is_active)
    SELECT
     rz.rental_zone_hal_id,rz.rental_zone_hal_src,co.company_sk,rz.name,rz.code,rz.type,rz.city,rz.country,
     REPLACE(rz.latitude, ',', '.') as latitude,
     REPLACE(rz.longitude, ',', '.') as longitude,
     DECODE(rz.poi_airport_x, 'Ja', 1, 0) as poi_airport_x,
     DECODE(rz.poi_long_distance_trains_x, 'Ja', 1, 0) as poi_long_distance_trains_x,
     DECODE(rz.poi_suburban_trains_x, 'Ja', 1, 0) as poi_suburban_trains_x,
     DECODE(rz.poi_underground_x, 'Ja', 1, 0) as poi_underground_x,
     DECODE(rz.active_x, 'Ja', 1, 0) as active_x
    FROM stage_rental_zones rz
    JOIN dim_companies co ON rz.company = co.company AND rz.company_group = co.company_group      
"""

LOAD_WEATHER = """
    INSERT INTO dim_weather (date_value, station_nk, city, width, length, temperature)
    SELECT
     swd.date_value,
     sws.station_id,
     sws.name,
     sws.width,
     sws.length,
     swd.ts05
    FROM stage_weather_data swd
    JOIN stage_weather_stations sws ON swd.station_id = sws.station_id 
"""

LOAD_BOOKING_FACTS = """
    SELECT
     b.booking_hal_id,
     CASE WHEN ca.category_sk IS NULL THEN 0 ELSE ca.category_sk END,
     CASE WHEN v.vehicle_sk IS NULL THEN 0 ELSE v.vehicle_sk END,
     CASE WHEN booking.date_sk IS NULL THEN 0 ELSE booking.date_sk END,
     CASE WHEN w.weather_sk IS NULL THEN 0 ELSE w.weather_sk END,
     CASE WHEN start_date.date_sk IS NULL THEN 0 ELSE start_date.date_sk END,
     CASE WHEN end_date.date_sk IS NULL THEN 0 ELSE end_date.date_sk END,
     CASE WHEN start_zone.rental_zone_sk IS NULL THEN 0 ELSE start_zone.rental_zone_sk END,
     CASE WHEN end_zone.rental_zone_sk IS NULL THEN 0 ELSE end_zone.rental_zone_sk END,
     b.distance,
     DATEDIFF(minutes, b.date_from, b.date_until) AS duration,
     DECODE(traverse_use, 'Ja', 1, 0) AS is_traverse_use,
     DECODE(compute_extra_booking_fee, 'Ja', 1, 0) AS is_extra_booking_fee,
     b.technical_income_channel
    FROM stage_bookings b
    LEFT JOIN dim_categories ca ON b.category_hal_id = ca.category_nk
    LEFT JOIN dim_vehicles v ON b.vehicle_hal_id = v.vehicle_nk
    LEFT JOIN dim_date booking ON DATE(b.date_booking) = booking.date_value
    LEFT JOIN dim_date start_date ON DATE(b.date_from) = start_date.date_value
    LEFT JOIN dim_date end_date ON DATE(b.date_until) = end_date.date_value
    LEFT JOIN dim_rental_zones start_zone ON b.start_rental_zone_hal_id = start_zone.rental_zone_nk AND b.rental_zone_hal_src = start_zone.rental_zone_src
    LEFT JOIN dim_rental_zones end_zone ON b.end_rental_zone_hal_id = end_zone.rental_zone_nk AND b.rental_zone_hal_src = end_zone.rental_zone_src
    LEFT JOIN dim_weather w ON start_zone.city = w.city AND to_char(start_date.date_value, 'YYYYmmdd') = w.date_value
"""