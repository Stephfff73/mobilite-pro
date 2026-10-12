# Mobilité Pro 🧭

Prototype Streamlit de comparaison porte-à-porte des déplacements professionnels.

## Inclus dans ce MVP
- Adresse de départ préremplie : 57 Impasse de la Ville, 38300 Châteauvilain.
- Paramètres modifiables pour Renault Talisman diesel : 6 L/100 km et 1,75 €/L.
- Itinéraire routier indicatif via géocodage OpenStreetMap/Nominatim et moteur OSRM.
- Calcul du carburant, péages et stationnement saisis.
- Champs de saisie pour les tarifs/durées réels du train et de l'avion.
- Marge de sécurité avant rendez-vous.
- Estimation carbone voiture provisoire, sans présenter de facteurs manquants comme connus.
- Liens de recherche d'hébergement.

## Limites à connaître
Cette version n'est pas encore un moteur de réservation ni un comparateur entièrement connecté.
- OSRM public ne fournit pas de trafic temps réel et n'offre aucune garantie de disponibilité.
- Le prix SNCF avec carte Liberté, les horaires et perturbations doivent être branchés à des données officielles ou à un fournisseur autorisé.
- Les tarifs d'avion, les frais de bagages et les parkings doivent être confirmés auprès de sources à jour.
- Les prix et disponibilités d'hôtels/location ne sont pas extraits automatiquement.
- Le facteur carbone voiture fourni est une estimation d'émissions directes à l'échappement ; il ne représente pas une analyse complète du cycle de vie. Pour des comparaisons publiables, documenter des facteurs comparables issus de l'ADEME/Base Empreinte et le périmètre de calcul.
- Les API publiques peuvent imposer des limites d'usage. En production, respecter leurs conditions, mettre en cache et afficher l'heure de mise à jour.

## Lancer en local
Python 3.11 ou 3.12 recommandé.

```bash
python -m venv .venv
# Windows :
.venv\\Scripts\\activate
# macOS/Linux :
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Puis ouvrir l'adresse locale indiquée dans le terminal.

## Tests
```bash
pytest -q
```

## Créer le dépôt GitHub
1. Sur GitHub, créer un nouveau dépôt nommé `mobilite-pro`.
2. Pour une première version, choisir un dépôt privé si vous préférez ne pas rendre publique l'adresse de départ et les usages professionnels.
3. Décompresser le ZIP, ouvrir un terminal dans le dossier et exécuter :

```bash
git init
git add .
git commit -m "Initial commit - Mobilité Pro"
git branch -M main
git remote add origin https://github.com/VOTRE_COMPTE/mobilite-pro.git
git push -u origin main
```

Remplacer `VOTRE_COMPTE` par votre identifiant GitHub.

## Déployer avec Streamlit Community Cloud
1. Ouvrir https://share.streamlit.io/ et se connecter avec GitHub.
2. Cliquer sur **Create app**.
3. Sélectionner le dépôt `mobilite-pro`, la branche `main` et le fichier `app.py`.
4. Choisir une version Python prise en charge, puis déployer.
5. Pour chaque clé API ajoutée plus tard, la saisir dans **App settings → Secrets**, jamais dans le code ni dans Git.
6. Vérifier l'application et consulter les logs en cas d'erreur.

## Architecture prévue pour la suite
- `services/rail.py` : horaires SNCF, perturbations et tarifs via fournisseurs autorisés.
- `services/flights.py` : recherche de vols et prix.
- `services/parking.py` : tarifs de stationnement.
- `services/lodging.py` : hôtels et locations.
- `services/carbon.py` : facteurs sourcés et périmètres homogènes.
- `core/recommendation.py` : score pondéré coût/temps/fiabilité ajustable.
- Base de données : historique et déplacements récurrents.

## Confidentialité
L'adresse de départ est préremplie dans le code de cette première version. Avant de partager le dépôt ou l'application, remplacez-la par une configuration privée ou un paramètre local. Un dépôt public rend le code visible. Ne stockez aucune clé API ou donnée confidentielle dans Git.
