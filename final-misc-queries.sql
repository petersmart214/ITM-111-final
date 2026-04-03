use ev_charger;
SET SESSION net_read_timeout = 120;
SET SESSION net_write_timeout = 120;

#Make sure to set your SQL editor preferences to not timeout (set DBMS connection read timeout to 0)

SELECT venue, count(charger_id) as `c` FROM ev_charger.charger where charger.charger_type = "DCFC" group by venue order by `c`;

#This Query pulls the average duration verses average energy pull grouped by region.
select region.region_name, round(avg(session.total_duration), 3) as `Average Duration`, round(avg(session.energy_kwh), 3) as `Average Energy Pull` from region right join (charger right join session on charger.charger_id = session.charger_id) on charger.region_id = region.region_id group by region.region_id order by `Average Duration`;

#This Query finds the average duration by charger type (DCFC is DC fast charger and L2 is Level 2)
select charger.charger_type, round(avg(session.charge_duration), 3) as `Average Charge Duration`, round(avg(session.total_duration), 3) as `Average Session Duration` from region right join (charger right join session on charger.charger_id = session.charger_id) on charger.region_id = region.region_id group by charger.charger_type order by `Average Charge Duration`;

#Histogram of how many sessions started at a certain hour. Shows a clear tendency towards midday starting times.
select time(DATE_FORMAT(session.start_datetime, '%Y-%m-%d %H:00:00')) as `Start Time`, count(session.session_id) from session group by `Start Time` order by `Start Time`;

#Histogram of sessions that use a DCFC charger
select HOUR(session.start_datetime) as `Start Time`, count(session.session_id) as `DCFC Start Counts` from charger join session on session.charger_id = charger.charger_id where charger.charger_type = "DCFC" group by `Start Time` order by `Start Time`;

#Histogram of sessions that use a L2 charger (this one takes a REALLY long time to run. I tried to optimize it somewhat but... didnt work as well)
select HOUR(session.start_datetime) as `Start Time`, count(session.session_id) as `L2 Start Counts` from charger join session on session.charger_id = charger.charger_id where charger.charger_type = "L2" group by `Start Time` order by `Start Time`;

#This was to verify the data does not contain significant anomolies, as it was suprising how many charging sessions were at 3am.
select * from session where time(session.start_datetime) >= '03:00:00' and time(session.start_datetime) < '04:00:00';

#This is used to show counts of charger venues
SELECT venue, count(charger_id) as `c` FROM ev_charger.charger group by venue order by `c`;