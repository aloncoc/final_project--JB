DROP FUNCTION get_airline_by_username;
CREATE OR REPLACE FUNCTION get_airline_by_username(_username text)
RETURNS TABLE(id bigint, name text,country_id bigint, user_id bigint)
LANGUAGE plpgsql AS
    $$
        BEGIN
           	RETURN QUERY
            SELECT a.id, a.name, a.country_id, a.user_id
            FROM airline_companies a
            JOIN users u ON a.user_id = u.id
            WHERE _username = u.username;
        END;
    $$;
---------------------------
SELECT * FROM get_airline_by_username('Elad');
---------
CREATE OR REPLACE FUNCTION get_customer_by_username(_username text)
RETURNS TABLE(id bigint, first_name text,last_name text, address text, phone_no text, credit_card_no text, user_id bigint)
LANGUAGE plpgsql AS
    $$
        BEGIN
           	RETURN QUERY
            SELECT c.id, c.first_name, c.last_name, c.address, c.phone_no, c.credit_card_no, c.user_id
            FROM customers c
            JOIN users u ON c.user_id = u.id
            WHERE _username = u.username;
        END;
    $$;
select * from get_customer_by_username('Yosi');
----------

CREATE OR REPLACE FUNCTION get_user_by_username(_username text)
RETURNS TABLE(id bigint, username text, password text, email text, user_role integer)
LANGUAGE plpgsql AS
    $$
        BEGIN
           	RETURN QUERY
            SELECT u.id, u.username, u.password, u.email, u.user_role
			FROM users u
            WHERE _username = u.username;
        END;
    $$;
------------------------
SELECT * FROM get_user_by_username('alonc');



CREATE OR REPLACE FUNCTION get_flights_by_parameters(_origin_country_id bigint, _destination_country_id bigint, _date timestamp)
RETURNS TABLE(id bigint, airline_company_id bigint, origin_country_id bigint, destination_country_id bigint, departure_time timestamp, landing_time timestamp, remaining_tickets bigint)
LANGUAGE plpgsql AS
    $$
        BEGIN
           	RETURN QUERY
            SELECT f.id, f.airline_company_id, f.origin_country_id, f.destination_country_id, f.departure_time, f.landing_time, f.remaining_tickets
            FROM flights f
            WHERE _origin_country_id = f.origin_country_id
			AND _destination_country_id = f.destination_country_id
			AND _date = f.departure_time;
        END;
    $$;
-----------------------------
SELECT * FROM get_flights_by_parameters(1, 3, '2022-01-30 16:00:00');
------------------------


CREATE OR REPLACE FUNCTION get_flights_by_airline_id(_airline_id bigint)
RETURNS TABLE(id bigint, airline_company_id bigint, origin_country_id bigint, destination_country_id bigint, departure_time timestamp, landing_time timestamp, remaining_tickets bigint)
LANGUAGE plpgsql AS
    $$
        BEGIN
           	RETURN QUERY
            SELECT f.id, f.airline_company_id, f.origin_country_id, f.destination_country_id, f.departure_time, f.landing_time, f.remaining_tickets
            FROM flights f
            WHERE _airline_id = f.airline_company_id;
        END;
    $$;
SELECT * FROM get_flights_by_airline_id(2);
|||
DROP FUNCTION get_arrival_flights;
CREATE OR REPLACE FUNCTION get_arrival_flights(_country_id int)
RETURNS TABLE(id bigint, airline_company_id bigint, origin_country_id bigint, destination_country_id bigint, departure_time timestamp, landing_time timestamp, remaining_tickets integer)
LANGUAGE plpgsql AS
    $$
        BEGIN
           	RETURN QUERY
            SELECT f.id, f.airline_company_id, f.origin_country_id, f.destination_country_id, f.departure_time, f.landing_time, f.remaining_tickets
            FROM flights f
            WHERE _country_id = f.destination_country_id
			AND f.landing_time <= CURRENT_TIMESTAMP + interval '12' HOUR;
        END;
    $$;

SELECT * FROM get_arrival_flights(2);

|||
CREATE OR REPLACE FUNCTION get_departure_flights(_country_id int)
RETURNS TABLE(id bigint, airline_company_id bigint, origin_country_id bigint, destination_country_id bigint, departure_time timestamp, landing_time timestamp, remaining_tickets integer)
LANGUAGE plpgsql AS
    $$
        BEGIN
           	RETURN QUERY
            SELECT f.id, f.airline_company_id, f.origin_country_id, f.destination_country_id, f.departure_time, f.landing_time, f.remaining_tickets
            FROM flights f
            WHERE _country_id = f.origin_country_id
			AND f.departure_time <= CURRENT_TIMESTAMP + interval '12' HOUR;
        END;
    $$;

SELECT * FROM get_departure_flights(2);


|||
CREATE OR REPLACE FUNCTION get_tickets_by_customer(_customer_id bigint)
RETURNS TABLE(id bigint, flight_id bigint, customer_id bigint)
LANGUAGE plpgsql AS
    $$
        BEGIN
           	RETURN QUERY
            SELECT t.id, t.flight_id, t.customer_id
            FROM tickets t
            JOIN customers c ON t.customer_id = c.id
            WHERE _customer_id = c.id;
        END;
    $$;

SELECT * FROM get_tickets_by_customer(1);
