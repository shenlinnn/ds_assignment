## booking conversion rate
select experiment_tag, SUM(CASE WHEN booking_status = 'COMPLETED' THEN 1 ELSE 0 END), SUM(CASE WHEN booking_status = 'CREATED' THEN 1 ELSE 0 END)
SUM(CASE WHEN booking_status = 'COMPLETED' THEN 1 ELSE 0 END)/SUM(CASE WHEN booking_status = 'CREATED' THEN 1 ELSE 0 END) AS booking_conversion_rate
from 
(select distinct * from (select order_id, booking_status, driver_id from `ds-assignments.go_ride_allocation.booking_log`)) booking_log
join
(select distinct * from (select order_id, experiment_tag from `ds-assignments.go_ride_allocation.experiment_log`)) experiment_log
on booking_log.order_id = experiment_log.order_id
group by experiment_tag;

## pickup time
select experiment_tag, AVG(pickup_ts - created_ts)/60 mean_pickup_mins from (select experiment_tag, booking_log.order_id,
MAX(CASE WHEN booking_status = 'CREATED' THEN UNIX_SECONDS(booking_log.event_timestamp) ELSE 0 END) created_ts,
MAX(CASE WHEN booking_status = 'PICKED_UP' THEN UNIX_SECONDS(booking_log.event_timestamp) ELSE 0 END) pickup_ts
from 
(select distinct * from (select event_timestamp, order_id, booking_status, driver_id from `ds-assignments.go_ride_allocation.booking_log`)) booking_log
join
(select distinct * from (select order_id, experiment_tag from `ds-assignments.go_ride_allocation.experiment_log`)) experiment_log
on booking_log.order_id = experiment_log.order_id
group by experiment_tag, booking_log.order_id) tmp
where created_ts != 0 and pickup_ts != 0
group by experiment_tag;


## driver acceptance rate
select experiment_tag, accepted/created as acceptance_rate
from (select experiment_tag, 
SUM(CASE WHEN participant_status = 'ACCEPTED' THEN 1 ELSE 0 END) accepted,
SUM(CASE WHEN participant_status = 'CREATED' THEN 1 ELSE 0 END) created
from 
(select distinct * from (select experiment_key, participant_status, order_id, driver_id from `ds-assignments.go_ride_allocation.participant_log`)) participant_log
join
(select distinct * from (select order_id, experiment_tag from `ds-assignments.go_ride_allocation.experiment_log`)) experiment_log
on participant_log.order_id = experiment_log.order_id
group by experiment_tag) tmp;


## cancel rate after dispatch
select experiment_tag, cancel/dispatch
from (select experiment_tag, 
SUM(CASE WHEN booking_status in ('CUSTOMER_CANCELLED','DRIVER_CANCELLED') THEN 1 ELSE 0 END) cancel,
SUM(CASE WHEN booking_status in ('DRIVER_FOUND') THEN 1 ELSE 0 END) dispatch
from 
(select distinct * from `ds-assignments.go_ride_allocation.booking_log` where order_id in (select distinct order_id from `ds-assignments.go_ride_allocation.booking_log` where booking_status = 'DRIVER_FOUND')) booking_log
join
(select distinct * from `ds-assignments.go_ride_allocation.experiment_log`) experiment_log
on booking_log.order_id = experiment_log.order_id
group by experiment_tag) tmp

