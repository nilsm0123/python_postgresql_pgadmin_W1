# Übungen Data Science

Übungssammlung zum Modul Data Science. Sie basiert auf dem *Factsheet Data Science*, der *Python & SQL Referenz* und
den Beispielprüfungen **AP01** (Management & Nutzung relationaler Daten) und **AP02** (Datenbeschaffung,
Datenaufbereitung & EDA). Alle Datensätze sind frei erfunden.

## Lernpfad

Arbeite die Übungen der Reihe nach durch. Jede Übung gibt es als **Aufgabe** und als **Lösung**
(`…_loesung` bzw. `…_musterloesung`). Erst selbst lösen, dann vergleichen.

### Teil 1 — Grundlagen

| Nr. | Übung | Inhalt | Factsheet |
|---|---|---|---|
| 01 | `01_python_grundlagen.ipynb` | Variablen, Datentypen, Listen, Dictionaries, Schleifen, Funktionen, typische Fehler | Kap. 1 |
| 02 | `02_pandas_teilnahmen.ipynb` | CSV einlesen, `groupby`, filtern, Datum, `merge`, Diagramm, Export | Kap. 1, 6 |
| 03 | `03_sql_sportverein.sql` | Tabellen anlegen, `SELECT`, `JOIN`, `GROUP BY`/`HAVING`, Unterabfragen, Transaktionen (in pgAdmin) | Kap. 2, 3, 10 |
| 04 | `04_datenformate.ipynb` | CSV, JSON, XML lesen und schreiben, Trennzeichen, Encoding | Kap. 11 |
| 05 | `05_etl_postgresql.ipynb` | ETL-Pipeline: CSV bereinigen → PostgreSQL → SQL-Auswertung → Bericht | Kap. 3, 12 |
| 06 | `06_git_github_codespaces.md` | Git, Branches, Merge-Konflikt, Pull Request, Actions, Codespaces, MongoDB | Kap. 4, 5, 7–9 |

### Teil 2 — Prüfungsvorbereitung AP01 (SQL)

| Nr. | Übung | Inhalt |
|---|---|---|
| 10 | `10_sql_pruefungsvorbereitung_ap01.ipynb` | 8 Stufen bis zum Prüfungsniveau: Datenmodell → Abfragen → Aggregation → JOINs → `LEFT JOIN`-Fallen → Datenqualität → **Fehleranalyse** → **Konzeptfragen** |
| 11 | `11_probepruefung_ap01.ipynb` | **Probeprüfung** im Format von AP01 (Teile A/B/C, 40 Punkte, gleiches Bewertungsschema) |

Datenbank: `Data/fitness.db` (Fitnesskette «MoveFit», Beschreibung in `Data/fitness_beschreibung.md`).

### Teil 3 — Prüfungsvorbereitung AP02 (Python & EDA)

| Nr. | Übung | Inhalt |
|---|---|---|
| 20 | `20_python_eda_pruefungsvorbereitung_ap02.ipynb` | 9 Stufen: BeautifulSoup → Scraping & Duplikate → Regex → fehlende Werte (MCAR/MAR/MNAR) → Verteilung & Ausreisser → `cut`/`qcut`/`crosstab` → `merge` & Korrelation → Tabellen einer Detailseite → Konzeptfragen |
| 21 | `21_probepruefung_ap02.ipynb` | **Probeprüfung** im Format von AP02 (Teile A/B/C, 40 Punkte, gleiches Bewertungsschema) |

Daten: `Data/velomarkt/` (fiktiver Velo-Shop «VeloMarkt», Beschreibung in `Data/velomarkt/README.md`).

## Tipps für die Probeprüfungen

- Setze dir ein Zeitlimit von **60 Minuten** und arbeite «open book» (Factsheet, Referenz, eigene Übungen), aber
  **ohne KI**, so wie in der Prüfung.
- Bewerte dich danach mit dem Bewertungsschema im Notebook und der Musterlösung.
- Bei Fehleranalyse-Aufgaben gibt es Punkte für **jede begründete Änderung**: Was tut der Code, warum ist das Ergebnis
  falsch, was änderst du?
- Bei Konzeptfragen zählen nur Antworten **mit Bezug zu den Daten**: Nenne Tabellen, Spalten und Zahlen.

## Voraussetzungen

- Docker-Container laufen (PostgreSQL + pgAdmin, siehe `README.md` im Hauptordner). Die AP01-Notebooks greifen
  automatisch auf das SQLite-Backup `Data/fitness.db` zurück, falls PostgreSQL nicht erreichbar ist.
- Bibliotheken: `pip install -r requirements.txt` (läuft im Codespace automatisch).
- Notebooks im Ordner `Uebungen/` öffnen. Die Datenpfade sind relativ dazu.

## Automatische Prüfung

Bei jedem Push führt GitHub Actions (`.github/workflows/uebungen.yml`) alle Lösungen gegen eine echte
PostgreSQL-Datenbank aus. Die Selbstkontrollen (`assert`) stellen sicher, dass die Musterlösungen stimmen.

## Daten neu erzeugen

```bash
python Uebungen/tools/generate_fitness_db.py   # Data/fitness.db
python Uebungen/tools/generate_velomarkt.py    # Data/velomarkt/
```
