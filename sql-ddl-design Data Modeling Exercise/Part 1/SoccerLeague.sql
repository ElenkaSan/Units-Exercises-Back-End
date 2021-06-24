CREATE TABLE "Teams" (
  "id" SERIAL PRIMARY KEY,
  "Team_name" varchar NOT NULL,
  "City_name" varchar NOT NULL
);

CREATE TABLE "Goals" (
  "id" int PRIMARY KEY,
  "Player_id" int NOT NULL,
  "Match_id" int,
  "Team_id" int NOT NULL,
  "Score" varchar
);

CREATE TABLE "Players" (
  "id" int PRIMARY KEY,
  "Full_name" varchar NOT NULL,
  "Birthday" varchar,
  "Insurance" varchar,
  "Team_id" int NOT NULL
);

CREATE TABLE "Referees" (
  "id" int PRIMARY KEY,
  "Full_name" varchar NOT NULL
);

CREATE TABLE "Matches" (
  "id" int PRIMARY KEY,
  "Referee_id" int NOT NULL,
  "Team_id" int NOT NULL,
  "Season_id" int NOT NULL,
  "Location" varchar,
  "Date_of_match" datetime,
  "Time" varchar
);

CREATE TABLE "Season" (
  "id" int PRIMARY KEY,
  "Start_date" datetime,
  "End_date" datetime
);

CREATE TABLE "Lineups" (
  "id" int PRIMARY KEY,
  "Player_id" int NOT NULL,
  "Match_id" int,
  "Team_id" int NOT NULL
);

ALTER TABLE "Goals" ADD FOREIGN KEY ("Player_id") REFERENCES "Players" ("id");

ALTER TABLE "Goals" ADD FOREIGN KEY ("Match_id") REFERENCES "Matches" ("id");

ALTER TABLE "Goals" ADD FOREIGN KEY ("Team_id") REFERENCES "Teams" ("id");

ALTER TABLE "Players" ADD FOREIGN KEY ("Team_id") REFERENCES "Teams" ("id");

ALTER TABLE "Matches" ADD FOREIGN KEY ("Referee_id") REFERENCES "Referees" ("id");

ALTER TABLE "Matches" ADD FOREIGN KEY ("Team_id") REFERENCES "Teams" ("id");

ALTER TABLE "Matches" ADD FOREIGN KEY ("Season_id") REFERENCES "Season" ("id");

ALTER TABLE "Lineups" ADD FOREIGN KEY ("Player_id") REFERENCES "Players" ("id");

ALTER TABLE "Lineups" ADD FOREIGN KEY ("Match_id") REFERENCES "Matches" ("id");

ALTER TABLE "Lineups" ADD FOREIGN KEY ("Team_id") REFERENCES "Teams" ("id");

COMMENT ON COLUMN "Goals"."Score" IS 'When team win, lost or draw';
