# Data Dictionary

## Dimensions

### Vehicle Dimension (dim_vehicles)

| Field Name | Data Type | Description | Example |
| -----------|-----------|-------------|---------|
| vehicle_sk | INT | Surrogate Key of each vehicle | 1 |
| vehicle_nk | INT | Natural Key | 2 |
| vehicle_model_fk | INT | Foreign Key referencing the Vehicle Model from dim_vehicle_models | 1 |
| company_fk | INT | Foreign Key referencing the company from dim_compabnies | 1 |
| vehicle_type_name | VARCHAR(255) | model name of the vehicle | E-Smart 30 kW |
| vehicle_identification_number | VARCHAR(50) | The unique identification number of this vehicle | ZFA31200000618611 |
| registration_plate | VARCHAR(25) | the registration plate number | HH-EM 3017 |
| serial_number | VARCHAR(50) | the cars serial number | 77450 |
| kw | INT | the amount of kw the car has | 70 |
| fuel_type_name | VARCHAR(25) | the type of fuel the vehicle uses | Strom |
| ownership_type | VARCHAR(50) |  | Langzeitmiete |
| capacity_amount | VARCHAR(10) | the amount of fuel the vehicle is able to take | 55 l |
| access_control_component_type | VARCHAR(50) | how access control is handled | Invers BCSA 2006 GPRS |
