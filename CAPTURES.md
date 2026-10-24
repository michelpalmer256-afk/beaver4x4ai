# Captures de l’application

Le carrousel conserve six emplacements. Quatre captures individuelles disponibles sont intégrées : Garage (`IMG_9807.png`), Trails World (`IMG_9809.png`), Copilote IA (`IMG_9808.png`), Mes véhicules (`IMG_9799.png`). Les originaux sont conservés ; les copies WebP de 660 pixels de large dans `assets/app-*.webp` servent à l’affichage, avec chargement différé.

Club et Profil restent explicitement illustratifs. Pour intégrer leurs captures officielles :

1. Ajouter les fichiers dans `assets/app-club.webp` et `assets/app-profil.webp`, sans recadrer la capture. Privilégier une largeur de 660 pixels et conserver les proportions originales.
2. Dans les deux articles correspondants de `index.html`, remplacer `is-placeholder` par `is-capture`, mettre à jour `src`, `alt`, `width` et `height` de l’image.
3. Retirer les éléments `phone-notch` et `phone-overlay` de ces deux articles, puis remplacer « Capture officielle à venir » par leur description.
4. Actualiser le paragraphe d’introduction du carrousel.

Le rendu utilise `object-fit: contain` et un écran aux dimensions contraintes : aucune déformation ni découpe, même si une future capture possède d’autres proportions.

Validation locale : `python3 -m http.server 8000 --bind 127.0.0.1`, puis vérifier le défilement tactile, les flèches et les six aperçus sur petit écran. La validation automatisée a été effectuée avec Chromium aux largeurs 320, 375, 390, 430, 768 et 1440 pixels ; un contrôle sur Safari iOS réel reste recommandé.
