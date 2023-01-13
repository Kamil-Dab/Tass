WITH city_dest_pass as (
SELECT split_part(b.city,'/',1) as dest_city, b.state_id, 
count(*) as flights_count, sum(fl.passengers) as passengers_sum from flights_flight as fl
left join (SELECT code, split_part(description, ',', 1) AS city, 
split_part(split_part(description, ',', 2),':',1) as state_id
FROM flights_airport) as b
on fl.dest_airport_id = b.code
group by b.city, b.state_id
order by passengers_sum)

Select a.dest_city, a.state_id, a.flights_count, a.passengers_sum, b.population, 
b.density, cast(a.passengers_sum as float)/b.population as ratio_pass_sum, 
cast(a.flights_count as float)/b.population as ratio_flights_count from city_dest_pass as a
inner join cities_city as b on a.dest_city = b.city and replace(a.state_id,' ','') = b.state_id
order by ratio_pass_sum desc;