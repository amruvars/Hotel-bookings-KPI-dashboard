create database Hotel_DB;

CREATE or replace STORAGE INTEGRATION azure_adls
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = 'AZURE'
ENABLED = TRUE
AZURE_TENANT_ID = 'ebfabf26-4e7f-4ae3-ac03-c3d71766e261' --tenant id from that azure account
STORAGE_ALLOWED_LOCATIONS = (
    'azure://saazureproject.blob.core.windows.net/bronze/customers/'  --location where data is present
);

CREATE OR REPLACE STAGE adls_bronze_stage  --create a external stage 
URL = 'azure://saazureproject.blob.core.windows.net/bronze/customers/'
STORAGE_INTEGRATION = azure_adls;
LIST @adls_bronze_stage;
create or replace file format FF_CSV
    type = 'CSV'
    field_optionally_enclosed_by='''' --if anyname in the table is in quotes ignore quotes and load only text.
    Skip_header=1  --headings will be not loaded as data
    NULL_if=('NULL','null','') --replace the data if it is null with NULL
create or replace table Bronze_Hotel_booking(
booking_id STRING,
hotel_id STRING,
hotel_city	STRING,
customer_id	STRING,
customer_name STRING,
customer_email STRING,
check_in_date STRING,
check_out_date STRING,
room_type STRING,
num_guests STRING,
total_amount STRING,
currency STRING,	
booking_status STRING
);

COPY INTO Bronze_Hotel_booking
FROM @adls_bronze_stage
files=('hotel_bookings_raw.csv')
FILE_FORMAT = FF_CSV
ON_ERROR = 'ABORT_STATEMENT';


SELECT * from BRONZE_HOTEL_BOOKING limit 50;


create or replace table SILVER_HOTEL_BOOKINGS(
 bookingid VARCHAR,
 hotel_id VARCHAR,
 hotel_city	VARCHAR,
 customer_id VARCHAR,
 customer_name VARCHAR,
 customer_email VARCHAR,
 check_in_date DATE,
 check_out_date DATE,
 room_type VARCHAR,
 num_guests INT,
 total_amount DOUBLE,
 currency VARCHAR,	
 booking_status VARCHAR
);

SELECT customer_email
FROM BRONZE_HOTEL_BOOKING
WHERE NOT (customer_email like '%@%.%')
or customer_email is null;

select total_amount 
from bronze_hotel_booking
where TRY_TO_NUMBER(total_amount)<0 or total_amount is null;

select check_in_date,check_out_date 
from bronze_hotel_booking
where TRY_TO_DATE(check_in_date) > TRY_TO_DATE(check_out_date) or check_in_date is null;

SELECT booking_status
from bronze_hotel_booking
where booking_status NOT IN ('Confirmed','No-Show','Cancelled');

--inserting data into silver table
INSERT INTO SILVER_HOTEL_BOOKINGS
SELECT 
 booking_id,
 hotel_id,
 INITCAP(TRIM(hotel_city)) AS hotel_city,
 customer_id,
 INITCAP(TRIM(customer_name)) AS customer_name,
 case 
    when customer_email LIKE '%@%.%' THEN LOWER(TRIM(customer_email))
    else NULL
end as customer_email,
 TRY_TO_DATE((NULLif(check_in_date,' '))) as check_in_date,
 TRY_TO_DATE((NULLif(check_out_date,' '))) as check_out_date,
 room_type,
 num_guests,
 ABS(total_amount) as total_amount,
 currency,	
 case 
    when Lower(booking_status) in ('confirmeeed','confirmeed','confirmd') THEN 'Confirmed'
    Else booking_status
end as booking_status

FROM BRONZE_HOTEL_BOOKING
WHERE 
    try_to_date(check_in_date) is not null 
    and try_to_date(check_out_date) is not null
    and try_to_date(check_in_date) < try_to_date(check_out_date);


select * from silver_hotel_bookings limit 20;

