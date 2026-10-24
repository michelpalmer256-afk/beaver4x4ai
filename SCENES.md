# Parcours Jeep

Trois visuels fournis, conservés à la racine sans modification :

| Scène | Original | Copies d’affichage |
| --- | --- | --- |
| Jeep de face | 77E8C065-1887-4A95-9694-35763E788B56.png | assets/scene-front-1536.webp |
| Rétroviseur | 4A8DB988-3212-41F2-BE11-70F4B18F7E5B.png | assets/scene-mirror-{768,1536}.webp |
| Départ | 89527DE4-8277-421C-85D2-58E67180CCA2.png | assets/scene-departure-{768,1536}.webp |

L’accueil permanent (`#accueil`) utilise un SVG avec un viewport `0 0 1152 1024`
sur le montage original 1536 × 1024 : sa bande latérale de références n’est jamais
visible. La Jeep entière reste fixe. Les lumières sont des formes SVG transparentes fixes, dans trois couches HTML
alignées dans le même repère. Seule l’opacité de ces couches est animée, avec
préparation de la composition pendant la séquence et libération ensuite : anneaux, phares principaux, puis cinq projecteurs.
Les halos radiaux et une réflexion légère sur le capot évitent les disques pleins.
Aucun morceau d’image ni deuxième visuel d’accueil n’est superposé.

Le logo officiel illustré remplace le grand titre textuel : copie WebP RGBA de
512 pixels (`assets/beaver-logo-welcome-transparent.webp`). Le détourage issu du
logo fourni est conservé en PNG dans `assets/beaver-logo-transparent.png` ; seuls
les blancs extérieurs au badge sont transparents, les blancs du dessin restent
visibles. Le petit logo d’en-tête et les sources originales sont conservés.
Le logo apparaît après la fin de l’allumage de la rampe de toit (zoom 90 % à 100 %
et lueur verte statique, sans filtre de flou animé),
puis l’accroche, le slogan et les deux boutons apparaissent à leur tour. Ils restent visibles : aucun écran temporaire, aucune redirection ni
bascule automatique. Sur mobile, le texte commence sous les phares. En réduction
des animations, le résultat final apparaît sans animation. Les appareils aux
capacités limitées conservent la séquence légère en opacité : les estimations
de processeur et de mémoire ne doivent pas désactiver l’allumage sur Safari. Sans JavaScript ou en cas d’échec de chargement, les liens restent
accessibles. Le focus clavier révèle immédiatement les commandes.

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

Optimisation mobile : aucun filtre CSS sur les phares ; photo et logo décodés
avant la séquence. Sur écran tactile, les textes apparaissent en opacité seule.
Le logo conserve son zoom. Les tests simulent aussi un écran tactile à densité ×3 ;
ils ne prouvent pas la fluidité sur Safari iOS réel.
