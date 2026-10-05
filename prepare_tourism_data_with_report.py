# prepare_tourism_data_with_report.py

import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib  # pip install joblib si besoin
import numpy as np
from scipy.sparse import save_npz
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ==============================
# 1. Chargement du dataset brut
# ==============================

file_path = "hotels_maroc_30000_equilibres_utf8.csv"

df = pd.read_csv(file_path, sep=";", encoding="utf-8")
cols_series = pd.Series(df.columns)
dup_counts = cols_series.value_counts()
duplicate_columns_info = dup_counts[dup_counts > 1].to_dict()
df = df.loc[:, ~pd.Index(df.columns).duplicated(keep='first')]
df_raw = df.copy()  # copie pour le rapport

print("Shape avant nettoyage :", df.shape)
print(df.head(3))


# =================================
# 2. Fonctions utilitaires
# =================================

def clean_text(s: str) -> str:
    """Nettoyage basique du texte."""
    if pd.isna(s):
        return ""
    s = str(s)
    # enlever les retours à la ligne
    s = s.replace("\n", " ").replace("\r", " ")
    # supprimer les espaces multiples
    s = re.sub(r"\s+", " ", s)
    # mettre en minuscule
    s = s.lower()
    return s.strip()


def extract_numeric(value: str):
    """Extrait une valeur numérique d'une chaîne (ex: '83DH/nuit' -> 83)."""
    if pd.isna(value):
        return None
    nums = re.findall(r"[\d\.]+", str(value))
    if not nums:
        return None
    try:
        if "." in nums[0]:
            return float(nums[0])
        else:
            return int(nums[0])
    except ValueError:
        return None


# ========================================
# 3. Nettoyage des colonnes numériques
# ========================================

# Budget_estime du type '83DH/nuit' -> entier/float (ne recrée pas si déjà présent)
if "Budget_estime_num" in df.columns:
    df.drop(columns=["Budget_estime_num"], inplace=True)

# Rating, Prix_nuit -> numériques (on conserve Score_utilisateur texte)
for col in ["Rating", "Prix_nuit"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ========================================
# 4. Nettoyage des colonnes texte
# ========================================

text_cols = [
    "Ville",
    "Type",
    "Saison_ideale",
    "Activites",
    "Description",
    "Accessibilite",
    "Securite_confort",
    "Hotel",
    "Services",
    "Score_utilisateur",
]

for col in text_cols:
    if col in df.columns:
        df[col] = df[col].apply(clean_text)

# ========================================
# 5. Gestion des valeurs manquantes & doublons
# ========================================

df_before = df.copy()  # pour voir l'effet des drop dans le rapport

# suppression des doublons
df.drop_duplicates(inplace=True)

# suppression des lignes sans Description (optionnel – à adapter)
if "Description" in df.columns:
    df = df.dropna(subset=["Description"])

df.reset_index(drop=True, inplace=True)

print("Shape après nettoyage :", df.shape)


# ========================================
# 6. Création d'un texte global pour la reco
# ========================================

def build_full_text(row):
    parts = []
    for c in ["Ville", "Type", "Saison_ideale", "Activites",
              "Description", "Services", "Score_utilisateur"]:
        if c in row and pd.notna(row[c]) and str(row[c]).strip() != "":
            parts.append(str(row[c]))
    return " | ".join(parts)


df["full_text"] = df.apply(build_full_text, axis=1)

print("Exemple full_text :")
print(df["full_text"].iloc[0])


# ========================================
# 7. Pré-entraînement TF-IDF
# ========================================

tfidf = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 2),
    stop_words="french"
)

try:
    X_tfidf = tfidf.fit_transform(df["full_text"])
except ValueError:
    tfidf = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        stop_words=None
    )
    X_tfidf = tfidf.fit_transform(df["full_text"])

print("Shape TF-IDF :", X_tfidf.shape)

# ========================================
# 8. Split train / test (ex: prédire Rating)
# ========================================

target_col = "Rating"  # tu peux changer ici

if target_col in df.columns:
    mask = df[target_col].notna()
    mask_idx = mask.to_numpy()
    indices_all = np.where(mask_idx)[0]
    X_all = X_tfidf[mask_idx]
    y_all = df.loc[mask_idx, target_col].to_numpy()

    pos = np.arange(X_all.shape[0])
    pos_train, pos_test = train_test_split(pos, test_size=0.2, random_state=42)

    X_train = X_all[pos_train]
    X_test = X_all[pos_test]
    y_train = y_all[pos_train]
    y_test = y_all[pos_test]

    orig_train_idx = indices_all[pos_train]
    orig_test_idx = indices_all[pos_test]

    df_train_clean = df.iloc[orig_train_idx].copy()
    df_test_clean = df.iloc[orig_test_idx].copy()

    print("Taille train :", X_train.shape, "— Taille test :", X_test.shape)
else:
    X_train = X_test = y_train = y_test = None
    df_train_clean = df_test_clean = None
    orig_train_idx = orig_test_idx = None
    print(f"⚠ La colonne cible '{target_col}' n'existe pas dans le dataset.")


# ========================================
# 9. SAUVEGARDE DES FICHIERS
# ========================================

df.to_csv("hotels_maroc_30000_equilibres_clean.csv", sep=";", index=False)

joblib.dump(tfidf, "tfidf_vectorizer.pkl")
joblib.dump(
    {
        "X_tfidf": X_tfidf,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
    },
    "tfidf_data_splits.pkl",
)

# Exports complémentaires: fichiers séparés train/test
if X_train is not None:
    save_npz("X_train_tfidf.npz", X_train)
    save_npz("X_test_tfidf.npz", X_test)

    pd.DataFrame({
        "row_index": orig_train_idx,
        target_col: y_train,
    }).to_csv("y_train.csv", index=False)

    pd.DataFrame({
        "row_index": orig_test_idx,
        target_col: y_test,
    }).to_csv("y_test.csv", index=False)

    df_train_clean.to_csv("hotels_maroc_30000_equilibres_clean_train.csv", sep=";", index=False)
    df_test_clean.to_csv("hotels_maroc_30000_equilibres_clean_test.csv", sep=";", index=False)

print("✅ Nettoyage et pré-traitement terminés.")
print("✅ Fichiers générés :")
print("   - hotels_maroc_30000_equilibres_clean.csv")
print("   - tfidf_vectorizer.pkl")
print("   - tfidf_data_splits.pkl")
if X_train is not None:
    print("   - X_train_tfidf.npz")
    print("   - X_test_tfidf.npz")
    print("   - y_train.csv")
    print("   - y_test.csv")
    print("   - hotels_maroc_30000_equilibres_clean_train.csv")
    print("   - hotels_maroc_30000_equilibres_clean_test.csv")


# ========================================
# 10. GÉNÉRATION D'UN RAPPORT TEXTE
# ========================================

report_lines = []

report_lines.append("==== RAPPORT DE NETTOYAGE DE DONNÉES ====")
report_lines.append(f"Généré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report_lines.append("")
report_lines.append("1) INFO GÉNÉRALE AVANT NETTOYAGE")
report_lines.append("-" * 40)
report_lines.append(f"Shape initial (lignes, colonnes) : {df_raw.shape}")
report_lines.append(f"Colonnes : {', '.join(df_raw.columns)}")
report_lines.append("")
if duplicate_columns_info:
    report_lines.append("Colonnes dupliquées supprimées (nom: occurrences) :")
    report_lines.append(str(duplicate_columns_info))
    report_lines.append("")

# valeurs manquantes initiales
report_lines.append("Top 20 des colonnes avec le plus de valeurs manquantes (AVANT) :")
missing_raw = df_raw.isna().sum().sort_values(ascending=False)
report_lines.append(str(missing_raw.head(20)))
report_lines.append("")

# stats numériques avant
num_cols_raw = df_raw.select_dtypes(include=["int64", "float64"]).columns
if len(num_cols_raw) > 0:
    report_lines.append("Statistiques descriptives des variables numériques (AVANT) :")
    report_lines.append(str(df_raw[num_cols_raw].describe().T))
    report_lines.append("")

report_lines.append("\n2) INFO GÉNÉRALE APRÈS NETTOYAGE")
report_lines.append("-" * 40)
report_lines.append(f"Shape après nettoyage (lignes, colonnes) : {df.shape}")
report_lines.append(f"Colonnes : {', '.join(df.columns)}")
report_lines.append("")

# valeurs manquantes après
report_lines.append("Top 20 des colonnes avec le plus de valeurs manquantes (APRÈS) :")
missing_clean = df.isna().sum().sort_values(ascending=False)
report_lines.append(str(missing_clean.head(20)))
report_lines.append("")

# stats numériques après
num_cols_clean = df.select_dtypes(include=["int64", "float64"]).columns
if len(num_cols_clean) > 0:
    report_lines.append("Statistiques descriptives des variables numériques (APRÈS) :")
    report_lines.append(str(df[num_cols_clean].describe().T))
    report_lines.append("")

# Impact des doublons & drop
report_lines.append("\n3) IMPACT DES OPÉRATIONS DE NETTOYAGE")
report_lines.append("-" * 40)
report_lines.append(f"Nombre de lignes initial : {df_raw.shape[0]}")
report_lines.append(f"Nombre de lignes après suppression doublons + NA Description : {df.shape[0]}")
report_lines.append(f"Nombre de lignes supprimées : {df_raw.shape[0] - df.shape[0]}")
report_lines.append("")

# Exemple de distribution d'une variable (Rating, Prix_nuit…)
if "Rating" in df.columns:
    report_lines.append("Distribution de 'Rating' (APRÈS) :")
    report_lines.append(str(df["Rating"].describe()))
    report_lines.append("")
if "Prix_nuit" in df.columns:
    report_lines.append("Distribution de 'Prix_nuit' (APRÈS) :")
    report_lines.append(str(df["Prix_nuit"].describe()))
    report_lines.append("")


# Info TF-IDF
report_lines.append("\n4) INFO TF-IDF")
report_lines.append("-" * 40)
report_lines.append(f"Nombre de documents utilisés pour 'full_text' : {df['full_text'].shape[0]}")
report_lines.append(f"Shape de la matrice TF-IDF : {X_tfidf.shape}")
report_lines.append(f"Nombre de features TF-IDF (vocabulaire) : {len(tfidf.get_feature_names_out())}")
report_lines.append("")

# Info split train/test
report_lines.append("\n5) SPLIT TRAIN / TEST")
report_lines.append("-" * 40)
report_lines.append(f"Colonne cible utilisée : {target_col}")
if X_train is not None:
    report_lines.append(f"Taille X_train : {X_train.shape}")
    report_lines.append(f"Taille X_test  : {X_test.shape}")
    report_lines.append(f"Taille y_train : {y_train.shape}")
    report_lines.append(f"Taille y_test  : {y_test.shape}")
    # distributions
    report_lines.append("\nDistribution de 'Rating' — TRAIN :")
    report_lines.append(str(pd.Series(y_train).describe()))
    report_lines.append("\nDistribution de 'Rating' — TEST :")
    report_lines.append(str(pd.Series(y_test).describe()))
    # fichiers exportés
    report_lines.append("\nFichiers exportés (train/test) :")
    report_lines.append(" - X_train_tfidf.npz")
    report_lines.append(" - X_test_tfidf.npz")
    report_lines.append(" - y_train.csv")
    report_lines.append(" - y_test.csv")
    report_lines.append(" - hotels_maroc_30000_equilibres_clean_train.csv")
    report_lines.append(" - hotels_maroc_30000_equilibres_clean_test.csv")
else:
    report_lines.append("⚠ Aucun split réalisé (colonne cible absente ou invalide).")

# Écriture du rapport dans un fichier .txt
report_filename_txt = "rapport_nettoyage_data.txt"
with open(report_filename_txt, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print("✅ Rapport de nettoyage généré :", report_filename_txt)

# ========================================
# 11. EXPORT DU RAPPORT EN PDF (ReportLab)
# ========================================

report_filename_pdf = "rapport_nettoyage_data.pdf"

def generate_pdf(text_file, output_pdf):
    """Convertit un fichier texte (.txt) en PDF ligne par ligne."""
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4

    x = 40
    y = height - 40
    line_spacing = 14

    with open(text_file, "r", encoding="utf-8") as f:
        for line in f:
            if y < 40:  # nouvelle page
                c.showPage()
                y = height - 40

            c.drawString(x, y, line.strip())
            y -= line_spacing

    c.save()

# Génération PDF
generate_pdf(report_filename_txt, report_filename_pdf)

print("✅ Rapport PDF généré :", report_filename_pdf)
