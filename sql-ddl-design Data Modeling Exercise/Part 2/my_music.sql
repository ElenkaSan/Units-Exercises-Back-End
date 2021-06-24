CREATE TABLE "producers" (
  "id" SERIAL PRIMARY KEY,
  "full_name" TEXT NOT NULL
);

CREATE TABLE "songs" (
  "id" SERIAL PRIMARY KEY,
  "title" TEXT NOT NULL,
  "duration_in_seconds" INTEGER NOT NULL,
  "release_date" DATE NOT NULL,
  "album" TEXT NOT NULL,
  "producers" INTEGER NOT NULL
);

CREATE TABLE "artists" (
  "id" SERIAL PRIMARY KEY,
  "nickname" TEXT,
  "first_name" TEXT NOT NULL,
  "last_name" TEXT,
  "birth_date" DATE NOT NULL
);

CREATE TABLE "musics" (
  "id" SERIAL PRIMARY KEY,
  "artist_id" INTEGER,
  "song_id" INTEGER
);

ALTER TABLE "songs" ADD FOREIGN KEY ("producers") REFERENCES "producers" ("id");

ALTER TABLE "musics" ADD FOREIGN KEY ("artist_id") REFERENCES "artists" ("id");

ALTER TABLE "musics" ADD FOREIGN KEY ("song_id") REFERENCES "songs" ("id");
