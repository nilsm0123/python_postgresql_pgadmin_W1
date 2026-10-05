"""Erzeugt die fiktive Datenbank der Fitnesskette «MoveFit» für die AP01-Vorbereitung.

Ausgabe: Uebungen/Data/fitness.db (SQLite). Die Daten sind frei erfunden und
reproduzierbar (fester Zufalls-Seed). Bewusst eingebaute Datenprobleme:
  - Studio ST06 ohne Kurstermine, Kurs CO15 ohne Kurstermine
  - Trainer TR030 ohne Studio (studioid NULL)
  - Mitglieder ME0501–ME0505 mit ungültigem membership_type und ohne Buchungen
  - weitere Mitglieder ohne Buchungen, fehlende/ungültige E-Mails,
    unplausible Geburtsjahre
  - einzelne Buchungen mit paid_price > base_price bzw. Buchung nach dem Termin
  - zwei überbuchte Kurstermine

Aufruf (im Hauptordner des Repos):  python Uebungen/tools/generate_fitness_db.py
"""
import os
import random
import sqlite3
from datetime import date, timedelta

rnd = random.Random(2026)
OUT = os.path.join(os.path.dirname(__file__), "..", "Data", "fitness.db")

FIRST = ["Anna", "Luca", "Mia", "Noah", "Lea", "Jonas", "Lara", "Elias", "Nina", "David",
         "Sara", "Leon", "Julia", "Tim", "Laura", "Nico", "Lena", "Samuel", "Alina", "Fabian",
         "Chiara", "Simon", "Elena", "Marco", "Sophie", "Jan", "Selina", "Reto", "Andrea", "Urs"]
LAST = ["Müller", "Meier", "Schmid", "Keller", "Weber", "Huber", "Schneider", "Meyer",
        "Steiner", "Fischer", "Gerber", "Brunner", "Baumann", "Frei", "Zimmermann", "Moser",
        "Widmer", "Wyss", "Graf", "Roth", "Suter", "Bühler", "Kälin", "Hofer"]
CITIES = ["Bern", "Zürich", "Basel", "Luzern", "Winterthur", "Thun", "Biel", "Olten"]

STUDIOS = [
    ("ST01", "MoveFit Bahnhof", "Bern", 2015),
    ("ST02", "MoveFit Oerlikon", "Zürich", 2017),
    ("ST03", "MoveFit Gundeli", "Basel", 2018),
    ("ST04", "MoveFit Seebad", "Luzern", 2019),
    ("ST05", "MoveFit Altstadt", "Winterthur", 2021),
    ("ST06", "MoveFit Wankdorf", "Bern", 2026),   # neu eröffnet, noch keine Kurse
]
COURSES = [  # courseid, title, category, duration_min, level, price
    ("CO01", "Power Yoga", "Yoga", 60, "mittel", 24.0),
    ("CO02", "Yin Yoga", "Yoga", 75, "einfach", 26.0),
    ("CO03", "Indoor Cycling", "Ausdauer", 45, "mittel", 20.0),
    ("CO04", "Cycling Endurance", "Ausdauer", 60, "schwer", 22.0),
    ("CO05", "HIIT Express", "Kraft", 30, "schwer", 18.0),
    ("CO06", "Bodypump", "Kraft", 55, "mittel", 22.0),
    ("CO07", "Functional Training", "Kraft", 60, "schwer", 24.0),
    ("CO08", "Pilates Basic", "Pilates", 50, "einfach", 25.0),
    ("CO09", "Pilates Reformer", "Pilates", 50, "mittel", 32.0),
    ("CO10", "Zumba", "Tanz", 60, "einfach", 19.0),
    ("CO11", "Dance Cardio", "Tanz", 45, "mittel", 19.0),
    ("CO12", "Rückenfit", "Gesundheit", 45, "einfach", 21.0),
    ("CO13", "Mobility", "Gesundheit", 45, "einfach", 21.0),
    ("CO14", "Boxen", "Kraft", 60, "schwer", 26.0),
    ("CO15", "Aqua Fit", "Gesundheit", 45, "einfach", 23.0),   # noch nie angeboten
]
STUDIO_SURCHARGE = {"ST02": 3.0}   # Zürich ist teurer


def mail(first, last):
    tr = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "é": "e"})
    return f"{first}.{last}".lower().translate(tr) + "@example.ch"


def main():
    if os.path.exists(OUT):
        os.remove(OUT)
    con = sqlite3.connect(OUT)
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE studios  (studioid TEXT PRIMARY KEY, name TEXT, city TEXT, opened_year INTEGER);
    CREATE TABLE courses  (courseid TEXT PRIMARY KEY, title TEXT, category TEXT,
                           duration_min INTEGER, level TEXT);
    CREATE TABLE trainers (trainerid TEXT PRIMARY KEY, firstname TEXT, lastname TEXT,
                           studioid TEXT REFERENCES studios(studioid), hourly_rate REAL);
    CREATE TABLE sessions (sessionid TEXT PRIMARY KEY, courseid TEXT REFERENCES courses(courseid),
                           studioid TEXT REFERENCES studios(studioid),
                           trainerid TEXT REFERENCES trainers(trainerid),
                           session_date TEXT, start_time TEXT, capacity INTEGER, base_price REAL);
    CREATE TABLE members  (memberid TEXT PRIMARY KEY, firstname TEXT, lastname TEXT, city TEXT,
                           birth_year INTEGER, membership_type TEXT, signup_date TEXT, email TEXT);
    CREATE TABLE bookings (bookingid TEXT PRIMARY KEY, sessionid TEXT REFERENCES sessions(sessionid),
                           memberid TEXT REFERENCES members(memberid), booking_date TEXT,
                           paid_price REAL, status TEXT);
    """)

    cur.executemany("INSERT INTO studios VALUES (?,?,?,?)", STUDIOS)
    cur.executemany("INSERT INTO courses VALUES (?,?,?,?,?)", [c[:5] for c in COURSES])
    price = {c[0]: c[5] for c in COURSES}

    # Trainer: 29 fest einem der aktiven Studios zugeteilt, TR030 freischaffend (ohne Studio)
    trainers = []
    for i in range(1, 31):
        sid = None if i == 30 else STUDIOS[(i - 1) % 5][0]
        trainers.append((f"TR{i:03d}", rnd.choice(FIRST), rnd.choice(LAST), sid,
                         float(rnd.randrange(45, 96, 5))))
    cur.executemany("INSERT INTO trainers VALUES (?,?,?,?,?)", trainers)
    by_studio = {}
    for t in trainers:
        by_studio.setdefault(t[3], []).append(t[0])

    # Kurstermine: 300 Termine in ST01–ST05 mit CO01–CO14
    sessions = []
    start = date(2026, 1, 5)
    for i in range(1, 301):
        sid = rnd.choices(["ST01", "ST02", "ST03", "ST04", "ST05"], weights=[24, 26, 18, 17, 15])[0]
        cid = rnd.choice([c[0] for c in COURSES[:14]])
        tid = "TR030" if rnd.random() < 0.04 else rnd.choice(by_studio[sid])
        d = start + timedelta(days=rnd.randrange(0, 175))
        sessions.append((f"SE{i:04d}", cid, sid, tid, d.isoformat(),
                         rnd.choice(["07:00", "09:30", "12:15", "17:30", "18:45", "20:00"]),
                         rnd.choice([12, 15, 20, 25]),
                         price[cid] + STUDIO_SURCHARGE.get(sid, 0.0)))
    cur.executemany("INSERT INTO sessions VALUES (?,?,?,?,?,?,?,?)", sessions)

    # Mitglieder
    types = ["Basic", "Premium", "Student", "Senior"]
    members = []
    for i in range(1, 501):
        f, l = rnd.choice(FIRST), rnd.choice(LAST)
        mt = rnd.choices(types, weights=[45, 25, 20, 10])[0]
        by = {"Student": rnd.randint(1998, 2007), "Senior": rnd.randint(1940, 1961)}.get(
            mt, rnd.randint(1962, 2005))
        signup = date(2023, 1, 1) + timedelta(days=rnd.randrange(0, 1100))
        members.append([f"ME{i:04d}", f, l, rnd.choice(CITIES), by, mt, signup.isoformat(), mail(f, l)])
    for idx in rnd.sample(range(500), 15):       # fehlende E-Mail
        members[idx][7] = None
    bad_mail = rnd.sample([i for i in range(500) if members[i][7]], 3)
    members[bad_mail[0]][7] = "n/a"
    members[bad_mail[1]][7] = members[bad_mail[1]][7].replace("@example.ch", "@example")
    members[bad_mail[2]][7] = ""
    members[41][4] = 1890                         # unplausible Geburtsjahre
    members[287][4] = 2031
    dirty = [("Petra", "Kunz", "basic"), ("Beat", "Lehmann", "BASIC"), ("Ines", "Arnold", "Basik"),
             ("Kurt", "Vogel", "premium"), ("Mara", "Sutter", "student")]
    for k, (f, l, mt) in enumerate(dirty, start=501):
        members.append([f"ME{k:04d}", f, l, rnd.choice(CITIES), rnd.randint(1970, 2000), mt,
                        "2026-09-01", mail(f, l)])
    cur.executemany("INSERT INTO members VALUES (?,?,?,?,?,?,?,?)", members)

    # Buchungen: 2000, ein Teil der Mitglieder bucht nie
    never = set(rnd.sample(range(500), 9))
    active = [members[i] for i in range(500) if i not in never]
    discount = {"Basic": 1.0, "Premium": 0.8, "Student": 0.75, "Senior": 0.85}
    sess_by_id = {s[0]: s for s in sessions}
    bookings = []
    overbooked = [s for s in sessions if s[6] == 12][:2]
    plan = [s[0] for s in overbooked for _ in range(14)]           # 2 überbuchte Termine
    rest_pool = [s[0] for s in sessions if s not in overbooked]
    plan += [rnd.choice(rest_pool) for _ in range(2000 - len(plan))]
    rnd.shuffle(plan)
    for i, se_id in enumerate(plan, start=1):
        s = sess_by_id[se_id]
        m = rnd.choice(active)
        factor = discount[m[5]]
        if m[5] == "Basic" and rnd.random() < 0.35:
            factor = 0.9                                          # 10er-Abo
        if rnd.random() < 0.06:
            factor *= 0.5                                         # Gutschein
        paid = round(s[7] * factor * 20) / 20                     # auf 5 Rappen
        sdate = date.fromisoformat(s[4])
        bdate = sdate - timedelta(days=rnd.randrange(0, 15))
        status = rnd.choices(["attended", "no-show", "cancelled"], weights=[85, 8, 7])[0]
        bookings.append([f"BO{i:05d}", se_id, m[0], bdate.isoformat(), paid, status])
    bookings[17][4] = sess_by_id[bookings[17][1]][7] + 6.0       # paid_price > base_price
    bookings[911][4] = sess_by_id[bookings[911][1]][7] + 4.0
    for idx in (233, 1402, 1777):                                 # Buchung nach dem Termin
        s = sess_by_id[bookings[idx][1]]
        bookings[idx][3] = (date.fromisoformat(s[4]) + timedelta(days=3)).isoformat()
    cur.executemany("INSERT INTO bookings VALUES (?,?,?,?,?,?)", bookings)

    con.commit()
    con.close()
    print("geschrieben:", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
