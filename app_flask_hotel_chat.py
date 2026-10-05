from flask import Flask, render_template_string, request, session, redirect, url_for

from app_gradio_hotel_chat import (
    recommend_hotels_train,
    parse_message_for_constraints,
    as_paragraph,
    cities_set,
)

app = Flask(__name__)
app.secret_key = "change-me-in-production"

PAGE_TEMPLATE = """<!doctype html>
<html lang=\"fr\">
<head>
  <meta charset=\"utf-8\" />
  <title>ExploreSmart · Recommandations IA pour hôtels au Maroc</title>
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
  <link href=\"https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Inter:wght@400;500;600&display=swap\" rel=\"stylesheet\">
  <style>
    :root {
      --bg: #020617;
      --bg-alt: #020b18;
      --primary: #0ea5e9;
      --primary-soft: #0f172a;
      --accent: #22c55e;
      --card: #020b13;
      --card-soft: #020617;
      --border: #1f2937;
      --text-main: #f9fafb;
      --text-muted: #9ca3af;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      background: radial-gradient(circle at top, #020617 0, #020617 40%, #000000 100%);
      color: var(--text-main);
    }

    a {
      color: inherit;
      text-decoration: none;
    }

    .page {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    .nav {
      position: sticky;
      top: 0;
      z-index: 40;
      background: linear-gradient(to bottom, rgba(2,6,23,0.98), rgba(2,6,23,0.9));
      border-bottom: 1px solid rgba(15,23,42,0.9);
      backdrop-filter: blur(18px);
    }

    .nav-inner {
      max-width: 1120px;
      margin: 0 auto;
      padding: 10px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .brand {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      font-family: "Poppins", system-ui, sans-serif;
    }

    .brand-icon {
      width: 32px;
      height: 32px;
      border-radius: 999px;
      background: radial-gradient(circle at 30% 0, #38bdf8, #0f172a);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      color: #e0f2fe;
      font-size: 17px;
    }

    .brand-name {
      font-weight: 700;
      font-size: 18px;
      letter-spacing: .02em;
    }

    .nav-links {
      display: flex;
      align-items: center;
      gap: 14px;
      font-size: 14px;
    }

    .nav-link {
      color: var(--text-muted);
    }

    .nav-link:hover {
      color: var(--text-main);
    }

    .nav-cta {
      padding: 7px 16px;
      border-radius: 999px;
      background: linear-gradient(135deg, #0ea5e9, #38bdf8);
      color: #0b1120;
      font-weight: 600;
      box-shadow: 0 10px 30px rgba(56,189,248,0.35);
      font-size: 13px;
    }

    .nav-cta:hover {
      transform: translateY(-1px);
    }

    .main {
      flex: 1;
    }

    .hero {
      padding: 40px 20px 32px;
      max-width: 1120px;
      margin: 0 auto;
      position: relative;
    }

    .hero-inner {
      text-align: center;
      padding: 56px 16px 48px;
      position: relative;
    }

    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 999px;
      background: rgba(56,189,248,0.12);
      border: 1px solid rgba(56,189,248,0.45);
      font-size: 12px;
      color: #e0f2fe;
      margin-bottom: 14px;
    }

    .hero-title {
      font-family: "Poppins", system-ui, sans-serif;
      font-size: 34px;
      font-weight: 800;
      margin: 0 0 10px;
    }

    .hero-title span {
      background: linear-gradient(135deg, #38bdf8, #22c55e);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .hero-subtitle {
      max-width: 640px;
      margin: 0 auto 20px;
      font-size: 14px;
      color: var(--text-muted);
    }

    .hero-actions {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 12px;
      margin-top: 12px;
    }

    .btn-primary {
      padding: 10px 22px;
      border-radius: 999px;
      border: none;
      font-size: 14px;
      font-weight: 600;
      background: linear-gradient(135deg, #0ea5e9, #38bdf8);
      color: #0b1120;
      box-shadow: 0 14px 38px rgba(56,189,248,0.45);
      cursor: pointer;
    }

    .btn-secondary {
      padding: 10px 22px;
      border-radius: 999px;
      border: 1px solid rgba(148,163,184,0.8);
      font-size: 14px;
      font-weight: 600;
      background: transparent;
      color: var(--text-main);
      cursor: pointer;
    }

    .hero-stats {
      display: flex;
      justify-content: center;
      gap: 40px;
      margin-top: 28px;
      font-family: "Poppins", system-ui, sans-serif;
    }

    .hero-stat-value {
      font-size: 24px;
      font-weight: 700;
      background: linear-gradient(135deg, #38bdf8, #22c55e);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .hero-stat-label {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 4px;
    }

    .features {
      max-width: 1120px;
      margin: 0 auto;
      padding: 16px 20px 32px;
    }

    .features-header {
      text-align: center;
      margin-bottom: 24px;
    }

    .features-header h2 {
      font-family: "Poppins", system-ui, sans-serif;
      font-size: 26px;
      font-weight: 700;
      margin: 0 0 6px;
    }

    .features-header span {
      background: linear-gradient(135deg, #38bdf8, #22c55e);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .features-header p {
      margin: 0;
      font-size: 14px;
      color: var(--text-muted);
    }

    .features-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 18px;
      margin-top: 16px;
    }

    .feature-card {
      background: linear-gradient(145deg, #020617, #020b18);
      border-radius: 18px;
      border: 1px solid rgba(31,41,55,0.9);
      padding: 18px 16px 16px;
      box-shadow: 0 18px 40px rgba(15,23,42,1);
    }

    .feature-icon {
      width: 40px;
      height: 40px;
      border-radius: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 10px;
      font-size: 20px;
    }

    .feature-title {
      font-family: "Poppins", system-ui, sans-serif;
      font-size: 15px;
      font-weight: 600;
      margin-bottom: 6px;
    }

    .feature-text {
      font-size: 13px;
      color: var(--text-muted);
    }

    .search-section {
      max-width: 1120px;
      margin: 0 auto;
      padding: 16px 20px 40px;
    }

    .search-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.7fr) minmax(0, 2fr);
      gap: 20px;
    }

    .search-card {
      background: linear-gradient(145deg, #020617, #020b18);
      border-radius: 18px;
      border: 1px solid rgba(31,41,55,0.9);
      padding: 18px 18px 16px;
      box-shadow: 0 18px 40px rgba(15,23,42,1);
    }

    .search-card h3 {
      font-family: "Poppins", system-ui, sans-serif;
      font-size: 18px;
      margin: 0 0 6px;
    }

    .search-card p {
      margin: 0 0 12px;
      font-size: 13px;
      color: var(--text-muted);
    }

    .field-label {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: .12em;
      color: var(--text-muted);
      margin-bottom: 6px;
    }

    textarea {
      width: 100%;
      min-height: 110px;
      resize: vertical;
      border-radius: 14px;
      border: 1px solid rgba(55,65,81,1);
      background: #000000;
      color: #e5e7eb;
      padding: 10px 12px;
      font-size: 14px;
      outline: none;
    }

    textarea:focus {
      border-color: #38bdf8;
      box-shadow: 0 0 0 1px rgba(56,189,248,0.6);
    }

    .hint {
      font-size: 11px;
      color: var(--text-muted);
    }

    .actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 10px;
      gap: 10px;
    }

    .results-title {
      font-family: "Poppins", system-ui, sans-serif;
      font-size: 16px;
      margin: 0 0 8px;
    }

    .results-wrapper {
      margin-top: 6px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      max-height: 260px;
      overflow-y: auto;
    }

    .hotel-card {
      border-radius: 14px;
      padding: 10px 11px;
      background: #020617;
      border: 1px solid rgba(55,65,81,1);
      font-size: 13px;
    }

    .hotel-header {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-bottom: 2px;
    }

    .hotel-name {
      font-weight: 600;
      font-size: 13px;
      color: #e5e7eb;
    }

    .hotel-meta {
      font-size: 11px;
      color: var(--text-muted);
    }

    .hotel-desc {
      font-size: 12px;
      color: #d1d5db;
      margin-top: 2px;
    }

    .hotel-link {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      margin-top: 4px;
      font-size: 12px;
      color: #38bdf8;
      text-decoration: none;
    }

    .hotel-link:hover {
      text-decoration: underline;
    }

    .no-results {
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 4px;
    }

    @media (max-width: 900px) {
      .hero-inner {
        padding-top: 40px;
      }

      .hero-title {
        font-size: 26px;
      }

      .hero-stats {
        flex-direction: column;
        gap: 12px;
      }

      .search-grid {
        grid-template-columns: minmax(0, 1fr);
      }
    }
  </style>
</head>
<body>
  <div class=\"page\">
    <header class=\"nav\">
      <div class=\"nav-inner\">
        <a href=\"/search\" class=\"brand\">
          <div class=\"brand-icon\">E</div>
          <span class=\"brand-name\">ExploreSmart</span>
        </a>
        <div class=\"nav-links\">
          <a href=\"/search\" class=\"nav-link\">Accueil</a>
          <a href=\"/\" class=\"nav-cta\">Tester le chatbot</a>
        </div>
      </div>
    </header>

    <main class=\"main\">
      <section class=\"hero\">
        <div class=\"hero-inner\">
          <div class=\"hero-badge\">Recommandations IA pour touristes</div>
          <h1 class=\"hero-title\">Découvrez les <span>merveilles</span> du Maroc</h1>
          <p class=\"hero-subtitle\">Notre assistant intelligent vous guide vers les hôtels et séjours parfaits selon vos envies.
            Plages, déserts, médinas ou montagnes — trouvez votre prochaine aventure.
          </p>
          <div class=\"hero-actions\">
            <a href=\"#search\" class=\"btn-primary\">Explorer maintenant</a>
            <a href=\"#features\" class=\"btn-secondary\">En savoir plus</a>
          </div>

          <div class=\"hero-stats\">
            <div>
              <div class=\"hero-stat-value\">10+</div>
              <div class=\"hero-stat-label\">Destinations</div>
            </div>
            <div>
              <div class=\"hero-stat-value\">24/7</div>
              <div class=\"hero-stat-label\">Disponible</div>
            </div>
            <div>
              <div class=\"hero-stat-value\">100%\</div>
              <div class=\"hero-stat-label\">Gratuit</div>
            </div>
          </div>
        </div>
      </section>

      <section id=\"features\" class=\"features\">
        <div class=\"features-header\">
          <h2>Pourquoi choisir <span>ExploreSmart</span> ?</h2>
          <p>Une technologie de pointe au service de votre exploration</p>
        </div>
        <div class=\"features-grid\">
          <div class=\"feature-card\">
            <div class=\"feature-icon\" style=\"background: rgba(56,189,248,0.1); color: #38bdf8;\">🤖</div>
            <div class=\"feature-title\">Assistant IA Intelligent</div>
            <div class=\"feature-text\">Discutez naturellement avec notre chatbot qui comprend vos préférences et besoins de voyage.</div>
          </div>
          <div class=\"feature-card\">
            <div class=\"feature-icon\" style=\"background: rgba(56,189,248,0.1); color: #22c55e;\">📍</div>
            <div class=\"feature-title\">Recommandations Personnalisées</div>
            <div class=\"feature-text\">Obtenez des suggestions d'hôtels adaptées à vos envies : plage, culture, aventure ou détente.</div>
          </div>
          <div class=\"feature-card\">
            <div class=\"feature-icon\" style=\"background: rgba(249,115,22,0.15); color: #fb923c;\">⚡</div>
            <div class=\"feature-title\">Réponses Instantanées</div>
            <div class=\"feature-text\">Notre système analyse votre demande en temps réel pour des recommandations immédiates.</div>
          </div>
          <div class=\"feature-card\">
            <div class=\"feature-icon\" style=\"background: rgba(248,113,113,0.15); color: #f97373;\">❤️</div>
            <div class=\"feature-title\">Expériences Uniques</div>
            <div class=\"feature-text\">Découvrez des séjours hors des sentiers battus sélectionnés par notre IA.</div>
          </div>
          <div class=\"feature-card\">
            <div class=\"feature-icon\" style=\"background: rgba(59,130,246,0.15); color: #60a5fa;\">🌍</div>
            <div class=\"feature-title\">Couverture Complète</div>
            <div class=\"feature-text\">Des plages d'Agadir aux dunes de Merzouga, explorez tout le Maroc.</div>
          </div>
          <div class=\"feature-card\">
            <div class=\"feature-icon\" style=\"background: rgba(34,197,94,0.15); color: #4ade80;\">🛡️</div>
            <div class=\"feature-title\">Informations Fiables</div>
            <div class=\"feature-text\">Données vérifiées avec coordonnées GPS et liens Google Maps directs.</div>
          </div>
        </div>
      </section>

      <section id=\"search\" class=\"search-section\">
        <div class=\"search-grid\">
          <div class=\"search-card\">
            <h3>Tester l'assistant hôtels</h3>
            <p>Décrivez le type de séjour que vous cherchez (ville, budget, type d'hôtel, activités...). \
L'assistant infère automatiquement ville, budget maximum et note minimale.</p>
            <form method=\"post\">\n              <div>\n                <div class=\"field-label\">Votre message</div>\n                <textarea name=\"message\" placeholder=\"Ex. : hôtel familial à Agadir, piscine, près de la plage, budget 800 DH, note au moins 4/5...\">{{ user_message }}</textarea>\n              </div>\n              <div class=\"actions\">\n                <div class=\"hint\">Conseil : précisez une ville marocaine, un budget maximum (en DH) et une note minimale.</div>\n                <button class=\"btn-primary\" type=\"submit\">Lancer la recherche</button>\n              </div>\n            </form>
          </div>

          <div class=\"search-card\">
            <h3 class=\"results-title\">Recommandations</h3>
            <div class=\"results-wrapper\">\n              {% if results_html %}\n                <div class=\"results\">{{ results_html|safe }}</div>\n              {% elif user_message %}\n                <p class=\"no-results\">Aucun résultat pour cette requête. Essayez d'élargir la recherche ou de simplifier la description.</p>\n              {% else %}\n                <p class=\"no-results\">Les recommandations s'afficheront ici après votre première requête.</p>\n              {% endif %}\n            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</body>
</html>"""


@app.route("/search", methods=["GET", "POST"])
def search():
    user_message = ""
    results_html = ""

    if request.method == "POST":
        user_message = (request.form.get("message") or "").strip()
        if user_message:
            cons = parse_message_for_constraints(user_message, cities_set)
            res = recommend_hotels_train(
                query_text=user_message,
                top_k=6,
                city=cons.get("city"),
                price_target=cons.get("price_target"),
                min_rating=cons.get("min_rating"),
            )

            if res is not None and len(res) > 0:
                cards = []
                for _, r in res.iterrows():
                    name = r.get("Hotel", "(Hôtel)") or "(Hôtel)"
                    city = r.get("Ville", "") or ""
                    typ = r.get("Type", "") or ""
                    rating = r.get("Rating", "") or ""
                    price = r.get("Prix_nuit", "") or ""
                    desc = r.get("Description", "") or ""
                    services = r.get("Services", "") or ""
                    url = r.get("GoogleMap_URL") or ""

                    para = as_paragraph(r)

                    header_meta = []
                    if city:
                        header_meta.append(city)
                    if typ:
                        header_meta.append(typ)
                    meta_str = " · ".join(header_meta)

                    rating_price = []
                    if rating != "":
                        rating_price.append(f"⭐ {rating}/5")
                    if price != "":
                        rating_price.append(f"💰 {price} DH / nuit")
                    rp_str = " · ".join(rating_price)

                    html = ["<div class='hotel-card'>"]
                    html.append("  <div class='hotel-header'>")
                    html.append(f"    <div class='hotel-name'>{name}</div>")
                    if rp_str:
                        html.append(f"    <div class='hotel-meta'>{rp_str}</div>")
                    html.append("  </div>")

                    if meta_str:
                        html.append(f"  <div class='hotel-meta'>{meta_str}</div>")

                    if desc:
                        html.append(f"  <div class='hotel-desc'>{desc}</div>")
                    elif para:
                        html.append(f"  <div class='hotel-desc'>{para}</div>")

                    if services:
                        html.append(f"  <div class='hotel-meta'>Services : {services}</div>")

                    if url:
                        html.append(f"  <a class='hotel-link' href='{url}' target='_blank'>Voir sur Google Maps</a>")

                    html.append("</div>")
                    cards.append("\n".join(html))

                results_html = "\n".join(cards)

    return render_template_string(PAGE_TEMPLATE, user_message=user_message, results_html=results_html)


# =====================
# Interface type ChatGPT (route principale "/")
# =====================
CHAT_TEMPLATE = """<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <title>Chatbot Recommandations · ExploreSmart</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #020617;
      --bg-soft: #020b18;
      --primary: #0ea5e9;
      --primary-strong: #38bdf8;
      --accent: #22c55e;
      --card: #020b13;
      --border: #1f2937;
      --text-main: #f9fafb;
      --text-muted: #9ca3af;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      background: radial-gradient(circle at top, #020617 0, #020617 40%, #000000 100%);
      color: var(--text-main);
    }

    a {
      color: inherit;
      text-decoration: none;
    }

    .page {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    .nav {
      position: sticky;
      top: 0;
      z-index: 40;
      background: linear-gradient(to bottom, rgba(2,6,23,0.98), rgba(2,6,23,0.9));
      border-bottom: 1px solid rgba(15,23,42,0.9);
      backdrop-filter: blur(18px);
    }

    .nav-inner {
      max-width: 1120px;
      margin: 0 auto;
      padding: 10px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .brand {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      font-family: "Poppins", system-ui, sans-serif;
    }

    .brand-icon {
      width: 32px;
      height: 32px;
      border-radius: 999px;
      background: radial-gradient(circle at 30% 0, #38bdf8, #0f172a);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      color: #e0f2fe;
      font-size: 17px;
    }

    .brand-name {
      font-weight: 700;
      font-size: 18px;
      letter-spacing: .02em;
    }

    .nav-links {
      display: flex;
      align-items: center;
      gap: 14px;
      font-size: 14px;
    }

    .nav-link {
      color: var(--text-muted);
    }

    .nav-link:hover {
      color: var(--text-main);
    }

    .nav-cta {
      padding: 7px 16px;
      border-radius: 999px;
      background: linear-gradient(135deg, #0ea5e9, #38bdf8);
      color: #0b1120;
      font-weight: 600;
      box-shadow: 0 10px 30px rgba(56,189,248,0.35);
      font-size: 13px;
    }

    .nav-cta:hover {
      transform: translateY(-1px);
    }

    .main {
      flex: 1;
    }

    .chat-section {
      max-width: 1120px;
      margin: 0 auto;
      padding: 32px 20px 28px;
    }

    .chat-title {
      text-align: center;
      margin-bottom: 18px;
    }

    .chat-title h1 {
      font-family: "Poppins", system-ui, sans-serif;
      font-size: 26px;
      font-weight: 700;
      margin: 0 0 6px;
    }

    .chat-title span {
      background: linear-gradient(135deg, #38bdf8, #22c55e);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .chat-title p {
      margin: 0;
      font-size: 14px;
      color: var(--text-muted);
    }

    .chat-shell {
      margin-top: 20px;
      border-radius: 20px;
      border: 1px solid rgba(31,41,55,0.95);
      background: radial-gradient(circle at top left, rgba(56,189,248,0.16), rgba(15,23,42,0.98));
      box-shadow: 0 24px 60px rgba(15,23,42,1);
      display: flex;
      flex-direction: column;
      min-height: 520px;
      max-height: calc(100vh - 200px);
    }

    .chat-header {
      padding: 14px 18px;
      border-bottom: 1px solid rgba(31,41,55,0.9);
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .chat-header-icon {
      width: 40px;
      height: 40px;
      border-radius: 14px;
      background: radial-gradient(circle at 30% 0, #22c55e, #064e3b);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
    }

    .chat-header-title {
      font-family: "Poppins", system-ui, sans-serif;
      font-size: 15px;
      font-weight: 600;
    }

    .chat-header-status {
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 2px;
    }

    .chat-header-status span {
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }

    .status-dot {
      width: 7px;
      height: 7px;
      border-radius: 999px;
      background: #22c55e;
      box-shadow: 0 0 0 4px rgba(34,197,94,0.25);
    }

    .chat-body {
      flex: 1;
      padding: 14px 18px 10px;
      overflow-y: auto;
    }

    .msg-row {
      display: flex;
      gap: 10px;
      margin-bottom: 10px;
    }

    .msg-row.user {
      justify-content: flex-end;
    }

    .msg-row.assistant {
      justify-content: flex-start;
    }

    .avatar {
      width: 30px;
      height: 30px;
      border-radius: 999px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 13px;
      font-weight: 600;
      flex-shrink: 0;
    }

    .avatar.user {
      background: #0ea5e9;
      color: #f9fafb;
      box-shadow: 0 8px 24px rgba(14,165,233,0.6);
    }

    .avatar.assistant {
      background: #020617;
      color: #e5e7eb;
      border: 1px solid rgba(55,65,81,0.9);
    }

    .bubble {
      max-width: 76%;
      padding: 9px 11px 8px;
      border-radius: 14px;
      font-size: 13px;
      line-height: 1.45;
      white-space: pre-wrap;
      border: 1px solid transparent;
    }

    .bubble.user {
      background: linear-gradient(135deg, #0ea5e9, #38bdf8);
      color: #eff6ff;
      border-color: rgba(56,189,248,0.9);
    }

    .bubble.assistant {
      background: #020617;
      color: #e5e7eb;
      border-color: rgba(31,41,55,0.9);
    }

    .bubble.assistant a {
      color: #38bdf8;
      text-decoration: none;
    }

    .bubble.assistant a:hover {
      text-decoration: underline;
    }

    .welcome {
      font-size: 13px;
      color: var(--text-muted);
    }

    .chat-suggestions {
      padding: 6px 18px 10px;
      border-top: 1px solid rgba(31,41,55,0.9);
    }

    .suggestions-label {
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 6px;
    }

    .chips {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .chip-form {
      display: inline-block;
    }

    .chip {
      padding: 6px 12px;
      border-radius: 999px;
      border: 1px solid rgba(55,65,81,1);
      background: #020617;
      color: var(--text-muted);
      font-size: 12px;
      cursor: pointer;
    }

    .chip:hover {
      border-color: #38bdf8;
      color: #e5e7eb;
    }

    .chat-input {
      padding: 10px 14px 12px;
      border-top: 1px solid rgba(31,41,55,0.9);
      background: linear-gradient(to top, #020617, #020b18);
      display: flex;
      gap: 10px;
      align-items: flex-end;
    }

    .chat-input textarea {
      flex: 1;
      resize: none;
      max-height: 90px;
      border-radius: 12px;
      border: 1px solid rgba(55,65,81,1);
      background: #000000;
      color: #e5e7eb;
      padding: 8px 10px;
      font-size: 13px;
      outline: none;
    }

    .chat-input textarea:focus {
      border-color: #38bdf8;
      box-shadow: 0 0 0 1px rgba(56,189,248,0.6);
    }

    .chat-input button {
      border: none;
      border-radius: 999px;
      padding: 8px 16px;
      font-size: 13px;
      font-weight: 600;
      color: #0b1120;
      cursor: pointer;
      background: linear-gradient(135deg, #0ea5e9, #38bdf8);
      box-shadow: 0 10px 30px rgba(56,189,248,0.45);
      flex-shrink: 0;
    }

    .chat-input button:hover {
      transform: translateY(-1px);
    }

    .hint-bottom {
      text-align: center;
      font-size: 11px;
      color: #6b7280;
      padding-bottom: 14px;
    }

    @media (max-width: 768px) {
      .chat-shell {
        max-height: none;
        min-height: 480px;
      }

      .bubble {
        max-width: 84%;
      }
    }
  </style>
</head>
<body>
  <div class="page">
    <header class="nav">
      <div class="nav-inner">
        <a href="/search" class="brand">
          <div class="brand-icon">E</div>
          <span class="brand-name">ExploreSmart</span>
        </a>
        <div class="nav-links">
          <a href="/search" class="nav-link">Accueil</a>
          <a href="#" class="nav-cta">Chatbot</a>
        </div>
      </div>
    </header>

    <main class="main">
      <section class="chat-section">
        <div class="chat-title">
          <h1>Chatbot <span>Recommandations</span></h1>
          <p>Décrivez vos envies et recevez des recommandations d'hôtels personnalisées au Maroc.</p>
        </div>

        <div class="chat-shell">
          <div class="chat-header">
            <div class="chat-header-icon">🏝️</div>
            <div>
              <div class="chat-header-title">Assistant ExploreSmart</div>
              <div class="chat-header-status">
                <span><span class="status-dot"></span> En ligne · Prêt à vous aider</span>
              </div>
            </div>
          </div>

          <div class="chat-body">
            {% if history %}
              {% for msg in history %}
                <div class="msg-row {{ msg.role }}">
                  {% if msg.role == 'assistant' %}
                    <div class="avatar assistant">AI</div>
                  {% endif %}
                  <div class="bubble {{ msg.role }}">
                    {% if msg.is_html %}
                      {{ msg.content|safe }}
                    {% else %}
                      {{ msg.content }}
                    {% endif %}
                  </div>
                  {% if msg.role == 'user' %}
                    <div class="avatar user">U</div>
                  {% endif %}
                </div>
              {% endfor %}
            {% else %}
              <div class="welcome">
                Bonjour ! 👋 Je suis votre assistant ExploreSmart. Dites-moi ce que vous recherchez : plages, désert,
                montagnes, culture, aventure... Je vous recommanderai les meilleurs hôtels et séjours au Maroc.
              </div>
            {% endif %}
          </div>

          {% if history|length <= 2 %}
          <div class="chat-suggestions">
            <div class="suggestions-label">Suggestions rapides</div>
            <div class="chips">
              {% set quick_suggestions = ["Plages à Agadir", "Désert et dunes", "Sites historiques", "Villes bleues", "Nature et cascades"] %}
              {% for label in quick_suggestions %}
                <form method="post" class="chip-form">
                  <input type="hidden" name="message" value="{{ label }}" />
                  <button type="submit" class="chip">{{ label }}</button>
                </form>
              {% endfor %}
            </div>
          </div>
          {% endif %}

          <form method="post" class="chat-input">
            <textarea
              name="message"
              rows="2"
              placeholder="Par ex. : hôtel familial en bord de mer à Agadir avec piscine, moins de 800 DH, note au moins 4/5..."
            ></textarea>
            <button type="submit">Envoyer</button>
          </form>
        </div>
      </section>

      <div class="hint-bottom">
        Les recommandations sont basées sur un corpus d'environ 30 000 hôtels au Maroc (données synthétiques).
      </div>
    </main>
  </div>
</body>
</html>"""


@app.route("/", methods=["GET", "POST"])
def chat():
    # Historique simple stocké en session (liste de dicts {role, content})
    history = session.get("history", [])

    if request.method == "POST":
        user_message = (request.form.get("message") or "").strip()
        if user_message:
            history.append({"role": "user", "content": user_message, "is_html": False})

            # Contraintes (ville, budget max, note minimale) extraites du texte
            cons = parse_message_for_constraints(user_message, cities_set)
            res = recommend_hotels_train(
                query_text=user_message,
                top_k=6,
                city=cons.get("city"),
                price_target=cons.get("price_target"),
                min_rating=cons.get("min_rating"),
            )

            if res is not None and len(res) > 0:
                parts = []
                parts.append("<p><strong>Voici des recommandations basées sur votre requête :</strong></p>")
                for _, r in res.iterrows():
                    url = r.get("GoogleMap_URL") or ""
                    para = as_paragraph(r)
                    snippet = ["<div class='hotel-snippet'>"]
                    snippet.append(para)
                    if url:
                        snippet.append(f"<br><a href='{url}' target='_blank'>Voir sur Google Maps</a>")
                    snippet.append("</div>")
                    parts.append("".join(snippet))
                assistant_text = "\n".join(parts)
                history.append({"role": "assistant", "content": assistant_text, "is_html": True})
            else:
                assistant_text = (
                    "Je n'ai trouvé aucun hôtel correspondant exactement à cette requête. "
                    "Essayez éventuellement de préciser une ville marocaine, un budget maximum (en DH) "
                    "et une note minimale (par ex. 'au moins 4/5')."
                )
                history.append({"role": "assistant", "content": assistant_text, "is_html": False})
            session["history"] = history

        return redirect(url_for("chat"))

    return render_template_string(CHAT_TEMPLATE, history=history)


if __name__ == "__main__":
    # Par défaut, écoute uniquement en local
    app.run(host="127.0.0.1", port=5000, debug=False)
