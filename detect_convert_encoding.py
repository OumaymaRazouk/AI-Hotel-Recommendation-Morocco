#!/usr/bin/env python3
"""
Détecte l'encodage probable d'un fichier CSV, vérifie le séparateur,
et crée des copies converties en UTF-8 (sans BOM) et UTF-8 avec BOM.

Usage:
    python detect_convert_encoding.py [input_csv]
"""

import sys
import os
import csv

CANDIDATE_ENCODINGS = [
    'utf-8',        # UTF-8 sans BOM
    'utf-8-sig',    # UTF-8 avec BOM
    'cp1252',       # Windows-1252
    'iso-8859-1',   # Latin-1
]


def try_decode(raw: bytes, encoding: str) -> str | None:
    try:
        # strict pour être certain que l'encodage est valide
        return raw.decode(encoding, errors='strict')
    except Exception:
        return None


def sniff_delimiter(text: str) -> str:
    try:
        sample = '\n'.join(text.splitlines()[:50])
        dialect = csv.Sniffer().sniff(sample, delimiters=[',',';','\t','|'])
        return dialect.delimiter
    except Exception:
        # fallback: compter les séparateurs les plus fréquents sur la première ligne
        first = text.splitlines()[0]
        counts = {sep: first.count(sep) for sep in [';', ',', '\t', '|']}
        return max(counts, key=counts.get)


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else 'hotels_maroc_30000_equilibres.csv'
    if not os.path.isfile(input_path):
        print(f"❌ Fichier introuvable: {input_path}")
        sys.exit(1)

    # Lire en binaire
    raw = open(input_path, 'rb').read()

    detected = None
    decoded_text = None

    # 1) Essayer UTF-8 strict d'abord
    decoded_text = try_decode(raw, 'utf-8')
    if decoded_text is not None:
        detected = 'utf-8'
    else:
        # 2) Essayer d'autres encodages communs
        for enc in ['utf-8-sig', 'cp1252', 'iso-8859-1']:
            decoded_text = try_decode(raw, enc)
            if decoded_text is not None:
                detected = enc
                break

    if detected is None:
        print('❌ Impossible de décoder le fichier avec les encodages courants (utf-8, utf-8-sig, cp1252, iso-8859-1).')
        sys.exit(2)

    # Sniffer le séparateur
    delimiter = sniff_delimiter(decoded_text)

    # Vérifier la présence de '@'
    has_at = '@' in decoded_text
    at_count = decoded_text.count('@')

    print('📄 Analyse du fichier:')
    print(f'- Chemin: {input_path}')
    print(f'- Encodage détecté: {detected}')
    print(f'- Séparateur détecté: {repr(delimiter)}')
    print(f"- Présence de '@': {'oui' if has_at else 'non'} (count={at_count})")

    # 3) Écrire la version convertie unique (UTF-8 sans BOM)
    base, ext = os.path.splitext(input_path)
    out_utf8 = f"{base}_utf8{ext}"

    # UTF-8 sans BOM — fichier principal pour Python et autres outils
    with open(out_utf8, 'w', encoding='utf-8', newline='') as f:
        f.write(decoded_text)

    print('✅ Fichier généré:')
    print(f'- {out_utf8} (UTF-8)')
    print('\nConseils:')
    print("- Dans VS Code: cliquez sur l'indicateur d'encodage en bas à droite > Reopen with Encoding > UTF-8")
    print("- Dans Excel: si l'encodage n'est pas détecté automatiquement, choisissez UTF-8 lors de l'import")


if __name__ == '__main__':
    main()
