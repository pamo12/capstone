# Data Dictionary

## Dimensions

### Vehicle Dimension (dim_vehicles)

| Field Name | Data Type | Description | Example |
| -----------|-----------|-------------|---------|
| vehicle_sk | INT | Surrogate Key of each vehicle | 1 |
| vehicle_nk | INT | Natural Key | 2 |
| vehicle_model_fk | INT | Foreign Key referencing the Vehicle Model from dim_vehicle_models | 1 |
| company_fk | INT | Foreign Key referencing the company from dim_companies | 1 |
| vehicle_type_name | VARCHAR(255) | model name of the vehicle | E-Smart 30 kW |
| vehicle_identification_number | VARCHAR(50) | The unique identification number of this vehicle | ZFA31200000618611 |
| registration_plate | VARCHAR(25) | the registration plate number | HH-EM 3017 |
| serial_number | VARCHAR(50) | the cars serial number | 77450 |
| kw | INT | the amount of kw the car has | 70 |
| fuel_type_name | VARCHAR(25) | the type of fuel the vehicle uses | Strom |
| ownership_type | VARCHAR(50) |  | Langzeitmiete |
| capacity_amount | VARCHAR(10) | the amount of fuel the vehicle is able to take | 55 l |
| access_control_component_type | VARCHAR(50) | how access control is handled | Invers BCSA 2006 GPRS |


### Vehicle Model Dimension (dim_vehicle_models)

| Field Name | Data Type | Description | Example |
| -----------|-----------|-------------|---------|
| vehicle_model_sk | INT | Surrogate Key of each vehicle model | 1 |
| vehicle_manufacturer | VARCHAR(50) | the name of the vehicle manufacturer | Opel |
| vehicle_model_type | VARCHAR(50) | the type of vehicle, whether it is a car or a motorbike | Auto |
| vehicle_model_name | VARCHAR(50) | the name of the vehicle model | Insignia |


### Company Dimension (dim_companies)

| Field Name | Data Type | Description | Example |
| -----------|-----------|-------------|---------|
| company_sk | INT | Surrogate Key of each company | 1 |
| company | VARCHAR(255) | the name of the company a vehicle/booking/rental zone belongs to | Flinkster (Endkd.) |
| company_group | VARCHAR(255) | the name of the company group a company belongs to | DB Fuhrpark |


### Category Dimension (dim_categories)

| Field Name | Data Type | Description | Example |
| -----------|-----------|-------------|---------|
| category_sk | INT | Surrogate Key of each category | 1 |
| category_nk | INT | the natural key of each category | 100004 |
| company_fk | INT | the foreign key of the company a category belongs to | 2 |
| category | VARCHAR(255) | the name of the category | Kompaktklasse Flughafen |


### Weather Dimension (dim_weather)

| Field Name | Data Type | Description | Example |
| -----------|-----------|-------------|---------|
| weather_sk | INT | Surrogate Key of each weather entry | 1 |
| date_value | INT | the date to which the weather entry belongs | 19910117 |
| station_nk | INT | the natural key of the weather station | 1048 |
| city | VARCHAR(50) | the name of the city the temperature has been measured | Dresden |
| width | DECIMAL | the longitude of the corresponding weather station | 51.13 |
| length | DECIMAL | the latitude of the corresponding weather station | 13.75 |
| temperature | DECIMAL | the temperature value in °C | 1.20 |


### Rental Zone Dimension (dim_rental_zones)

| Field Name | Data Type | Description | Example |
| -----------|-----------|-------------|---------|
| rental_zone_sk | INT | Surrogate Key of each rental zone | 1 |
| rental_zone_nk | INT | Natural Key of the rental zone | 406277 |
| rental_zone_src | VARCHAR(50) | part of the natural key | Station |
| company_fk | INT | Foreign Key referencing the company from dim_companies | 2 |
| name | VARCHAR(255) | the name of the rental zone | Bahnhof-ELEKTRO |
| code | VARCHAR(255) | the short code of the rental zone | BF-ELEKTRO |
| type | VARCHAR(50) | the type of the rental zone | stationbased |
| city | VARCHAR(50) | the name of the city in which the rental zone is located | St. Wendel |
| country | VARCHAR(50) | the name of the country in which the rental zone is located | Deutschland |
| latitude | VARCHAR(25) | the latitude of the rental zones position | 49.156445000000000 |
| longitude | VARCHAR(25) | the longitude of the rental zones position | 7.033782000000000 |
| is_airport_x | BOOLEAN | Indicator whether the rental zone is near an airport | 1 |
| is_long_distance_trains_x | BOOLEAN | Indicator whether the rental zone is near a long distance train station | 1 |
| is_suburban_trains_x | BOOLEAN | Indicator whether the rental zone is near a suburban train station | 0 |
| is_underground_x | BOOLEAN | Indicator whether the rental zone is near the underground | 0 |
| is_active | BOOLEAN | Indicator whether the rental zone is active | 1 |


### Date Dimension (dim_date)

| Field Name | Data Type | Description | Example |
| -----------|-----------|-------------|---------|
| date_sk | INT | Surrogate Key of each date entry | 1 |
| date_value | DATE | Natural Key of the rental zone | 2010-01-08 |
| year_number | SMALLINT | the number of the related year | 2010 |
| year_week_number | SMALLINT | the number of the week within the year | 1 |
| year_day_number | SMALLINT | the number of the day within a year | 10 |
| quarter_number | SMALLINT | the number of the quarter | 1 |
| month_number | SMALLINT | the number of the month | 1 |
| month_name | CHAR(9) | the name of the month | Jan |
| month_day_number | SMALLINT | the number of the day within the month | 10 |
| week_day_number | SMALLINT | the number of the given weekday | 6 |
| day_name | CHAR(9) | the name of the weekday | Sunday |
| is_weekend | BOOLEAN | Indicator whether the date is on a weekend | 1 |
