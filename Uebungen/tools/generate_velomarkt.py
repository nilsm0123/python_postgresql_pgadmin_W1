"""Erzeugt die fiktiven Shop-Daten von «VeloMarkt» für die AP02-Vorbereitung.

Ausgabe in Uebungen/Data/velomarkt/:
  html/shop_page_1.html … shop_page_3.html   Produktlisten (Seite 3 wiederholt 6 Produkte)
  html/product_detail.html                   Detailseite mit drei Tabellen
  reviews.json                               Antwort der Reviews-API
  velos_clean.csv                            aufbereitete Daten (inhaltlich nicht geprüft)

Bewusst eingebaute Probleme:
  - 126 Produktkarten für 120 Artikel (Überlappung der Paginierung)
  - Preise mit Tausender-Apostroph (CHF 3'499.–) und «Preis auf Anfrage»
    (nur bei sehr teuren Velos -> MNAR)
  - Tippfehler beim Preis eines «Tour de Suisse»-Velos (eine Null zu viel)
  - Gewicht «k. A.» bei vier zufälligen Velos (MCAR)
  - Akku/Reichweite «–» bei Velos ohne Motor (strukturell fehlend)

Aufruf (im Hauptordner des Repos):  python Uebungen/tools/generate_velomarkt.py
"""
import csv
import json
import os
import random

rnd = random.Random(7)
OUT = os.path.join(os.path.dirname(__file__), "..", "Data", "velomarkt")
NBSP = "\xa0"

# brand, category, model-stem, price range, e-bike?
CATALOG = [
    ("Cube", "E-Mountainbike", ["Stereo Hybrid", "Reaction Hybrid"], (3499, 5999), True),
    ("Cube", "E-Trekking", ["Kathmandu Hybrid", "Nuroad Hybrid"], (2799, 3999), True),
    ("Cube", "City", ["Hyde", "Ella Ride"], (699, 1099), False),
    ("Cube", "Kindervelo", ["Acid 200", "Acid 240", "Numovo"], (279, 549), False),
    ("Specialized", "E-Mountainbike", ["Turbo Levo", "Turbo Kenevo"], (6999, 11999), True),
    ("Specialized", "Rennvelo", ["Tarmac", "Allez", "Aethos"], (1299, 8999), False),
    ("Trek", "E-Trekking", ["Allant+", "Verve+"], (3499, 5499), True),
    ("Trek", "Gravel", ["Checkpoint", "Domane AL"], (1499, 3999), False),
    ("Trek", "Kindervelo", ["Precaliber", "Wahoo"], (299, 599), False),
    ("Stromer", "S-Pedelec", ["ST3", "ST5", "ST7"], (6990, 12990), True),
    ("Flyer", "E-Trekking", ["Upstreet", "Gotour"], (3999, 5999), True),
    ("Flyer", "E-City", ["Upstreet 1", "Gotour 2"], (3499, 4999), True),
    ("Scott", "Gravel", ["Addict Gravel", "Speedster Gravel"], (1599, 5499), False),
    ("Scott", "E-Mountainbike", ["Patron eRIDE", "Strike eRIDE"], (4999, 8999), True),
    ("Canyon", "Rennvelo", ["Endurace", "Ultimate"], (1699, 6999), False),
    ("Canyon", "Gravel", ["Grizl", "Grail"], (1899, 4999), False),
    ("Tour de Suisse", "E-City", ["Bern", "Basel", "Genf"], (1999, 3299), True),
    ("Tour de Suisse", "City", ["Rapide", "Classic"], (599, 999), False),
]
COLORS = ["Schwarz", "Weiss", "Grau", "Blau", "Rot", "Grün", "Sand", "Petrol"]
AVAIL = ["Sofort lieferbar", "Lieferbar in 2–5 Tagen", "Lieferbar in 3–4 Wochen", "Ausverkauft"]
SIZES = ["S", "M", "L", "XL"]


def chf(p):
    s = f"{p:,}".replace(",", "'")
    return f"CHF{NBSP}{s}.–"


def make_products():
    products = []
    pid = 30001
    # 120 Produkte, Katalog zyklisch durchlaufen
    while len(products) < 120:
        for brand, cat, stems, (lo, hi), ebike in CATALOG:
            if len(products) >= 120:
                break
            stem = rnd.choice(stems)
            price = rnd.randrange(lo, hi + 1, 100) - 1 if hi - lo > 200 else rnd.randrange(lo, hi + 1, 10) - 1
            price = max(price, lo)
            weight = {"Kindervelo": rnd.uniform(6.5, 11), "Rennvelo": rnd.uniform(6.8, 9.5),
                      "Gravel": rnd.uniform(8.5, 11.5), "City": rnd.uniform(12, 17)}.get(
                cat, rnd.uniform(21, 28.5))
            battery = rnd.choice([500, 545, 625, 750, 800, 983]) if ebike else None
            rng = (round(battery / 5.5 / 5) * 5 if battery else None)
            products.append({
                "product_id": f"VM-{pid}", "brand": brand,
                "model": f"{stem} {rnd.choice(['', 'Pro', 'SL', 'EX', 'Comp', 'One'])}".strip(),
                "category": cat, "size": rnd.choice(SIZES), "color": rnd.choice(COLORS),
                "weight_kg": round(weight, 1), "battery_wh": battery, "range_km": rng,
                "price_chf": float(price), "availability": rnd.choices(AVAIL, weights=[45, 30, 15, 10])[0],
            })
            pid += rnd.choice([1, 1, 2, 3])
    return products


def main():
    os.makedirs(os.path.join(OUT, "html"), exist_ok=True)
    products = make_products()

    # «Preis auf Anfrage»: alle Velos ab CHF 9'000 (MNAR)
    expensive = [p for p in products if p["price_chf"] >= 9000]
    on_request = {p["product_id"] for p in expensive}
    # Gewicht «k. A.» bei vier zufälligen Velos (MCAR)
    no_weight = {p["product_id"] for p in rnd.sample(products, 4)}
    # Tippfehler im aufbereiteten Datensatz: ein Velo der günstigen Marke
    # «Tour de Suisse» erhält eine Null zu viel (z. B. 2'999 -> 29'990)
    typo = next(p for p in products if p["brand"] == "Tour de Suisse" and p["category"] == "E-City")
    typo_id = typo["product_id"]
    typo_price = typo["price_chf"] * 10 + 1

    # ---------- HTML-Listenseiten ----------
    pages = {1: products[0:40], 2: products[40:80], 3: products[74:120]}   # 6 Duplikate
    for page, items in pages.items():
        cards = []
        for p in items:
            price = "Preis auf Anfrage" if p["product_id"] in on_request else chf(int(p["price_chf"]))
            weight = "k. A." if p["product_id"] in no_weight else f"{p['weight_kg']:.1f}".replace(".", ",") + f"{NBSP}kg"
            battery = f"{p['battery_wh']}{NBSP}Wh" if p["battery_wh"] else "–"
            rng = f"bis {p['range_km']}{NBSP}km" if p["range_km"] else "–"
            cards.append(f"""      <div class="product-card" data-product-id="{p['product_id']}">
        <h3><span class="brand">{p['brand']}</span> <span class="model">{p['model']}</span></h3>
        <ul class="specs">
          <li class="category">{p['category']}</li>
          <li class="size">Rahmengrösse {p['size']}</li>
          <li class="color">{p['color']}</li>
          <li class="weight">{weight}</li>
          <li class="battery">{battery}</li>
          <li class="range">{rng}</li>
        </ul>
        <div class="buy">
          <span class="price">{price}</span>
          <span class="availability">{p['availability']}</span>
        </div>
      </div>""")
        active = ' class="active"'
        nav = " ".join(f'<a href="shop_page_{i}.html"{active if i == page else ""}>{i}</a>'
                       for i in (1, 2, 3))
        html = f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <title>VeloMarkt – Velos &amp; E-Bikes – Seite {page}</title>
</head>
<body>
  <header>
    <h1>VeloMarkt</h1>
    <p class="result-count">120 Artikel</p>
  </header>
  <main>
    <section class="product-list">
{chr(10).join(cards)}
    </section>
    <nav class="pagination">{nav}</nav>
  </main>
  <footer>VeloMarkt AG · fiktiver Online-Shop für Übungszwecke</footer>
</body>
</html>
"""
        with open(os.path.join(OUT, "html", f"shop_page_{page}.html"), "w", encoding="utf-8") as f:
            f.write(html)

    # ---------- Detailseite ----------
    detail = """<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <title>Flyer Upstreet 5.23 – VeloMarkt</title>
</head>
<body>
  <h1>Flyer Upstreet 5.23</h1>
  <p class="price">CHF&nbsp;5'299.–</p>

  <h2>Preisverlauf</h2>
  <table class="data-table">
    <tr><td>März 2026</td><td>CHF 5'699.–</td></tr>
    <tr><td>Juni 2026</td><td>CHF 5'499.–</td></tr>
    <tr><td>September 2026</td><td>CHF 5'299.–</td></tr>
  </table>

  <h2>Technische Daten</h2>
  <table class="data-table">
    <tr><td colspan="2" class="section">Antrieb</td></tr>
    <tr><td>Motor</td><td>Panasonic GX Ultimate</td></tr>
    <tr><td>Drehmoment</td><td>90 Nm</td></tr>
    <tr><td colspan="2" class="section">Akku</td></tr>
    <tr><td>Kapazität</td><td>750 Wh</td></tr>
    <tr><td>Reichweite</td><td>bis 140 km</td></tr>
    <tr><td>Ladezeit</td><td>5 h</td></tr>
    <tr><td colspan="2" class="section">Rahmen &amp; Ausstattung</td></tr>
    <tr><td>Rahmen</td><td>Aluminium</td></tr>
    <tr><td>Gewicht</td><td>26,8 kg</td></tr>
    <tr><td>Schaltung</td><td>Enviolo Automatiq</td></tr>
    <tr><td>Bremsen</td><td>Magura MT4 hydraulisch</td></tr>
  </table>

  <h2>Lieferung</h2>
  <table class="data-table">
    <tr><td>Versand</td><td>CHF 99.–</td></tr>
    <tr><td>Abholung Filiale</td><td>kostenlos</td></tr>
  </table>
</body>
</html>
"""
    with open(os.path.join(OUT, "html", "product_detail.html"), "w", encoding="utf-8") as f:
        f.write(detail)

    # ---------- reviews.json ----------
    reviews = []
    for old in ("VM-29911", "VM-29954", "VM-29987", "VM-29999"):           # nicht mehr im Sortiment
        reviews.append({"product_id": old, "review_count": rnd.randint(40, 300),
                        "avg_score": round(rnd.uniform(3.0, 4.6), 1)})
    for p in rnd.sample(products, 95):
        base = 3.3 + 0.9 * min(p["price_chf"], 9000) / 9000                # leichter Preiseffekt
        score = min(5.0, max(1.0, rnd.gauss(base, 0.45)))
        reviews.append({"product_id": p["product_id"],
                        "review_count": rnd.choice([1, 2, 3]) if rnd.random() < 0.1 else rnd.randint(8, 420),
                        "avg_score": round(score, 1)})
    reviews.sort(key=lambda r: r["product_id"])
    with open(os.path.join(OUT, "reviews.json"), "w", encoding="utf-8") as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # ---------- velos_clean.csv ----------
    cols = ["product_id", "brand", "model", "category", "size", "color",
            "weight_kg", "battery_wh", "range_km", "price_chf", "availability"]
    with open(os.path.join(OUT, "velos_clean.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for p in products:
            row = dict(p)
            if p["product_id"] in on_request:
                row["price_chf"] = ""
            if p["product_id"] == typo_id:
                row["price_chf"] = typo_price                                 # Tippfehler
            if p["product_id"] in no_weight:
                row["weight_kg"] = ""
            row["battery_wh"] = row["battery_wh"] or ""
            row["range_km"] = row["range_km"] or ""
            w.writerow([row[c] for c in cols])

    print("geschrieben nach", os.path.abspath(OUT))
    print("Preis auf Anfrage:", sorted(on_request))
    print("Tippfehler:", typo_id)


if __name__ == "__main__":
    main()
