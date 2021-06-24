CREATE TABLE "Regions" (
  "id" SERIAL PRIMARY KEY,
  "City_name" varchar UNIQUE NOT NULL
);

CREATE TABLE "Users" (
  "id" int PRIMARY KEY,
  "Full_name" varchar NOT NULL,
  "Username" varchar(15) UNIQUE NOT NULL,
  "User_password" varchar(20) NOT NULL,
  "Region_id" int NOT NULL
);

CREATE TABLE "Posts" (
  "id" int PRIMARY KEY,
  "Title" varchar NOT NULL,
  "Text" varchar,
  "User_id" int NOT NULL,
  "Location" varchar,
  "Region_id" int NOT NULL,
  "Categories_id" int NOT NULL
);

CREATE TABLE "Categories" (
  "id" int PRIMARY KEY,
  "Name" varchar NOT NULL,
  "Types" varchar
);

ALTER TABLE "Users" ADD FOREIGN KEY ("Region_id") REFERENCES "Regions" ("id");

ALTER TABLE "Posts" ADD FOREIGN KEY ("User_id") REFERENCES "Users" ("id");

ALTER TABLE "Posts" ADD FOREIGN KEY ("Region_id") REFERENCES "Regions" ("id");

ALTER TABLE "Posts" ADD FOREIGN KEY ("Categories_id") REFERENCES "Categories" ("id");

ALTER TABLE "Posts" ADD FOREIGN KEY ("id") REFERENCES "Categories" ("id");
