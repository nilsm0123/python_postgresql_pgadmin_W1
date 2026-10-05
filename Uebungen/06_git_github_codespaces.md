# Übung 06 — Git, GitHub, Codespaces & NoSQL

Bezug: *Factsheet Data Science*, Kapitel 4 (MongoDB), 5 (VS Code), 7 (Git), 8 (GitHub) und 9 (Codespaces).

Du arbeitest direkt in **diesem Repository**, am besten im Codespace. Die Lösungen sind jeweils eingeklappt —
erst selbst probieren, dann aufklappen.

---

## Teil A — Git im Terminal

**A1. Wo stehe ich?** Öffne in VS Code ein Terminal (*Terminal → New Terminal*) und finde heraus:
a) auf welchem Branch du bist, b) ob es geänderte Dateien gibt, c) wie die letzten 5 Commits heissen.

<details><summary>Lösung</summary>

```bash
git status              # a) "On branch ..." und b) geänderte/neue Dateien
git log --oneline -5    # c) die letzten 5 Commits, je eine Zeile
```
</details>

**A2. Eigener Branch.** Erstelle den Branch `uebung-git` und wechsle hinein. Lege die Datei `Uebungen/meine_notizen.md`
mit einer Überschrift an und committe sie mit einer aussagekräftigen Commit Message.

<details><summary>Lösung</summary>

```bash
git switch -c uebung-git
echo "# Meine Notizen" > Uebungen/meine_notizen.md
git add Uebungen/meine_notizen.md
git commit -m "Notizen-Datei für die Übungen angelegt"
```
`git add` legt die Datei in die **Staging Area**, `git commit` speichert den Schnappschuss.
</details>

**A3. Was hat sich geändert?** Ergänze eine Zeile in `meine_notizen.md`. Zeige die Änderung **vor** dem Commit an
und danach, was zwischen `main`/`master` und deinem Branch anders ist.

<details><summary>Lösung</summary>

```bash
git diff                    # Änderungen im Working Directory (noch nicht gestaged)
git add Uebungen/meine_notizen.md
git diff --staged           # Änderungen in der Staging Area
git commit -m "Notiz ergänzt"
git diff master..uebung-git --stat   # Unterschiede zwischen den Branches
```
</details>

**A4. .gitignore verstehen.** Führe das Notebook `02_pandas_teilnahmen_loesung.ipynb` aus. Es erzeugt Dateien im Ordner
`Uebungen/output/`. Warum zeigt `git status` diese Dateien nicht an? Wann ist eine `.gitignore` besonders wichtig?

<details><summary>Lösung</summary>

In der `.gitignore` steht die Zeile `Uebungen/output/`, darum ignoriert Git den ganzen Ordner. Wichtig ist das bei
**generierten Dateien** (die man jederzeit neu erzeugen kann), bei grossen Dateien, bei virtuellen Umgebungen (`.venv/`)
und vor allem bei **Personendaten und Passwörtern**: Die gehören nie in ein Repository, schon gar nicht in ein
öffentliches.
</details>

**A5. Merge-Konflikt provozieren und lösen.**
1. Bring die Notizen-Datei zuerst auf `master`: `git switch master` und `git merge uebung-git`.
2. Ändere auf `master` die Überschrift in `# Notizen (master)` und committe.
3. Wechsle auf `uebung-git`, ändere die Überschrift in `# Notizen (branch)` und committe.
4. Merge `master` in `uebung-git`. Was passiert, und wie löst du es?

<details><summary>Lösung</summary>

Beide Branches haben **dieselbe Zeile** unterschiedlich geändert, Git meldet einen **Merge-Konflikt** und markiert die
Stelle in der Datei:
```
<<<<<<< HEAD
# Notizen (branch)
=======
# Notizen (master)
>>>>>>> master
```
Lösung: Die Datei so bearbeiten, dass nur die gewünschte Version übrig bleibt (Markierungen entfernen), dann
`git add Uebungen/meine_notizen.md` und `git commit`. In VS Code helfen die Buttons «Accept Current / Incoming / Both».

*Übrigens:* Genau solche vergessenen Markierungen standen in `requirements.txt` dieses Repos, und `pip install`
schlug deshalb fehl.
</details>

---

## Teil B — GitHub

**B1. Push und Pull Request.** Lade deinen Branch auf GitHub hoch und erstelle einen Pull Request nach `master`.

<details><summary>Lösung</summary>

```bash
git push -u origin uebung-git     # -u merkt sich die Verbindung für künftige Pushes
```
Auf github.com erscheint der Button **Compare & pull request** → Beschreibung schreiben → **Create pull request**.
Ein Pull Request ist der Antrag «Bitte übernehmt meine Änderungen». Andere können ihn prüfen (Review), kommentieren und
mergen.
</details>

**B2. GitHub Actions lesen.** Öffne `.github/workflows/uebungen.yml` und beantworte:
a) Wann läuft der Workflow? b) Auf welchem Betriebssystem? c) Woher kommt die PostgreSQL-Datenbank?
d) Was bedeutet ein rotes ✗ neben einem Commit?

<details><summary>Lösung</summary>

a) Bei jedem Push und Pull Request, der etwas in `Uebungen/`, `requirements.txt` oder am Workflow ändert, sowie
manuell (`workflow_dispatch`). b) `ubuntu-latest`, ein Linux-Server von GitHub. c) Aus einem **Service-Container**
(`postgres:16`) mit denselben Zugangsdaten wie in `docker-compose.yml`. d) Ein Schritt ist fehlgeschlagen, z. B. eine
Lösung liefert nicht mehr das erwartete Ergebnis. Im Tab **Actions** steht im Log, welcher.
</details>

**B3. Issue anlegen.** Erstelle auf GitHub ein Issue «Übung 10, Stufe 7 nochmals wiederholen» und weise es dir selbst zu.
Wofür sind Issues im Unterschied zu Pull Requests da?

<details><summary>Lösung</summary>

Ein **Issue** beschreibt eine Aufgabe, einen Fehler oder eine Idee (wie ein Ticket), noch ohne Code. Ein **Pull
Request** enthält konkrete Code-Änderungen, die übernommen werden sollen. Ein PR kann ein Issue schliessen
(z. B. «Closes #3» in der Beschreibung).
</details>

---

## Teil C — Codespaces & Dev Container

**C1.** Öffne `.devcontainer/devcontainer.json`. Was bewirken `postCreateCommand` und `postStartCommand`?

<details><summary>Lösung</summary>

`postCreateCommand` läuft **einmal** nach dem Erstellen des Codespaces und installiert alle Bibliotheken aus
`requirements.txt`. `postStartCommand` läuft **bei jedem Start** und startet mit `.devcontainer/start.sh` die
Docker-Container (PostgreSQL und pgAdmin).
</details>

**C2.** Du hast im Codespace eine Stunde an Übung 10 gearbeitet und löschst den Codespace. Was ist verloren, was nicht?

<details><summary>Lösung</summary>

Verloren ist alles, was **nicht committet und gepusht** wurde. Erhalten bleibt, was auf GitHub liegt. Darum vor dem
Beenden immer `git add`, `git commit`, `git push`. Nicht benutzte Codespaces sollte man stoppen, weil sie das
Gratiskontingent verbrauchen.
</details>

**C3.** pgAdmin läuft im Codespace auf Port 5050. Wie öffnest du es im Browser, und warum heisst der Host der Datenbank
in pgAdmin `db`, im Python-Notebook aber `localhost`?

<details><summary>Lösung</summary>

VS Code → Tab **Ports** → Port 5050 → Weltkugel-Symbol (Port-Weiterleitung). pgAdmin läuft selbst in einem Container
im Docker-Netz von `docker-compose.yml`. Dort ist die Datenbank unter dem **Service-Namen** `db` erreichbar. Das Notebook
läuft dagegen direkt im Codespace und erreicht die Datenbank über den nach aussen freigegebenen Port 5432 auf
`localhost`.
</details>

---

## Teil D — NoSQL & MongoDB (Konzept)

**D1.** Übersetze in die MongoDB-Schreibweise (`mongosh`) für eine Collection `mitglieder`:
a) `SELECT * FROM mitglieder WHERE team = 'U15';`
b) `SELECT team, COUNT(*) FROM mitglieder GROUP BY team;`
c) alle Mitglieder, die überhaupt ein Feld `kontakt` haben

<details><summary>Lösung</summary>

```javascript
db.mitglieder.find({ team: "U15" })                                        // a)
db.mitglieder.aggregate([{ $group: { _id: "$team", anzahl: { $sum: 1 } } }])  // b)
db.mitglieder.find({ kontakt: { $exists: true } })                         // c)
```
</details>

**D2.** Für welche Daten aus dieser Übungssammlung wäre MongoDB besser geeignet als PostgreSQL, für welche nicht?
Begründe mit je einem Beispiel.

<details><summary>Lösung</summary>

**PostgreSQL:** `fitness.db`. Feste Struktur, viele Beziehungen (Mitglied ↔ Buchung ↔ Termin ↔ Studio), Fremdschlüssel
sichern die Integrität, Auswertungen mit JOINs.
**MongoDB:** die API-Antwort `reviews.json` oder die technischen Daten von Velos. Je nach Velo gibt es ganz
unterschiedliche Merkmale (Akku, Motor, Federweg, Anhängerkupplung …), die man als flexibles Dokument speichern kann,
ohne für jedes Merkmal eine Spalte anzulegen (flexibles Schema, Verschachtelung).
</details>

**D3 (praktisch, optional).** Starte im Codespace eine MongoDB und probiere D1 aus:

```bash
docker run -d --name mongo -p 27017:27017 mongo:7
docker exec -it mongo mongosh
```
```javascript
use sportverein
db.mitglieder.insertMany([
  { name: "Anna", team: "U15", lizenzen: ["Swiss Badminton", "J+S"] },
  { name: "Luca", team: "U15" },
  { name: "Mia", team: "Damen 1", kontakt: { email: "mia@example.ch" } }
])
```
