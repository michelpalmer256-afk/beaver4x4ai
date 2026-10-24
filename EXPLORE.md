# EXPLORE — intégration et contrôle avant publication

La section `#explore` ajoute six panoramas responsives sans bibliothèque supplémentaire.
Les photographies sont chargées à la demande, en 720, 1440 ou 1920 pixels, avec
compression et format négociés par le CDN Unsplash. L'animation utilise des
transformations limitées à 18 pixels ; elle est désactivée par le réglage de
réduction des animations. Sans JavaScript, le contenu reste visible.

## Photographies locales

Les six scènes utilisent des copies WebP locales en trois tailles. Les sources,
la référence de licence et les limites de vérification sont dans `PHOTOS.md`.
Les photos ont été inspectées ; la scène désert montre Monument Valley, la scène
mer une plage et la scène montagne des sommets enneigés. La forêt est une ambiance
de conifères, sans affirmation de localisation canadienne de la prise de vue.

## Vérification locale

Depuis `/workspace/beaver4x4ai` :

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Vérifier les six panoramas, les liens de navigation, le défilement du carrousel,
l'absence de débordement et le mode réduction des animations. Les tests Chromium
couvrent 320, 375, 390, 430, 768, 1440 pixels et le format paysage 844 × 390.
Un contrôle Safari sur iPhone réel reste nécessaire ; Chromium ne le remplace pas.

Tests de mise en page et de navigation (Playwright Python et Chromium requis) :

```sh
python3 tests/browser_check.py
```

`BASE_URL` et `CHROMIUM_PATH` permettent de choisir le serveur et le navigateur.
Ces tests vérifient les ancres, le nombre de véhicules et de scènes, les flèches,
les révélations au défilement, les erreurs JavaScript et la réduction des animations.
Ils ne valident pas le contenu ou la licence des photos distantes, ni Safari.
