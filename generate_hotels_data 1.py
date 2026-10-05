import requests
import csv
import time
import os

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY n'est pas définie. Configurez-la dans une variable d'environnement."
    )

ENDPOINT = "https://places.googleapis.com/v1/places:searchText"

HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": (
        "places.displayName,"
        "places.formattedAddress,"
        "places.location,"
        "places.rating,"
        "places.priceLevel,"
        "places.types"
    )
}

def search_hotels(city, max_results=50):
    body = {
        "textQuery": f"hotels in {city} Morocco"
    }

    response = requests.post(ENDPOINT, headers=HEADERS, json=body)

    if response.status_code != 200:
        print("Erreur API:", response.text)
        return []

    data = response.json().get("places", [])
    hotels = []

    for p in data[:max_results]:
        hotel = {
            "name": p.get("displayName", {}).get("text"),
            "address": p.get("formattedAddress"),
            "lat": p.get("location", {}).get("latitude"),
            "lng": p.get("location", {}).get("longitude"),
            "rating": p.get("rating"),
            "price_level": p.get("priceLevel"),
            "types": ",".join(p.get("types", [])),
            "city": city
        }
        hotels.append(hotel)

    return hotels


# ----------- MAIN ---------------

villes = ["Casablanca", "Marrakech", "Rabat", "Fès", "Agadir"]

all_hotels = []

for city in villes:
    print(f"Ville : {city}")
    hotels = search_hotels(city, max_results=100)
    print(f"{len(hotels)} hôtels trouvés.")
    all_hotels.extend(hotels)
    time.sleep(1)  # éviter rate-limit

# --------- SAVE CSV -------------

with open("hotels_new_api.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=all_hotels[0].keys())
    writer.writeheader()
    writer.writerows(all_hotels)

print("✔ Dataset généré avec succès !")
