-- =============================================================
-- Übung 03 — SQL & PostgreSQL: Datenbank "sportverein"  (AUFGABEN)
-- =============================================================
-- Bearbeite die Aufgaben der Reihe nach im Query Tool von pgAdmin.
-- Schreibe deine Abfrage jeweils unter "Deine Lösung:", markiere sie und
-- führe sie mit F5 aus. Unter "Erwartet" steht das richtige Ergebnis.
-- Lösungen: 03_sql_sportverein_loesung.sql


-- -------------------------------------------------------------
-- Aufgabe 1: Datenbank anlegen
-- -------------------------------------------------------------
-- In pgAdmin mit der Datenbank "postgres" verbunden ausführen:
--
--   CREATE DATABASE sportverein;
--
-- Danach im Object Explorer "Refresh" und das Query Tool auf der
-- neuen Datenbank "sportverein" öffnen. (In psql: \c sportverein)


-- -------------------------------------------------------------
-- Aufgabe 2: Tabellen anlegen (DDL)
-- mitglieder: mitglied_id (fortlaufend, Primärschlüssel), name (Text, Pflicht),
--             team (Text), eintritt (Ganzzahl, mind. 1900)
-- teilnahmen: teilnahme_id (fortlaufend, Primärschlüssel),
--             mitglied_id (Fremdschlüssel auf mitglieder), datum (Datum, Pflicht)
-- Tipp: Beginne mit DROP TABLE IF EXISTS, damit du das Skript wiederholen kannst.
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 3: Daten einfügen (DML) — vorgegeben
-- -------------------------------------------------------------
INSERT INTO mitglieder (name, team, eintritt) VALUES
    ('Anna',  'U15',      2022),
    ('Luca',  'U15',      2023),
    ('Mia',   'Damen 1',  2019),
    ('Noah',  'Herren 1', 2020),
    ('Lea',   'Damen 1',  2021),
    ('Jonas', 'U15',      2024);

INSERT INTO teilnahmen (mitglied_id, datum) VALUES
    (1, '2026-09-01'), (2, '2026-09-01'), (1, '2026-09-03'),
    (3, '2026-09-02'), (1, '2026-09-08'), (2, '2026-09-08'),
    (5, '2026-09-02'), (5, '2026-09-09'), (3, '2026-09-09'),
    (6, '2026-09-10'), (1, '2026-09-15'), (5, '2026-09-16'),
    (1, '2026-10-01'), (2, '2026-10-01'), (5, '2026-10-07');


-- -------------------------------------------------------------
-- Aufgabe 4: Welche Mitglieder spielen im Team 'U15'?
-- Erwartet: Anna, Luca, Jonas
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 5: Welche verschiedenen Teams gibt es? Alphabetisch sortiert.
-- Erwartet: Damen 1, Herren 1, U15
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 6: Welche Mitglieder haben einen Namen, der mit 'L' beginnt?
-- Erwartet: Luca, Lea
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 7: Welche Mitglieder sind zwischen 2020 und 2022
-- (Grenzen eingeschlossen) eingetreten? Nach Eintrittsjahr sortiert.
-- Erwartet: Noah (2020), Lea (2021), Anna (2022)
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 8: Wie viele Trainingsteilnahmen gibt es insgesamt?
-- Erwartet: 15
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 9: Wie viele Trainings hat jedes Mitglied besucht —
-- auch Mitglieder ohne Teilnahme (mit 0)? Absteigend sortiert.
-- Erwartet: Anna 5, Lea 4, Luca 3, Mia 2, Jonas 1, Noah 0
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 10: Welche Mitglieder haben mehr als 2 Trainings besucht?
-- Erwartet: Anna 5, Lea 4, Luca 3
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 11: Wie viele Teilnahmen hat jedes Team?
-- Erwartet: U15 9, Damen 1 6
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 12: Welche Mitglieder waren noch nie im Training?
-- Erwartet: Noah
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 13: Wie viele Teilnahmen hatte jedes Mitglied im
-- September 2026? Absteigend sortiert, bei Gleichstand nach Name.
-- Erwartet: Anna 4, Lea 3, Luca 2, Mia 2, Jonas 1
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 14: Erstes und letztes Training pro Mitglied.
-- Erwartet z. B.: Anna 2026-09-01 / 2026-10-01
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 15: Wie viele Trainings besucht ein Mitglied im
-- Durchschnitt (inkl. Noah mit 0)? Auf 2 Stellen gerundet.
-- Erwartet: 2.50
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 16: Welche Mitglieder liegen über diesem Durchschnitt?
-- Erwartet: Anna 5, Lea 4, Luca 3
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 17: Spalte "email" ergänzen, für Mia die Adresse
-- 'mia@example.ch' eintragen und zählen, wie viele Mitglieder
-- noch keine E-Mail haben.
-- Erwartet: 5
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 18: Transaktion — Anna wechselt ins Team 'U17' UND ihre
-- erste Teilnahme im neuen Team am 2026-10-08 wird erfasst.
-- Beides soll nur zusammen gespeichert werden.
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 19: Index anlegen, damit Abfragen nach Datum schneller werden.
-- -------------------------------------------------------------
-- Deine Lösung:



-- -------------------------------------------------------------
-- Aufgabe 20: Jonas tritt aus dem Verein aus und soll gelöscht werden.
-- a) Warum schlägt "DELETE FROM mitglieder WHERE name = 'Jonas';" fehl?
-- b) Lösche Jonas korrekt.
-- -------------------------------------------------------------
-- Deine Lösung:
