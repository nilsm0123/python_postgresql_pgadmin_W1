-- =============================================================
-- Übung 03 — SQL & PostgreSQL: Datenbank "sportverein"  (LÖSUNG)
-- =============================================================
-- Ausführen in pgAdmin: Rechtsklick auf die Datenbank "sportverein"
-- -> Query Tool -> Datei öffnen -> F5. Das Skript ist wiederholbar
-- (es löscht und erstellt die Tabellen am Anfang neu).


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
-- -------------------------------------------------------------
DROP TABLE IF EXISTS teilnahmen;
DROP TABLE IF EXISTS mitglieder;

CREATE TABLE mitglieder (
    mitglied_id SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    team        VARCHAR(50),
    eintritt    INT CHECK (eintritt >= 1900)
);

CREATE TABLE teilnahmen (
    teilnahme_id SERIAL PRIMARY KEY,
    mitglied_id  INT REFERENCES mitglieder(mitglied_id),
    datum        DATE NOT NULL
);


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
SELECT *
FROM mitglieder
WHERE team = 'U15';


-- -------------------------------------------------------------
-- Aufgabe 5: Welche verschiedenen Teams gibt es? Alphabetisch sortiert.
-- Erwartet: Damen 1, Herren 1, U15
-- -------------------------------------------------------------
SELECT DISTINCT team
FROM mitglieder
ORDER BY team;


-- -------------------------------------------------------------
-- Aufgabe 6: Welche Mitglieder haben einen Namen, der mit 'L' beginnt?
-- Erwartet: Luca, Lea
-- -------------------------------------------------------------
SELECT name, team
FROM mitglieder
WHERE name LIKE 'L%';


-- -------------------------------------------------------------
-- Aufgabe 7: Welche Mitglieder sind zwischen 2020 und 2022
-- (Grenzen eingeschlossen) eingetreten? Nach Eintrittsjahr sortiert.
-- Erwartet: Noah (2020), Lea (2021), Anna (2022)
-- -------------------------------------------------------------
SELECT name, eintritt
FROM mitglieder
WHERE eintritt BETWEEN 2020 AND 2022
ORDER BY eintritt;


-- -------------------------------------------------------------
-- Aufgabe 8: Wie viele Trainingsteilnahmen gibt es insgesamt?
-- Erwartet: 15
-- -------------------------------------------------------------
SELECT COUNT(*) AS anzahl_teilnahmen
FROM teilnahmen;


-- -------------------------------------------------------------
-- Aufgabe 9: Wie viele Trainings hat jedes Mitglied besucht —
-- auch Mitglieder ohne Teilnahme (mit 0)? Absteigend sortiert.
-- Erwartet: Anna 5, Lea 4, Luca 3, Mia 2, Jonas 1, Noah 0
-- -------------------------------------------------------------
SELECT m.name,
       m.team,
       COUNT(t.teilnahme_id) AS anzahl_trainings
FROM mitglieder m
LEFT JOIN teilnahmen t ON m.mitglied_id = t.mitglied_id
GROUP BY m.name, m.team
ORDER BY anzahl_trainings DESC;
-- COUNT(t.teilnahme_id) statt COUNT(*): sonst würde Noah 1 statt 0 erhalten,
-- weil der LEFT JOIN für ihn eine Zeile mit NULL-Werten erzeugt.


-- -------------------------------------------------------------
-- Aufgabe 10: Welche Mitglieder haben mehr als 2 Trainings besucht?
-- Erwartet: Anna 5, Lea 4, Luca 3
-- -------------------------------------------------------------
SELECT m.name,
       COUNT(t.teilnahme_id) AS anzahl_trainings
FROM mitglieder m
JOIN teilnahmen t ON m.mitglied_id = t.mitglied_id
GROUP BY m.name
HAVING COUNT(t.teilnahme_id) > 2
ORDER BY anzahl_trainings DESC;
-- HAVING statt WHERE, weil nach der Gruppierung gefiltert wird.


-- -------------------------------------------------------------
-- Aufgabe 11: Wie viele Teilnahmen hat jedes Team?
-- Erwartet: U15 9, Damen 1 6
-- -------------------------------------------------------------
SELECT m.team,
       COUNT(*) AS teilnahmen
FROM teilnahmen t
INNER JOIN mitglieder m ON m.mitglied_id = t.mitglied_id
GROUP BY m.team
ORDER BY teilnahmen DESC;


-- -------------------------------------------------------------
-- Aufgabe 12: Welche Mitglieder waren noch nie im Training?
-- Erwartet: Noah
-- -------------------------------------------------------------
SELECT m.name, m.team
FROM mitglieder m
LEFT JOIN teilnahmen t ON m.mitglied_id = t.mitglied_id
WHERE t.teilnahme_id IS NULL;
-- Achtung: "= NULL" funktioniert nicht, es braucht IS NULL.


-- -------------------------------------------------------------
-- Aufgabe 13: Wie viele Teilnahmen hatte jedes Mitglied im
-- September 2026? Absteigend sortiert, bei Gleichstand nach Name.
-- Erwartet: Anna 4, Lea 3, Luca 2, Mia 2, Jonas 1
-- -------------------------------------------------------------
SELECT m.name,
       COUNT(*) AS teilnahmen_september
FROM teilnahmen t
JOIN mitglieder m ON m.mitglied_id = t.mitglied_id
WHERE t.datum BETWEEN '2026-09-01' AND '2026-09-30'
GROUP BY m.name
ORDER BY teilnahmen_september DESC, m.name;
-- Alternative: WHERE EXTRACT(MONTH FROM t.datum) = 9
--                AND EXTRACT(YEAR FROM t.datum) = 2026


-- -------------------------------------------------------------
-- Aufgabe 14: Erstes und letztes Training pro Mitglied.
-- Erwartet z. B.: Anna 2026-09-01 / 2026-10-01
-- -------------------------------------------------------------
SELECT m.name,
       MIN(t.datum) AS erstes_training,
       MAX(t.datum) AS letztes_training
FROM teilnahmen t
JOIN mitglieder m ON m.mitglied_id = t.mitglied_id
GROUP BY m.name
ORDER BY m.name;


-- -------------------------------------------------------------
-- Aufgabe 15: Wie viele Trainings besucht ein Mitglied im
-- Durchschnitt (inkl. Noah mit 0)? Auf 2 Stellen gerundet.
-- Erwartet: 2.50
-- -------------------------------------------------------------
SELECT ROUND(AVG(anzahl), 2) AS durchschnitt
FROM (
    SELECT m.mitglied_id,
           COUNT(t.teilnahme_id) AS anzahl
    FROM mitglieder m
    LEFT JOIN teilnahmen t ON m.mitglied_id = t.mitglied_id
    GROUP BY m.mitglied_id
) AS pro_mitglied;


-- -------------------------------------------------------------
-- Aufgabe 16: Welche Mitglieder liegen über diesem Durchschnitt?
-- Erwartet: Anna 5, Lea 4, Luca 3
-- -------------------------------------------------------------
SELECT m.name,
       COUNT(t.teilnahme_id) AS anzahl
FROM mitglieder m
LEFT JOIN teilnahmen t ON m.mitglied_id = t.mitglied_id
GROUP BY m.name
HAVING COUNT(t.teilnahme_id) > (
    SELECT AVG(anzahl)
    FROM (
        SELECT COUNT(t2.teilnahme_id) AS anzahl
        FROM mitglieder m2
        LEFT JOIN teilnahmen t2 ON m2.mitglied_id = t2.mitglied_id
        GROUP BY m2.mitglied_id
    ) AS pro_mitglied
)
ORDER BY anzahl DESC;


-- -------------------------------------------------------------
-- Aufgabe 17: Spalte "email" ergänzen, für Mia die Adresse
-- 'mia@example.ch' eintragen und zählen, wie viele Mitglieder
-- noch keine E-Mail haben.
-- Erwartet: 5
-- -------------------------------------------------------------
ALTER TABLE mitglieder ADD COLUMN email VARCHAR(100) UNIQUE;

-- Zuerst prüfen, welche Zeile betroffen ist ...
SELECT * FROM mitglieder WHERE name = 'Mia';
-- ... dann ändern (nie ohne WHERE!)
UPDATE mitglieder SET email = 'mia@example.ch' WHERE name = 'Mia';

SELECT COUNT(*) AS ohne_email
FROM mitglieder
WHERE email IS NULL;


-- -------------------------------------------------------------
-- Aufgabe 18: Transaktion — Anna wechselt ins Team 'U17' UND ihre
-- erste Teilnahme im neuen Team am 2026-10-08 wird erfasst.
-- Beides soll nur zusammen gespeichert werden.
-- -------------------------------------------------------------
BEGIN;
UPDATE mitglieder SET team = 'U17' WHERE mitglied_id = 1;
INSERT INTO teilnahmen (mitglied_id, datum) VALUES (1, '2026-10-08');
COMMIT;

-- Kontrolle — erwartet: U17, 6 Teilnahmen
SELECT m.name, m.team, COUNT(t.teilnahme_id) AS anzahl
FROM mitglieder m
JOIN teilnahmen t ON m.mitglied_id = t.mitglied_id
WHERE m.mitglied_id = 1
GROUP BY m.name, m.team;


-- -------------------------------------------------------------
-- Aufgabe 19: Index anlegen, damit Abfragen nach Datum schneller werden.
-- -------------------------------------------------------------
CREATE INDEX idx_teilnahmen_datum ON teilnahmen(datum);


-- -------------------------------------------------------------
-- Aufgabe 20: Jonas tritt aus dem Verein aus und soll gelöscht werden.
-- a) Warum schlägt "DELETE FROM mitglieder WHERE name = 'Jonas';" fehl?
-- b) Lösche Jonas korrekt.
-- -------------------------------------------------------------
-- a) Jonas hat noch eine Teilnahme. Der Fremdschlüssel
--    teilnahmen.mitglied_id -> mitglieder.mitglied_id verbietet,
--    ein Mitglied zu löschen, auf das noch Teilnahmen verweisen
--    (Fehler: "violates foreign key constraint").
-- b) Zuerst die abhängigen Teilnahmen, dann das Mitglied löschen —
--    in einer Transaktion, damit nichts halb gelöscht wird:
BEGIN;
DELETE FROM teilnahmen
WHERE mitglied_id = (SELECT mitglied_id FROM mitglieder WHERE name = 'Jonas');
DELETE FROM mitglieder WHERE name = 'Jonas';
COMMIT;

-- Kontrolle — erwartet: 5 Mitglieder, 15 Teilnahmen
SELECT (SELECT COUNT(*) FROM mitglieder) AS mitglieder,
       (SELECT COUNT(*) FROM teilnahmen) AS teilnahmen;
