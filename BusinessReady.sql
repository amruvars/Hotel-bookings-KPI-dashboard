use database hotel_db;
create table GOLD_AGG_DAILY_BOOKINGS AS
SELECT 
    check_in_date as DATE,
    Count(*) AS total_booking,
    SUM(total_amount) as Total_revenue

from silver_hotel_bookings 
GROUP BY check_in_date
order by date;


create OR REPLACE table GOLD_AGG_HOTEL_CITY_SALES AS
SELECT
hotel_city,
sum(total_amount) as total_revenue,
from silver_hotel_bookings 
GROUP BY hotel_city
order by total_revenue desc;

create table GOLD_BOOKING_CLEAN AS
SELECT 
 bookingid,
 hotel_id,
 hotel_city,
 customer_id,
 customer_name,
 customer_email,
 check_in_date,
 check_out_date,
 room_type,
 num_guests,
 total_amount,
 currency,	
 booking_status
 
 from silver_hotel_bookings;
SELECT * FROM GOLD_BOOKING_CLEAN lIMIT 30
 