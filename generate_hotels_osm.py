#!/usr/bin/env python3
import requests
import pandas as pd
import random
import time
from urllib.parse import quote
from tqdm import tqdm
import logging

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

output_file = "moroccan_hotels_dataset_full_osm.csv"
target_rows = 30000

villes_maroc = [
    "Marrakech", "Casablanca", "Fès", "Rabat", "Agadir", "Tanger", "Meknès",
    "Oujda", "Tétouan", "Salé", "Kénitra", "El Jadida", "Beni Mellal", "Errachidia",
    "Nador", "Taza", "Settat", "Larache", "Khouribga", "Guelmim", "Jorf El Melha",
    "Laâyoune", "Ksar El Kebir", "Sale", "Bir Lehlou", "Arfoud", "Temara",
    "Mohammedia", "Ifrane", "Taroudant", "Berkane", "Safi", "Fnideq", "Taourirt",
    "Nador", "Essaouira", "Chefchaouen", "Ouarzazate", "Dakhla", "Al Hoceima"
]

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

def get_coordinates_osm(location):
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={quote(location+', Maroc')}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            return None, None
    except Exception as e:
        logger.warning(f"Erreur coordonnées pour {location}: {e}")
        return None, None

def generate_hotel_names(ville, n):
    prefixes = ["Hôtel", "Riad", "Resort", "Auberge", "Maison"]
    suffixes = ["Royal", "Imperial", "Atlas", "Sahara", "Medina", "Palace", "Garden", "View", "Spa", "Beach"]
    hotels = []
    while len(hotels) < n:
        hotel_name = f"{random.choice(prefixes)} {ville} {random.choice(suffixes)}"
        if hotel_name not in hotels:
            hotels.append(hotel_name)
    return hotels

def generate_hotel_criteria(hotel_name, ville):
    # Type
    type_hotel = random.choice(types_hotels)
    if "Riad" in hotel_name: type_hotel = "Riad traditionnel"
    elif "Resort" in hotel_name: type_hotel = "Resort"
    elif "Palace" in hotel_name or "Royal" in hotel_name: type_hotel = "Hôtel de luxe"

    # Services
    services = ", ".join(random.sample(services_hotels, random.randint(5,12)))

    # Budget
    budget_levels = ["Économique (50-100€/nuit)", "Modéré (100-200€/nuit)", "Élevé (200-400€/nuit)", "Luxe (400€+/nuit)"]
    budget = random.choice(budget_levels)

    # Score
    score_levels = ["Excellent (9.0+/10)", "Très bien (8.0-9.0/10)", "Bien (7.0-8.0/10)", "Correct (6.0-7.0/10)"]
    score = random.choice(score_levels)

    # Saison idéale
    saison = random.choice(["Printemps", "Été", "Automne", "Hiver", "Toute l'année"])

    # Activités
    activites_list = ["Visite de la médina", "Excursion dans le désert", "Randonnée en montagne", 
                      "Découverte des souks", "Dégustation culinaire", "Spa et détente",
                      "Visite des monuments historiques", "Shopping traditionnel", "Cours de cuisine",
                      "Excursion en chameau", "Visite des jardins", "Spectacles folkloriques"]
    activites = ", ".join(random.sample(activites_list, random.randint(3,6)))

    # Description
    description_list = [
        f"Magnifique {type_hotel.lower()} situé au cœur de {ville}, offrant un séjour inoubliable.",
        f"Découvrez l'hospitalité marocaine authentique dans ce {type_hotel.lower()} élégant de {ville}.",
        f"Profitez d'un séjour exceptionnel dans ce {type_hotel.lower()} de {ville}, réputé pour son confort.",
        f"Expérience unique dans ce {type_hotel.lower()} à {ville}, parfait pour découvrir la région.",
        f"Séjour de rêve garanti dans ce {type_hotel.lower()} premium de {ville}, avec des prestations haut de gamme."
    ]
    description = random.choice(description_list)

    # Durée suggérée
    duree_options = ["1-2 nuits", "2-3 nuits", "3-5 nuits", "1 semaine", "Week-end"]
    duree = random.choice(duree_options)

    # Accessibilité
    accessibilite_options = ["Accès facile en voiture", "Proche des transports publics", 
                             "Navette aéroport disponible", "Centre-ville accessible à pied",
                             "Parking privé disponible"]
    accessibilite = random.choice(accessibilite_options)

    # Sécurité et confort
    securite_options = ["Quartier sécurisé", "Réception 24h/24", "Service de sécurité",
                        "Zone touristique sûre", "Surveillance vidéo"]
    securite = random.choice(securite_options)

    # Rating
    rating = round(random.uniform(3.5, 5.0),1)

    # Prix nuit en euro
    prix_nuit = random.randint(50,500)

    return {
        "Type": type_hotel,
        "Saison_ideale": saison,
        "Activites": activites,
        "Description": description,
        "Budget_estime": budget,
        "Score_utilisateur": score,
        "Duree_suggeree": duree,
        "Accessibilite": accessibilite,
        "Securite_confort": securite,
        "Services": services,
        "Rating": rating,
        "Prix_nuit": prix_nuit
    }

def generate_hotels_dataset():
    all_data = []
    hotels_per_city = target_rows // len(villes_maroc) + 1
    for ville in tqdm(villes_maroc, desc="Traitement des villes"):
        lat, lon = get_coordinates_osm(ville)
        hotels = generate_hotel_names(ville, hotels_per_city)
        for hotel in hotels[:hotels_per_city]:
            hotel_lat = lat + random.uniform(-0.05,0.05) if lat else 31.7917 + random.uniform(-5,5)
            hotel_lon = lon + random.uniform(-0.05,0.05) if lon else -7.0926 + random.uniform(-5,5)
            criteria = generate_hotel_criteria(hotel, ville)
            google_map_url = f"https://www.google.com/maps/search/{quote(hotel + ' ' + ville)}"
            row = {
                "Ville": ville,
                "Type": criteria["Type"],
                "Saison_ideale": criteria["Saison_ideale"],
                "Activites": criteria["Activites"],
                "Description": criteria["Description"],
                "Budget_estime": criteria["Budget_estime"],
                "Score_utilisateur": criteria["Score_utilisateur"],
                "Duree_suggeree": criteria["Duree_suggeree"],
                "Accessibilite": criteria["Accessibilite"],
                "Securite_confort": criteria["Securite_confort"],
                "Hotel": hotel,
                "Latitude": round(hotel_lat,6),
                "Longitude": round(hotel_lon,6),
                "GoogleMap_URL": google_map_url,
                "Services": criteria["Services"],
                "Rating": criteria["Rating"],
                "Prix_nuit": criteria["Prix_nuit"]
            }
            all_data.append(row)
            if len(all_data) >= target_rows: break
            time.sleep(random.uniform(0.01,0.05))
        if len(all_data) >= target_rows: break
    df = pd.DataFrame(all_data[:target_rows])
    df.to_csv(output_file, index=False, encoding='utf-8')
    logger.info(f"Dataset créé: {output_file} ({len(df)} lignes)")
    return df

if __name__ == "__main__":
    dataset = generate_hotels_dataset()
    print(dataset.head())
