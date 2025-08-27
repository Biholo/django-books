# Projet Django — API Bibliothèque et Mini‑blog

## Installation
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

## Lancer le serveur
```bash
python manage.py runserver
```

## Authentification API
- Type: Token
- Header: Authorization: Token <votre_token>

## Endpoints API (DRF)
- Livres
  - GET/POST: /api/livres/
  - GET/PUT/DELETE: /api/livres/<id>/
  - Recherche: /api/livres/?search=<titre>
- Auteurs
  - GET/POST: /api/auteurs/
  - GET/PUT/DELETE: /api/auteurs/<id>/
  - Filtre: /api/auteurs/?year=<année>
  - Action: /api/auteurs/<id>/titres/

## Routes Web (MVT)
- Accueil: /
- Articles (liste): /articles/
- Détail article: /articles/<id>/
- Nouveau: /articles/nouveau/
- Date/heure: /now/

## Administration
- URL: /admin/
- Créez un superuser si besoin: `python manage.py createsuperuser`

## CORS
- Origine autorisée: http://localhost:3000