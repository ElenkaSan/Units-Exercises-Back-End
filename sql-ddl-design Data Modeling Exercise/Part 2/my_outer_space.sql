-- from the terminal run:
-- psql < my_outer_space.sql
-- psql my_outer_space     

DROP DATABASE IF EXISTS my_outer_space;

CREATE DATABASE my_outer_space;

\c my_outer_space

CREATE TABLE "type_of_system" (
  "id" int PRIMARY KEY,
  "name" TEXT NOT NULL
);

CREATE TABLE "orbits" (
  "id" int PRIMARY KEY,
  "name" TEXT NOT NULL
);

CREATE TABLE "planets" (
  "id" int PRIMARY KEY,
  "name" TEXT NOT NULL,
  "orbital_period_in_years" FLOAT NOT NULL,
  "type_of_system_id" int NOT NULL,
  "orbits_around_id" int NOT NULL,
  "galaxy" TEXT NOT NULL,
  "satellite" TEXT NOT NULL
);

ALTER TABLE "planets" ADD FOREIGN KEY ("type_of_system_id") REFERENCES "type_of_system" ("id");

ALTER TABLE "planets" ADD FOREIGN KEY ("orbits_around_id") REFERENCES "orbits" ("id");


INSERT INTO planets (name, orbital_period_in_years, type_of_system_id, orbits_around_id, galaxy, satellite)
VALUES
 ('Earth', 1.00, 1, 1, 'Milky Way', '{"The Moon"}'),
 ('Mars', 1.88, 1, 1, 'Milky Way', '{"Phobos", "Deimos"}'),
 ('Venus', 0.62, 1, 1, 'Milky Way', '{}'),
 ('Neptune', 164.8, 1, 1 'Milky Way', '{"Naiad", "Thalassa", "Despina", "Galatea", "Larissa", "S/2004 N 1", "Proteus", "Triton", "Nereid", "Halimede", "Sao", "Laomedeia", "Psamathe", "Neso"}'),
 ('Jupite', 11.86, 1, 1, 'Milky Way', '{total 79 (53 confirmed, 26 provisional): "Europa", "Ganymede", "Io", "Callisto", "Amalthea", "Himalia" and more}' ),
 ('Mercury', 0.24, 1, 1, 'Milky Way', '{}'),
 ('Saturn', 29.46, 1, 1, 'Milky Way', '{total 82 (53 confirmed, 29 provisional): and more}'),
 ('Uranus', 84.01, 1, 1, 'Milky Way', '{total 27: and more}'),
 ('Proxima Centauri b', 0.03, 2, 2, 'Milky Way', '{}'),
 ('Gliese 876 b', 0.23, 2, 3, 'Milky Way', '{}');

INSERT INTO type_of_system (name) VALUES
 ('Solar System'),
 ('Planetary System');

INSERT INTO orbits (name) VALUES 
 ('The Sun'),
 ('Proxima Centauri'),
 ('Gliese 876');