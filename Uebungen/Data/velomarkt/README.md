# VeloMarkt — fiktiver Velo-Shop

Daten für die Übungen `20_…ap02` und `21_probepruefung_ap02`. Aufgebaut wie die PhoneMarkt-Daten der Prüfung AP02.
Alle Daten sind frei erfunden und lassen sich mit `python Uebungen/tools/generate_velomarkt.py` neu erzeugen.

## Datenquellen

| Datei | Format | Inhalt |
|---|---|---|
| `html/shop_page_1.html` … `shop_page_3.html` | HTML | gespeicherte Produktlisten-Seiten (Paginierung), je Produkt eine `<div class="product-card">` |
| `html/product_detail.html` | HTML | Detailseite «Flyer Upstreet 5.23» mit drei Tabellen (Preisverlauf, Technische Daten, Lieferung) |
| `reviews.json` | JSON | gespeicherte Antwort der Reviews-API: Liste mit `product_id`, `review_count`, `avg_score` (1–5 Sterne) |
| `velos_clean.csv` | CSV | aufbereitete Shop-Daten: Formate vereinheitlicht, Duplikate entfernt, **inhaltlich nicht geprüft** |

## Spalten in `velos_clean.csv`

| Spalte | Beschreibung |
|---|---|
| `product_id` | Artikelnummer im Shop (`VM-…`) |
| `brand`, `model` | Marke und Modell |
| `category` | E-Mountainbike, E-Trekking, E-City, S-Pedelec, Rennvelo, Gravel, City, Kindervelo |
| `size`, `color` | Rahmengrösse (S–XL) und Farbe |
| `weight_kg` | Gewicht in kg (leer, wenn der Shop «k. A.» anzeigt) |
| `battery_wh` | Akkukapazität in Wattstunden (nur E-Bikes) |
| `range_km` | Reichweite laut Hersteller in km (nur E-Bikes) |
| `price_chf` | Preis in CHF (leer bei «Preis auf Anfrage») |
| `availability` | Lieferstatus |
