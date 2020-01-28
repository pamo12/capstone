LOAD_VEHICLE_MODELS = """
    INSERT INTO dim_vehicle_models (vehicle_manufacturer, vehicle_model_type, vehicle_model_name)
    SELECT DISTINCT vehicle_manufacturer_name, vehicle_model_type, vehicle_model_name
    FROM stage_vehicles
"""

LOAD_COMPANIES = """
    INSERT INTO dim_companies (company, company_group)
    SELECT DISTINCT company, company_group
    FROM stage_vehicles
"""

LOAD_DATES = """
    INSERT INTO dim_date 
    SELECT 1, '2020-01-17', 2020, 1, 1, 1, 1, 'January', 27, 1, 'Monday', 1, 0 
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