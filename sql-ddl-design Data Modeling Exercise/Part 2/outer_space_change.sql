
-- from the terminal run:
-- psql < outer_space.sql

DROP DATABASE IF EXISTS outer_space;

CREATE DATABASE outer_space;

\c outer_space

CREATE TABLE planets
(
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  orbital_period_in_years FLOAT NOT NULL,
  orbits_around TEXT NOT NULL,
  galaxy TEXT NOT NULL,
  moons TEXT[]
);

INSERT INTO planets
  (name, orbital_period_in_years, orbits_around, galaxy, moons)
VALUES
  ('Earth', 1.00, 'The Sun', 'Milky Way', '{"The Moon"}'),
  ('Mars', 1.88, 'The Sun', 'Milky Way', '{"Phobos", "Deimos"}'),
  ('Venus', 0.62, 'The Sun', 'Milky Way', '{}'),
  ('Neptune', 164.8, 'The Sun', 'Milky Way', '{"Naiad", "Thalassa", "Despina", "Galatea", "Larissa", "S/2004 N 1", "Proteus", "Triton", "Nereid", "Halimede", "Sao", "Laomedeia", "Psamathe", "Neso"}'),
  ('Proxima Centauri b', 0.03, 'Proxima Centauri', 'Milky Way', '{}'),
  ('Gliese 876 b', 0.23, 'Gliese 876', 'Milky Way', '{}');

Before: 

  outer_space=# SELECT * FROM planets;
 id |        name        | orbital_period_in_years |  orbits_around   |  galaxy   |                                                      moons                                                       
----+--------------------+-------------------------+------------------+-----------+------------------------------------------------------------------------------------------------------------------
  1 | Earth              |                       1 | The Sun          | Milky Way | {"The Moon"}
  2 | Mars               |                    1.88 | The Sun          | Milky Way | {Phobos,Deimos}
  3 | Venus              |                    0.62 | The Sun          | Milky Way | {}
  4 | Neptune            |                   164.8 | The Sun          | Milky Way | {Naiad,Thalassa,Despina,Galatea,Larissa,"S/2004 N 1",Proteus,Triton,Nereid,Halimede,Sao,Laomedeia,Psamathe,Neso}
  5 | Proxima Centauri b |                    0.03 | Proxima Centauri | Milky Way | {}
  6 | Gliese 876 b       |                    0.23 | Gliese 876       | Milky Way | {}
(6 rows)

outer_space=# \dt
           List of relations
 Schema |  Name   | Type  |   Owner    
--------+---------+-------+------------
 public | planets | tabl

 After: 

--1) outer_space=# DELETE FROM planets WHERE id = 5; 
--   outer_space=# DELETE FROM planets WHERE id = 6;
--2) outer_space=# INSERT INTO planets (name, orbital_period_in_years, orbits_around, galaxy, moons) VALUES  
-- ('Mercury', 0.24, 'The Sun', 'Milky Way', '{}'), ('Saturn', 29.46, 'The Sun', 'Milky Way', '{total 82 (53 confirmed, 29 provisional)}'), ('Uranus', 84.01, 'The Sun', 'Milky Way', '{total 27 }'), ('Jupite', 11.86, 'The Sun', 'Milky Way', '{total 79 (53 confirmed, 26 provisional)}');
--3) outer_space=# INSERT INTO planets (name, orbital_period_in_years, orbits_around, galaxy, moons) VALUES ('Proxima Centauri b', 0.03, 'Proxima Centauri', 'Milky Way', '{}'), ('Gliese 876 b', 0.23, 'Gliese 876', 'Milky Way', '{}');

outer_space=#  SELECT * FROM planets;
 id |        name        | orbital_period_in_years |  orbits_around   |  galaxy   |                                                      moons                                                       
----+--------------------+-------------------------+------------------+-----------+------------------------------------------------------------------------------------------------------------------
  1 | Earth              |                       1 | The Sun          | Milky Way | {"The Moon"}
  2 | Mars               |                    1.88 | The Sun          | Milky Way | {Phobos,Deimos}
  3 | Venus              |                    0.62 | The Sun          | Milky Way | {}
  4 | Neptune            |                   164.8 | The Sun          | Milky Way | {Naiad,Thalassa,Despina,Galatea,Larissa,"S/2004 N 1",Proteus,Triton,Nereid,Halimede,Sao,Laomedeia,Psamathe,Neso}
  8 | Mercury            |                    0.24 | The Sun          | Milky Way | {}
  9 | Saturn             |                   29.46 | The Sun          | Milky Way | {"total 82 (53 confirmed","29 provisional): and more"}
 10 | Uranus             |                   84.01 | The Sun          | Milky Way | {"total 27: and more"}
 11 | Jupite             |                   11.86 | The Sun          | Milky Way | {"total 79 (53 confirmed","26 provisional)"}
 12 | Proxima Centauri b |                    0.03 | Proxima Centauri | Milky Way | {}
 13 | Gliese 876 b       |                    0.23 | Gliese 876       | Milky Way | {}
(10 rows)

