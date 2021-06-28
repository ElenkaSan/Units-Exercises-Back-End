CREATE TABLE "Doctors" (
  "id" SERIAL PRIMARY KEY,
  "Full_name" varchar NOT NULL,
  "Speciality" varchar NOT NULL
);

CREATE TABLE "Visits" (
  "id" int PRIMARY KEY,
  "Doctor_id" int NOT NULL,
  "Patient_id" int NOT NULL,
  "Diagnose_id" int,
  "Date_of_visit" datetime
);

CREATE TABLE "Patients" (
  "id" int PRIMARY KEY,
  "Full_name" varchar NOT NULL,
  "Birthday" varchar,
  "Insurance" varchar
);

CREATE TABLE "Diagnoses" (
  "id" int PRIMARY KEY,
  "Visit_id" int NOT NULL,
  "Disease_id" int NOT NULL,
  "Types" varchar
);

CREATE TABLE "Diseases" (
  "id" int PRIMARY KEY,
  "Full_name" varchar NOT NULL,
  "Description" varchar,
  "Treatment" varchar
);

ALTER TABLE "Visits" ADD FOREIGN KEY ("Doctor_id") REFERENCES "Doctors" ("id");

ALTER TABLE "Visits" ADD FOREIGN KEY ("Patient_id") REFERENCES "Patients" ("id");

ALTER TABLE "Visits" ADD FOREIGN KEY ("Diagnose_id") REFERENCES "Diagnoses" ("id");

ALTER TABLE "Diagnoses" ADD FOREIGN KEY ("Visit_id") REFERENCES "Visits" ("id");

ALTER TABLE "Diagnoses" ADD FOREIGN KEY ("Diseases_id") REFERENCES "Diseases" ("id");

COMMENT ON COLUMN "Diagnoses"."Types" IS 'When type of diagnoses created';
