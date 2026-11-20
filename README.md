# TaskLab TWIN2 — Projet fil rouge
Projet pédagogique Django pour les chapitres VIII à XII du Génie Logiciel.

## Installation
```bash
python -m venv .venv
# Windows PowerShell : .venv\Scripts\Activate.ps1
# Linux/macOS : source .venv/bin/activate
pip install -r requirements.txt
# Windows : copy .env.example .env  |  Linux/macOS : cp .env.example .env
python manage.py makemigrations taches
python manage.py migrate
python manage.py runserver
```
Accès : http://127.0.0.1:8000/ ; admin : /admin/ (créer un superuser si besoin).

## Configuration

La configuration est lue à partir de variables d'environnement, stockées dans un fichier `.env` à la racine du projet. Ce fichier n'est pas versionné : il contient des valeurs propres à chaque machine et des secrets.

1. Copier le modèle :
   - Windows : `copy .env.example .env`
   - Linux/macOS : `cp .env.example .env`
2. Modifier les valeurs dans `.env` si nécessaire.

| Variable | Rôle | Valeur par défaut (dev) |
|---|---|---|
| `DEBUG` | Active le mode debug de Django (pages d'erreur détaillées). À mettre sur `False` en production. | `True` |
| `SECRET_KEY` | Clé secrète de Django, utilisée pour signer les sessions et les jetons. Doit être longue, aléatoire et gardée secrète. | `replace-me-with-a-long-random-secret` |
| `ALLOWED_HOSTS` | Liste des noms d'hôte autorisés à accéder à l'application, séparés par des virgules. | `127.0.0.1,localhost` |

Pour générer une vraie clé secrète :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Fichiers non versionnés

- `.env` : contient des secrets. Sur un dépôt public, ils seraient visibles de tous. On versionne seulement `.env.example`, qui liste les variables sans leurs vraies valeurs.
- `.venv` : environnement virtuel, lourd et propre à chaque machine. Il se recrée avec `pip install -r requirements.txt`.
- `db.sqlite3` : base de données locale avec des données propres à chaque développeur. Elle se recrée avec `python manage.py migrate`.

## Tests
`python manage.py test`

## Travail à réaliser
Voir le document TP associé. Ce starter est volontairement incomplet :
pas de filtre de statut, peu de tests, pas de version de livraison.
Ne jamais publier une clé SECRET_KEY de production ; DEBUG=False en production.