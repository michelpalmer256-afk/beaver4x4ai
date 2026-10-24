# Parcours Jeep

Trois visuels fournis, conservés à la racine sans modification :

| Scène | Original | Copies d’affichage |
| --- | --- | --- |
| Jeep de face | 77E8C065-1887-4A95-9694-35763E788B56.png | assets/scene-front-1536.webp |
| Rétroviseur | 4A8DB988-3212-41F2-BE11-70F4B18F7E5B.png | assets/scene-mirror-{768,1536}.webp |
| Départ | 89527DE4-8277-421C-85D2-58E67180CCA2.png | assets/scene-departure-{768,1536}.webp |

Le SVG d’introduction utilise un viewport `0 0 1152 1024` sur le montage original
1536 × 1024 : sa bande latérale de références n’est jamais visible. Les lumières
sont des formes SVG animées en opacité, alignées avec les phares de la grande
scène : anneaux, phares principaux, puis cinq projecteurs de toit. Aucune vidéo,
aucune bibliothèque supplémentaire. L’introduction est courte, peut être passée,
s’efface aussi en cas d’image indisponible et disparaît en mode réduction des animations.

Ordre : accueil, fonctionnalités et captures officielles, quatre véhicules,
Explore, rétroviseur, communauté, futures plateformes, départ. Les trois scènes
ne sont pas ajoutées aux cartes des quatre véhicules. Les six cartes Explore
utilisent leurs véritables photographies locales, avec un dégradé de lisibilité.

Sur mobile, le rétroviseur conserve un format panoramique. La clôture cadre
l’aventurier et la Jeep ensemble au-dessus de l’annonce App Store, pour éviter
leur découpe dans une image de fond trop haute. Aucun lien App Store n’est créé.
Pour ajouter le bouton, utiliser uniquement la future URL officielle vérifiée.

Contrôles :

```sh
node --check quality.js
python3 tests/browser_check.py
python3 tests/intro_check.py
```

Serveur local : `python3 -m http.server 8000 --bind 127.0.0.1` dans le checkout
existant. Les tests utilisent Playwright Python et Chromium. Safari iPhone réel
reste à contrôler sur appareil. La photo distante Club préexistante est conservée.
