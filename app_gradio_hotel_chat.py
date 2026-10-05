# app_gradio_hotel_chat.py
# Chat type "ChatGPT" pour recommandation d'hôtels (hybride: embeddings + TF‑IDF + numériques + géo)
# Utilise le corpus d'entraînement: moroccan_tourism_dataset_clean_train.csv

import os
import re
import math
import time
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any

import gradio as gr
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# =====================
# Config et chemins
# =====================
DATASET_PREFIX = "hotels_maroc_30000_equilibres"
TRAIN_DATA_PATH = f"{DATASET_PREFIX}_clean_train.csv"
MODEL_NAME = os.environ.get("HF_EMBED_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
EMB_TRAIN_PATH = f"embeddings_{DATASET_PREFIX}_{MODEL_NAME.split('/')[-1]}_train.npy"
VECT_PATH = f"tfidf_vectorizer_{DATASET_PREFIX}.pkl"

# Pondérations par défaut
DEFAULT_WEIGHTS = {"dense": 0.55, "lex": 0.30, "rating": 0.10, "price": 0.05, "geo": 0.10}

# =====================
# Utilitaires
# =====================

def clean_text(s: Any) -> str:
    if pd.isna(s):
        return ""
    s = str(s).replace("\n", " ").replace("\r", " ").strip().lower()
    return s


def haversine_scores(lat_arr, lon_arr, q_lat, q_lon, cap_km=50.0):
    if (q_lat is None) or (q_lon is None):
        return np.zeros_like(lat_arr, dtype=float)
    R = 6371.0
    lat1 = np.radians(float(q_lat))
    lat2 = np.radians(lat_arr.astype(float))
    dlat = np.radians(lat_arr.astype(float) - float(q_lat))
    dlon = np.radians(lon_arr.astype(float) - float(q_lon))
    a = np.sin(dlat/2.0)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2.0)**2
    c = 2*np.arctan2(np.sqrt(a), np.sqrt(1-a))
    dist = R*c
    dist = np.where(np.isfinite(dist), dist, 1e9)
    s = 1.0 - np.minimum(dist/float(cap_km), 1.0)
    return np.where(np.isfinite(s), s, 0.0)


def parse_message_for_constraints(msg: str, cities_set) -> Dict[str, Any]:
    msg_l = msg.lower()
    # ville
    city = None
    for c in cities_set:
        if c and c in msg_l:
            city = c
            break
    # budget / prix
    price_target = None
    if any(k in msg_l for k in ["dh", "mad", "prix", "budget", "dirham"]):
        nums = re.findall(r"\d+", msg_l)
        if nums:
            price_target = float(nums[0])
    # min rating
    min_rating = None
    m = re.search(r"(\d(?:\.\d)?)\s*/\s*5", msg_l)
    if m:
        try:
            min_rating = float(m.group(1))
        except Exception:
            pass
    else:
        m2 = re.search(r"(note|rating|etoile|étoile)\D*(\d(?:\.\d)?)", msg_l)
        if m2:
            try:
                min_rating = float(m2.group(2))
            except Exception:
                pass
    return {"city": city, "price_target": price_target, "min_rating": min_rating}


def as_paragraph(row: pd.Series) -> str:
    name = row.get("Hotel", "") or "(Hôtel)"
    city = row.get("Ville", "") or ""
    typ = row.get("Type", "") or ""
    rating_str = row.get("Rating", "")
    prix = row.get("Prix_nuit", "")
    desc = row.get("Description", "") or ""
    services = row.get("Services", "") or ""
    # Paragraphe concis
    para = f"{name} à {city} est un {typ} noté {rating_str}/5, proposé à {prix} DH/nuit. {desc} Services: {services}."
    return para


# =====================
# Chargement du corpus TRAIN
# =====================
if not os.path.exists(TRAIN_DATA_PATH):
    raise FileNotFoundError(f"Fichier introuvable: {TRAIN_DATA_PATH}. Générez-le via prepare_tourism_data_with_report.py")

_df = pd.read_csv(TRAIN_DATA_PATH, sep=";")
# Colonnes texte pour full_text
TEXT_COLS = [
    "Ville", "Hotel", "Type", "Saison_ideale", "Activites", "Description",
    "Accessibilite", "Securite_confort", "Services", "Score_utilisateur", "GoogleMap_URL",
]
for c in TEXT_COLS:
    if c in _df.columns:
        _df[c] = _df[c].apply(clean_text)
used_cols = [c for c in TEXT_COLS if c in _df.columns]
_df["full_text"] = _df[used_cols].apply(lambda r: " | ".join([x for x in r if x]), axis=1)

# Numériques / géo
_rating = pd.to_numeric(_df.get("Rating"), errors="coerce").fillna(0.0).to_numpy()
_rating_norm = np.clip(_rating / 5.0, 0.0, 1.0)
_price = pd.to_numeric(_df.get("Prix_nuit"), errors="coerce").fillna(0.0).to_numpy()
_lat = pd.to_numeric(_df.get("Latitude"), errors="coerce").to_numpy()
_lon = pd.to_numeric(_df.get("Longitude"), errors="coerce").to_numpy()

# Echelle prix
p_low, p_high = np.nanpercentile(_price, [5, 95])
_price_range = float(max(p_high - p_low, 1.0))

def price_closeness_train(target):
    if target is None:
        return np.zeros_like(_price, dtype=float)
    d = np.abs(_price - float(target))
    return 1.0 - np.minimum(d / _price_range, 1.0)

# Villes connues (pour extraction naive)
cities_set = set(str(v).strip().lower() for v in _df.get("Ville", pd.Series()).dropna().unique())

# TF‑IDF sur TRAIN
if os.path.exists(VECT_PATH):
    try:
        tfidf = joblib.load(VECT_PATH)
    except Exception:
        tfidf = TfidfVectorizer(max_features=20000, ngram_range=(1, 2), stop_words=None)
        tfidf.fit(_df["full_text"])  # fit
        joblib.dump(tfidf, VECT_PATH)
else:
    tfidf = TfidfVectorizer(max_features=20000, ngram_range=(1, 2), stop_words=None)
    tfidf.fit(_df["full_text"])  # fit
    joblib.dump(tfidf, VECT_PATH)

X_tfidf_train = tfidf.transform(_df["full_text"])  # transform

# Embeddings du TRAIN
model = SentenceTransformer(MODEL_NAME)
use_prefix = any(k in MODEL_NAME.lower() for k in ["e5", "gte", "bge"])  # préfixes type e5/gte

if os.path.exists(EMB_TRAIN_PATH):
    try:
        embeddings_train = np.load(EMB_TRAIN_PATH)
    except Exception:
        embeddings_train = None
else:
    embeddings_train = None

if embeddings_train is None:
    texts = _df["full_text"].tolist()
    corpus_texts = [("passage: " + t) if use_prefix else t for t in texts]
    try:
        embeddings_train = model.encode(corpus_texts, batch_size=64, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=True)
    except TypeError:
        embeddings_train = model.encode(corpus_texts, batch_size=64, convert_to_numpy=True)
        norms = np.linalg.norm(embeddings_train, axis=1, keepdims=True) + 1e-12
        embeddings_train = embeddings_train / norms
    np.save(EMB_TRAIN_PATH, embeddings_train)


# =====================
# Recommandation hybride sur TRAIN
# =====================

def recommend_hotels_train(
    query_text: str,
    top_k: int = 5,
    city: str | None = None,
    lat_q: float | None = None,
    lon_q: float | None = None,
    price_target: float | None = None,
    min_rating: float | None = None,
    weights: Dict[str, float] | None = None,
):
    if weights is None:
        weights = dict(DEFAULT_WEIGHTS)
    w = dict(weights)
    if price_target is None:
        w["price"] = 0.0
    if (lat_q is None) or (lon_q is None):
        w["geo"] = 0.0
    s = sum(w.values()) or 1.0
    for k in list(w.keys()):
        w[k] = w[k] / s

    # Dense
    q_text = ("query: " + query_text) if use_prefix else query_text
    try:
        q_vec = model.encode([q_text], convert_to_numpy=True, normalize_embeddings=True)[0]
    except TypeError:
        q_vec = model.encode([q_text], convert_to_numpy=True)[0]
        q_vec = q_vec / (np.linalg.norm(q_vec) + 1e-12)
    dense_scores = embeddings_train.dot(q_vec)

    # Lexical
    v = tfidf.transform([query_text])
    lex_scores = linear_kernel(v, X_tfidf_train).ravel()

    # Numériques / géo
    rating_scores = _rating_norm.copy()
    price_scores = price_closeness_train(price_target)
    geo_scores = haversine_scores(_lat, _lon, lat_q, lon_q)

    final = (
        w.get("dense", 0) * dense_scores
        + w.get("lex", 0) * lex_scores
        + w.get("rating", 0) * rating_scores
        + w.get("price", 0) * price_scores
        + w.get("geo", 0) * geo_scores
    )

    mask = np.ones(_df.shape[0], dtype=bool)
    if city:
        cc = str(city).strip().lower()
        mask &= _df["Ville"].str.contains(cc, na=False)
    if min_rating is not None:
        mask &= (_rating >= float(min_rating))
    # Filtre dur sur le prix si demandé (Prix_nuit <= price_target)
    if price_target is not None:
        try:
            thr = float(price_target)
            mask_price = (_price <= thr)
            # On applique le filtre prix seulement s'il reste au moins un hôtel
            if mask_price.any():
                mask &= mask_price
        except Exception:
            pass

    scores = final.copy()
    scores[~mask] = -1e9

    # Sélection des meilleurs scores avec déduplication par nom d'hôtel
    k = int(max(1, min(top_k, _df.shape[0])))
    order = np.argsort(scores)[::-1]  # tous les indices triés par score décroissant

    seen_hotels = set()
    selected_idx = []
    for idx in order:
        hotel_name = str(_df.iloc[idx].get("Hotel", "")).strip().lower()
        # si pas de nom d'hôtel, on n'applique pas de déduplication spécifique
        key = hotel_name or f"row_{idx}"
        if key in seen_hotels:
            continue
        seen_hotels.add(key)
        selected_idx.append(idx)
        if len(selected_idx) >= k:
            break

    selected_idx = np.array(selected_idx, dtype=int)
    res = _df.iloc[selected_idx].copy()
    res["__score__"] = scores[selected_idx]
    return res


# =====================
# Fonction de réponse Chat
# =====================

def chat_fn(message, history):
    # Extraire contraintes simples
    cons = parse_message_for_constraints(message, cities_set)
    res = recommend_hotels_train(
        query_text=message,
        top_k=5,
        city=cons.get("city"),
        price_target=cons.get("price_target"),
        min_rating=cons.get("min_rating"),
    )
    # Composer la réponse
    parts = []
    parts.append("Voici des recommandations basées sur votre requête.\n")
    for _, r in res.iterrows():
        url = r.get("GoogleMap_URL") or ""
        para = as_paragraph(r)
        # Lien cliquable (Markdown)
        line = f"- {para}\n  [Voir sur Google Maps]({url})" if url else f"- {para}"
        parts.append(line)
    answer = "\n\n".join(parts)
    return answer


# =====================
# Lancer l'app Gradio
# =====================
with gr.Blocks() as app:
    # Injection du CSS personnalisé depuis style.css via une balise <style>
    css_str = ""
    try:
        with open("style.css", "r", encoding="utf-8") as f:
            css_str = f.read()
    except FileNotFoundError:
        css_str = ""

    if css_str:
        gr.HTML(f"<style>{css_str}</style>")

    gr.ChatInterface(
        fn=chat_fn,
        title="Assistant Recommandation Hôtels (Multilingue, Hybride)",
        description=(
            "Posez une question en français, anglais ou autre. L'assistant utilise un mélange d'indices sémantiques "
            "(embeddings), lexicaux (TF-IDF) et numériques (note, prix, distance)."
        ),
    )

if __name__ == "__main__":
    app.launch(server_name="127.0.0.1", server_port=7860, share=False)
