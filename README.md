# Udacity Data Engineering Capstone Project
## Project Description

The goal of this project is to pull data from at least 2 different sources and to prepare an analytical data model.
1. Data related to Carsharing Bookings and Cars from Deutsche Bahn: https://data.deutschebahn.com/dataset/data-flinkster 
2. Weather Data from german weather stations gathered from DWD: https://opendata.dwd.de/climate_environment/CDC/derived_germany/soil/daily/historical/

The following questions should be answered:
* Which cities are the most successful ones related to the usage of Car Sharing?
* How long is the average, longest and shortest distance for a Car sharing trip?
* Is there a relation between the number of car sharing usages and temperatures?

### Data assessment
* The Car Sharing data is available for bookings between June 2013 and May 2017
* Weather data is available for 487 weather stations between January 1991 and December 2019 
* As there isn't a weather station available in each city, temperatures can't be matched to all car bookings
* Boolean values are given as german 'Ja/Nein' in the booking data, this will be translated to Boolean 1 & 0
* latitude and longitude values are given with ',' ac decimal separator and therefor can't be read in as Decimal in the first place
* some columns appear occasional empty, default values are applied

### Target Data model

![Data Model](resources/img/db-diagram.png "Data Model")

The above ER-Diagram shows the target Data Model that has been designed in order to answer the given questions above.
It contains of 1 Fact and 7 Dimension Tables. The Fact Table (`fact_bookings) contains metrics about the duration and the distance of a booked car sharing trip. 


### ETL pipeline
There are two pipelines available, one taking care of initializing the Database and one for populating the data. 

#### Initialization
![Init DAG](resources/img/init_main.png "Init DAG")

![Init Stage SubDAG](resources/img/init_stage.png "Init Stage SubDAG") 

![Init Dims SubDAG](resources/img/init_dims.png "Init Dims SubDAG")

![Init Facts SubDAG](resources/img/init_facts.png "Init Facts SubDAG")

#### Data Load
![Data Load DAG](resources/img/load_main.png "Data Load DAG")

![Data Load Stage SubDAG](resources/img/load_stage.png "Data Load Stage SubDAG") 

![Data Load Dims SubDAG](resources/img/load_dims.png "Data Load Dims SubDAG")

![Data Load Facts SubDAG](resources/img/load_facts.png "Data Load Facts SubDAG")

### Analytical Queries

### Choice of technologies
For this project, Airflow was chosen because it allows us to build complex pipelines in a modular manner. 
Different stages can be separated into tasks with specified dependencies between them. With setting up the dependencies, 
we can easily manage which tasks can run in parallel and which need to run in sequential order.
The Airflow UI enables us to analyse the individual runs of a pipeline and one can easily check on failures and observe 
logfiles.

Amazon Redshift has been chosen as a Cloud Data Warehouse because of its scalability as well as its ease of use. 
Having a higher amount of data to process, one can easily increase the amount of processing nodes as well as their size. 
Since there is built-in support to load data from S3, it has been chosen to store the raw data.  

## next steps
* 100x
* 7am
* 100+ users

## Setup 
### Running the project