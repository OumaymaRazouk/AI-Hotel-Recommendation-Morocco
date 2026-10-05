#!/usr/bin/env python3
"""
Générateur de données d'hôtels pour recommandations
100% gratuit, illimité, basé sur OpenStreetMap + données aléatoires
Génère 30 000 lignes avec ville + hôtel + critères
"""

import pandas as pd
import random
import time
from tqdm import tqdm
import logging
from geopy.geocoders import Nominatim
import overpy

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ---------- CONFIGURATION ----------
output_file = "moroccan_tourism_dataset_30000_new_hotels_NEW.csv"
target_rows = 30000

# Initialiser geolocator OSM
geolocator = Nominatim(user_agent="my_hotels_app")
api = overpy.Overpass()

# Villes principales du Maroc
villes_maroc = [
    "Marrakech", "Casablanca", "Fès", "Rabat", "Agadir", "Tanger", "Meknès", 
    "Oujda", "Tétouan", "Salé", "Kénitra", "El Jadida", "Beni Mellal", "Errachidia",
    "Nador", "Taza", "Settat", "Larache", "Khouribga", "Guelmim", "Jorf El Melha",
    "Laâyoune", "Ksar El Kebir", "Sale", "Bir Lehlou", "Arfoud", "Temara",
    "Mohammedia", "Ifrane", "Taroudant", "Berkane", "Safi", "Fnideq", "Taourirt",
    "Essaouira", "Chefchaouen", "Ouarzazate", "Dakhla", "Al Hoceima"
]

# Types et services
types_hotels = [
    "Hôtel de luxe", "Hôtel boutique", "Resort", "Riad traditionnel", "Auberge",
    "Hôtel d'affaires", "Hôtel familial", "Hôtel économique", "Maison d'hôtes",
    "Hôtel spa", "Hôtel de charme", "Hôtel moderne"
]

services_hotels = [
    "WiFi gratuit", "Piscine", "Spa", "Restaurant", "Bar", "Salle de sport",
    "Service de chambre", "Parking gratuit", "Climatisation", "Petit-déjeuner inclus",
    "Navette aéroport", "Centre d'affaires", "Terrasse", "Jardin", "Vue sur mer",
    "Vue sur montagne", "Balcon", "Coffre-fort", "Blanchisserie", "Réception 24h/24"
]

# ----------------- FONCTIONS -----------------
def get_city_coordinates(city):
    """Récupère les coordonnées de la ville via OSM"""
    try:
        location = geolocator.geocode(f"{city}, Maroc")
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        logger.warning(f"Erreur géocodage pour {city}: {e}")
    # Valeur par défaut si échec
    return 31.7917, -7.0926

def get_hotels_from_osm(city, max_hotels=15):
    """Récupère les hôtels via Overpass API"""
    hotels = []
    try:
        query = f"""
        area["name"="{city}"]->.searchArea;
        node["tourism"="hotel"](area.searchArea);
        out;
        """
        result = api.query(query)
        for node in result.nodes[:max_hotels]:
            hotel_name = node.tags.get("name")
            if hotel_name:
                hotels.append(hotel_name)
    except Exception as e:
        logger.warning(f"Erreur Overpass pour {city}: {e}")
    # Générer des noms réalistes si pas assez
    while len(hotels) < max_hotels:
        prefix = random.choice(["Hôtel", "Riad", "Resort", "Auberge"])
        suffix = random.choice(["Royal", "Atlas", "Medina", "Palace", "Garden", "Spa"])
        name = f"{prefix} {city} {suffix} {len(hotels)+1}"
        if name not in hotels:
            hotels.append(name)
    return hotels

def generate_hotel_criteria(hotel_name, city):
    """Génère les critères aléatoires pour un hôtel"""
    type_hotel = random.choice(types_hotels)
    if "Riad" in hotel_name:
        type_hotel = "Riad traditionnel"
    elif "Resort" in hotel_name:
        type_hotel = "Resort"
    elif "Palace" in hotel_name or "Royal" in hotel_name:
        type_hotel = "Hôtel de luxe"

    services = ", ".join(random.sample(services_hotels, random.randint(5, 12)))

    price_level = random.randint(1, 4)
    if price_level == 1:
        budget = "Économique (50-100€/nuit)"
    elif price_level == 2:
        budget = "Modéré (100-200€/nuit)"
    elif price_level == 3:
        budget = "Élevé (200-400€/nuit)"
    else:
        budget = "Luxe (400€+/nuit)"

    saisons = ["Printemps", "Été", "Automne", "Hiver", "Toute l'année"]
    saison_ideale = random.choice(saisons)

    descriptions = [
        f"Magnifique {type_hotel.lower()} situé au cœur de {city}, offrant un séjour inoubliable avec des services de qualité supérieure.",
        f"Découvrez l'hospitalité marocaine authentique dans ce {type_hotel.lower()} élégant de {city}, alliant tradition et modernité.",
        f"Profitez d'un séjour exceptionnel dans ce {type_hotel.lower()} de {city}, réputé pour son confort et son service personnalisé.",
        f"Expérience unique dans ce {type_hotel.lower()} de charme à {city}, parfait pour découvrir les merveilles de la région.",
        f"Séjour de rêve garanti dans ce {type_hotel.lower()} premium de {city}, avec des prestations haut de gamme."
    ]
    description = random.choice(descriptions)

    activites = [
        "Visite de la médina", "Excursion dans le désert", "Randonnée en montagne", 
        "Découverte des souks", "Dégustation culinaire", "Spa et détente",
        "Visite des monuments historiques", "Shopping traditionnel", "Cours de cuisine",
        "Excursion en chameau", "Visite des jardins", "Spectacles folkloriques"
    ]
    activites_str = ", ".join(random.sample(activites, random.randint(3, 6)))

    rating = round(random.uniform(3.5, 4.8), 1)
    if rating >= 4.5:
        score = "Excellent (9.0+/10)"
    elif rating >= 4.0:
        score = "Très bien (8.0-9.0/10)"
    elif rating >= 3.5:
        score = "Bien (7.0-8.0/10)"
    else:
        score = "Correct (6.0-7.0/10)"

    duree = random.choice(["1-2 nuits", "2-3 nuits", "3-5 nuits", "1 semaine", "Week-end"])
    accessibilite = random.choice([
        "Accès facile en voiture", "Proche des transports publics", 
        "Navette aéroport disponible", "Centre-ville accessible à pied",
        "Parking privé disponible"
    ])
    securite = random.choice([
        "Quartier sécurisé", "Réception 24h/24", "Service de sécurité",
        "Zone touristique sûre", "Surveillance vidéo"
    ])

    return {
        'Type': type_hotel,
        'Saison_ideale': saison_ideale,
        'Activites': activites_str,
        'Description': description,
        'Budget_estime': budget,
        'Score_utilisateur': score,
        'Duree_suggeree': duree,
        'Accessibilite': accessibilite,
        'Securite_confort': securite,
        'Services': services,
        'Rating': rating
    }

def generate_hotels_dataset():
    logger.info(f"🚀 Génération de {target_rows} lignes de données d'hôtels")
    all_data = []
    hotels_per_city = target_rows // len(villes_maroc) + 1

    for city in tqdm(villes_maroc, desc="Traitement des villes"):
        city_lat, city_lng = get_city_coordinates(city)
        hotels = get_hotels_from_osm(city, max_hotels=hotels_per_city)

        for i, hotel in enumerate(hotels[:hotels_per_city]):
            if len(all_data) >= target_rows:
                break

            # Coordonnées légèrement aléatoires autour de la ville
            hotel_lat = city_lat + random.uniform(-0.05, 0.05)
            hotel_lng = city_lng + random.uniform(-0.05, 0.05)

            criteria = generate_hotel_criteria(hotel, city)

            google_map_url = f"https://www.google.com/maps/search/{hotel} {city}"

            row_data = {
                'Ville': city,
                'Hotel': hotel,
                'Latitude': round(hotel_lat, 6),
                'Longitude': round(hotel_lng, 6),
                'GoogleMap_URL': google_map_url,
                **criteria
            }

            all_data.append(row_data)
            time.sleep(random.uniform(0.01, 0.05))  # pause légère

        if len(all_data) >= target_rows:
            break

    df = pd.DataFrame(all_data[:target_rows])
    df.to_csv(output_file, index=False, encoding='utf-8')
    logger.info(f"✅ Dataset sauvegardé: {output_file}")
    return df

if __name__ == "__main__":
    dataset = generate_hotels_dataset()
    print(f"🎉 Génération terminée avec succès! {len(dataset)} lignes créées")
