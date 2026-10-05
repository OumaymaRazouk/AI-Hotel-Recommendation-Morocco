#!/usr/bin/env python3
import pandas as pd
import numpy as np
import random

SOURCE_FILE = "Hotels_Maroc_Complet.csv"
OUTPUT_FILE = "hotels_maroc_30000_equilibres.csv"
TARGET_ROWS = 30000

random.seed(42)
rng = np.random.default_rng(42)

# ------------------
# 1) Chargement
# ------------------
df = pd.read_csv(SOURCE_FILE)

# Harmoniser les noms de colonnes sources
df = df.rename(columns={
    "Nom": "Hotel",
    "Saison_Recommandée": "Saison_src",
    "Activités_Proposées": "Activites_src",
    "Budget_Estimé": "Budget_src",
    "Durée_Séjour_Recommandée": "Duree_src",
    "Accessibilité": "Accessibilite_src",
    "Sécurité": "Securite_src",
})

# Liste de toutes les villes
cities = sorted(df["Ville"].dropna().unique())
n_cities = len(cities)
if n_cities == 0:
    raise ValueError("Aucune ville trouvée dans Hotels_Maroc_Complet.csv")

# On calcule un nombre de lignes par ville aussi égal que possible
base_per_city = TARGET_ROWS // n_cities
remainder = TARGET_ROWS % n_cities  # quelques villes auront +1 si nécessaire

def rows_for_city(idx_city: int) -> int:
    """Retourne le nombre de lignes à générer pour cette ville (pour obtenir ~30000 lignes)."""
    return base_per_city + (1 if idx_city < remainder else 0)

# ------------------
# 2) Listes pour variations
# ------------------
type_synonyms = [
    "Hôtel de charme",
    "Hôtel moderne",
    "Hôtel familial",
    "Hôtel économique",
    "Hôtel de luxe",
    "Hôtel boutique",
    "Maison d'hôtes",
    "Hôtel spa",
]

services_pool = [
    "WiFi gratuit", "Piscine", "Spa", "Restaurant", "Bar", "Salle de sport",
    "Service de chambre", "Parking gratuit", "Climatisation",
    "Petit-déjeuner inclus", "Navette aéroport", "Centre d'affaires",
    "Terrasse", "Jardin", "Vue sur mer", "Vue sur montagne",
    "Balcon", "Coffre-fort", "Blanchisserie", "Réception 24h/24",
]

description_prefixes = [
    "Séjournez dans un établissement idéalement situé. ",
    "Profitez d'un cadre agréable et d'un service de qualité. ",
    "Un hébergement parfait pour découvrir la région. ",
    "Une adresse appréciée pour son confort et son ambiance. ",
]

description_suffixes = [
    " Idéal pour les séjours en famille comme pour les voyages d'affaires.",
    " Parfait pour un séjour de détente et de découverte.",
    " Un excellent point de départ pour explorer la ville.",
    " Une expérience authentique au cœur du Maroc.",
]

def fr_type(base_type: str) -> str:
    """Traduire / enrichir le type en français avec des synonymes."""
    # On ignore la valeur exacte et on choisit un type FR plausible
    return random.choice(type_synonyms)


def normalize_saison(s: str) -> str:
    s = str(s).lower()
    if "printemps" in s:
        return "Printemps"
    if "été" in s or "ete" in s:
        return "Été"
    if "automne" in s:
        return "Automne"
    if "hiver" in s:
        return "Hiver"
    return "Toute l'année"


def build_score_utilisateur(rating) -> str:
    try:
        val = float(rating)
    except Exception:
        return ""
    if val >= 4.5:
        label = "Excellent"
    elif val >= 4.0:
        label = "Très bien"
    elif val >= 3.5:
        label = "Bien"
    else:
        label = "Correct"
    return f"{label} ({val:.1f}/5)"


def price_from_budget(cat: str) -> int:
    s = str(cat).lower()
    # cat exemples: Économique, Moyen, Premium, Luxe
    if "économique" in s or "economique" in s:
        return random.randint(150, 400)
    if "moyen" in s:
        return random.randint(400, 700)
    if "premium" in s:
        return random.randint(700, 1200)
    if "luxe" in s:
        return random.randint(1200, 2000)
    # fallback
    return random.randint(200, 900)


def augment_activites(txt: str) -> str:
    parts = [p.strip() for p in str(txt).split(",") if p.strip()]
    rng.shuffle(parts)
    return ", ".join(parts)


def augment_description(desc: str) -> str:
    """Ancienne fonction d'enrichissement de description (non utilisée désormais).

    On conserve désormais la description originale du dataset source
    pour que le contenu reste 100% réel.
    """
    return str(desc).strip()


def build_services() -> str:
    # Tirer 4 à 8 services aléatoires
    k = random.randint(4, 8)
    return ", ".join(random.sample(services_pool, k))


def build_accessibilite(txt: str) -> str:
    """Diversifie la formulation de l'accessibilité en restant fidèle au sens.

    On détecte quelques catégories (proche gare, centre-ville, voiture, transport public)
    et on choisit une paraphrase française adaptée. Sinon, on renvoie le texte original.
    """
    base = str(txt).strip()
    s = base.lower()

    # Proche d'une gare ou station
    if "gare" in s or "station" in s:
        variants = [
            "Situé à proximité d'une gare ou d'une station de transport",
            "À quelques minutes à pied d'une gare ou station",
            "Accès facile grâce à la proximité de la gare ou de la station",
        ]
        return random.choice(variants)

    # Proche du centre-ville / taxis
    if "centre-ville" in s or "centre ville" in s or "taxis" in s:
        variants = [
            "Proche du centre-ville et facilement desservi par les taxis",
            "À quelques minutes du centre-ville, accès simple en taxi",
            "Idéalement placé près du centre-ville avec de nombreux taxis disponibles",
        ]
        return random.choice(variants)

    # Accessible en voiture uniquement
    if "voiture" in s:
        variants = [
            "Accès principalement en voiture, avec routes bien indiquées",
            "Accessible en voiture uniquement, parking généralement disponible",
            "Accès recommandé en voiture, accès routier facile",
        ]
        return random.choice(variants)

    # Transport public / facile d'accès
    if "transport public" in s or "facile d’accès" in s or "facile d'accès" in s:
        variants = [
            "Facilement accessible en transports publics",
            "Bonne desserte par les transports en commun",
            "Accès simple via bus ou tram à proximité",
        ]
        return random.choice(variants)

    # Par défaut : texte original nettoyé
    return base


def build_securite(txt: str) -> str:
    return str(txt).strip()

# ------------------
# 3) Génération équilibrée par ville
# ------------------
rows_out = []

for idx_city, city in enumerate(cities):
    df_city = df[df["Ville"] == city].reset_index(drop=True)
    if df_city.empty:
        continue

    n_rows = rows_for_city(idx_city)
    # on échantillonne avec remise
    idx_sample = rng.integers(0, len(df_city), size=n_rows)

    for idx in idx_sample:
        base = df_city.iloc[int(idx)]

        rating_val = base.get("Rating", 0.0)
        prix_nuit = price_from_budget(base.get("Budget_src", ""))

        row = {
            "Ville": city,
            "Type": fr_type(base.get("Type", "")),
            "Saison_ideale": normalize_saison(base.get("Saison_src", "")),
            "Activites": augment_activites(base.get("Activites_src", "")),
            # On conserve la description originale telle qu'elle figure dans Hotels_Maroc_Complet
            "Description": str(base.get("Description", "")).strip(),
            "Budget_estime": f"{prix_nuit}DH/nuit",
            "Score_utilisateur": build_score_utilisateur(rating_val),
            "Duree_suggeree": str(base.get("Duree_src", "")).strip(),
            "Accessibilite": build_accessibilite(base.get("Accessibilite_src", "")),
            "Securite_confort": build_securite(base.get("Securite_src", "")),
            "Hotel": str(base.get("Hotel", "")).strip(),
            "Latitude": float(base.get("Latitude", 0.0)),
            "Longitude": float(base.get("Longitude", 0.0)),
            "GoogleMap_URL": str(base.get("GoogleMap_URL", "")).strip(),
            "Services": build_services(),
            "Rating": float(rating_val),
            "Prix_nuit": int(prix_nuit),
        }
        rows_out.append(row)


df_out = pd.DataFrame(rows_out)

# Normalement len(df_out) == TARGET_ROWS si la division tombe juste.
# Par sécurité, si on a un tout petit peu plus, on tronque sans créer de nouvelles lignes.
if len(df_out) > TARGET_ROWS:
    df_out = df_out.sample(n=TARGET_ROWS, random_state=42).reset_index(drop=True)

df_out = df_out.sample(frac=1, random_state=42).reset_index(drop=True)

print("Forme finale :", df_out.shape)
df_out.to_csv(OUTPUT_FILE, sep=";", index=False, encoding="utf-8")
print(f"Dataset généré : {OUTPUT_FILE}")
