CREATE DATABASE course_tracker;

CREATE TABLE person (
    discord_id BIGINT NOT NULL PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    first_joined TIMESTAMP NOT NULL
);

CREATE TABLE course (
    crn BIGINT NOT NULL PRIMARY KEY,
    subject VARCHAR(100) NOT NULL,
    status VARCHAR(6) NOT NULL CHECK (status IN ('OPEN','CLOSED','NONE')), 
    last_changed TIMESTAMP NOT NULL
);

CREATE TABLE tracking (
    FK_discord_id BIGINT REFERENCES person (discord_id),
    FK_crn BIGINT REFERENCES course (crn),
    started_tracking TIMESTAMP NOT NULL
);