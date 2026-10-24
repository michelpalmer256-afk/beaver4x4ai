# Paysages immersifs dans les sections existantes

Les six photographies locales remplacent la longue galerie de panoramas par des
arrière-plans intégrés aux sections :

| Section | Paysage |
| --- | --- |
| Univers 4x4 (`#vehicules`) | Désert américain |
| Fonctionnalités (`#fonctionnalites`) | Forêt |
| Captures de l’application (`#application`) | Rivière |
| Explore (`#explore`) | Mer |
| Club (`#club`) | Vallées montagneuses |
| Futures plateformes (`#futures-versions`) | Montagne enneigée |

Voile sombre, images WebP responsives en 720/1440/1920 pixels, chargement différé
et parallaxe limitée à 18 pixels. La réduction des animations désactive cet effet.
Les slogans et avertissements déjà validés restent dans un bloc Explore compact.
Le visuel Club existant et l’animation d’accueil sont conservés.
La provenance des photographies est documentée dans PHOTOS.md.

Depuis `/workspace/beaver4x4ai`, lancer :

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Puis, avec Playwright Python et Chromium :

```sh
node --check quality.js
python3 tests/browser_check.py
```

`BASE_URL` et `CHROMIUM_PATH` permettent de choisir le serveur et le navigateur.
Tests : quatre véhicules, grille mobile à deux colonnes, six nouvelles captures
entières, six arrière-plans, décodage des images locales, ancres, pages légales
et assistance, carrousel, sept formats, réduction des animations et erreurs JS.
Un contrôle sur Safari iPhone réel reste recommandé.
