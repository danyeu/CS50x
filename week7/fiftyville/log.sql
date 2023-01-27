-- Keep a log of any SQL queries you execute as you solve the mystery.

-- looking at schema
.schema

-- looking at format of crime_scene_reports
SELECT * from crime_scene_reports;
-- looking for this crime
SELECT * from crime_scene_reports WHERE street = "Humphrey Street" AND year = 2021 AND month = 7 AND day = 28;
-- id: 295
-- Tells us the theft took place at 10:15am at a bakery on that street.
-- Interviews took place with 3 different witnesses. Interviews include "bakery"

-- looking at format of interviews
SELECT * from interviews;
-- looking for interviews that mention bakery
SELECT * from interviews WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%";
-- interview ids: 161, 162, 163:
-- 161: Between 10:15 - 10:25, thief escaped by car. Look at CCTV.
-- 162: Before 10:15, thief withdrew money from ATM on Leggett Street.
-- 163: Around 10:15, thief called someone for <1minute. Thief will take the earliest flight out of Fiftyville on the 29th. Accomplice (recipient) will purchase.

-- looking at format of crime_scene_reports
SELECT * from bakery_security_logs;
-- looking for movement withing the crime time frame
SELECT * from bakery_security_logs WHERE activity = "exit" AND year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <=25;
-- potentially entrance is useful?
-- select * from bakery_security_logs where activity = "entrance" and license_plate in (SELECT license_plate from bakery_security_logs WHERE activity = "exit" AND year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <=25);

-- looking at format of atm_transactions
select * from atm_transactions;
-- looking for the specific withdrawal
select * from atm_transactions where year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" and transaction_type = "withdraw";
-- looking at format of bank_accounts
select * from bank_accounts;
-- looking for people that made a withdrawal
select person_id from bank_accounts where account_number in (select account_number from atm_transactions where year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" and transaction_type = "withdraw");

-- looking at format of phone_calls
select * from phone_calls;
-- looking at phone calls on that day <60s
select * from phone_calls where duration < 60 and year = 2021 AND month = 7 AND day = 28;

-- looking at format of airports
select * from airports;
-- looking for id of Fiftyville airport
select id from airports where city = "Fiftyville";
-- looking at format of flights
select * from flights;
-- looking for earliest flights on the next day from Fiftyville
select * from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville") and hour in (select min(hour) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville")) and minute in (select min(minute) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville") and hour in (select min(hour) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville")));
-- looking at format of passengers
select * from passengers;
-- list of passports for that flight
select passport_number from passengers where flight_id in (select id from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville") and hour in (select min(hour) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville")) and minute in (select min(minute) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville") and hour in (select min(hour) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville"))));


-- THIEF
    -- license
        -- select license_plate from bakery_security_logs WHERE activity = "exit" and year = 2021 and month = 7 and day = 28 and hour = 10 and minute >= 15 and minute <=25;
    -- atm
        -- select person_id from bank_accounts where account_number in (select account_number from atm_transactions where year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" and transaction_type = "withdraw");
    -- phone
        -- select caller from phone_calls where duration < 60 and year = 2021 AND month = 7 AND day = 28;
    -- passport
        -- select passport_number from passengers where flight_id in (select id from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville") and hour in (select min(hour) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville")) and minute in (select min(minute) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville") and hour in (select min(hour) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville"))));
-- looking at format of people
select * from people;
-- combined:
select name from people where
    license_plate in (select license_plate from bakery_security_logs WHERE activity = "exit" and year = 2021 and month = 7 and day = 28 and hour = 10 and minute >= 15 and minute <=25) and
    id in (select person_id from bank_accounts where account_number in (select account_number from atm_transactions where year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" and transaction_type = "withdraw")) and
    phone_number in (select caller from phone_calls where duration < 60 and year = 2021 AND month = 7 AND day = 28) and
    passport_number in (select passport_number from passengers where flight_id in (select id from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville") and hour in (select min(hour) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville")) and minute in (select min(minute) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville") and hour in (select min(hour) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville")))));


-- CITY:
    -- destination id:
        -- select destination_airport_id from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville") and hour in (select min(hour) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville")) and minute in (select min(minute) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville") and hour in (select min(hour) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville")));
-- destination city:
select city from airports where id in (select destination_airport_id from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville") and hour in (select min(hour) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville")) and minute in (select min(minute) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville") and hour in (select min(hour) from flights where year = 2021 and month = 7 and day = 29 and origin_airport_id in (select id from airports where city = "Fiftyville"))));


-- ACCOMPLICE
-- phone:
select name from people where phone_number in (select receiver from phone_calls where duration < 60 and year = 2021 AND month = 7 AND day = 28 and caller in (select phone_number from people where name = "Bruce"));


