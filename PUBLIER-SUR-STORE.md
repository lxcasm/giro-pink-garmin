# Publier Giro Pink sur le Connect IQ Store

> Garmin n'a **pas d'API** de publication : tout se fait **à la main** sur le portail
> développeur, avec **revue manuelle** (souvent 2 à 7 jours).

## 1. Fichier à uploader

```
bin\GiroPink.iq
```

Le régénérer si besoin : double-clic **`scripts\BUILD-IQ.bat`**

## 2. Étapes (1ère publication)

1. Ouvre **[apps.garmin.com/developer/upload](https://apps.garmin.com/developer/upload)**
   (ou **[apps-developer.garmin.com](https://apps-developer.garmin.com)**).
2. Connecte-toi avec ton **compte Garmin**.
3. **Choisir un fichier** → `bin\GiroPink.iq`.
4. **Version** → `1.0.0`.
5. **Continuer** → remplis la fiche store (textes dans `FICHE-STORE-GARMIN.md`).
6. Ajoute les **images** (voir plus bas).
7. **Soumets** → attente de validation Garmin.
8. Une fois approuvé : visible dans le **Connect IQ Store** (app Garmin Connect mobile).

## 3. Images prêtes (dossier `store-assets\`)

| Champ du portail | Fichier | Taille |
| --- | --- | --- |
| Image principale | `image-principale-1440x720.png` | 1440×720 |
| Image de couverture | `image-couverture-500x500.png` | 500×500 |
| Capture 1 (Z2 bleu) | `capture-z2-bleu.png` | 282×470 |
| Capture 2 (Z4 jaune) | `capture-z4-jaune.png` | 282×470 |
| Capture 3 (Z6 rouge) | `capture-z6-rouge.png` | 282×470 |
| Icône (déjà dans l'app) | `..\resources\drawables\launcher_icon.png` | 40×40 |

Régénérer les images : `py store-assets\generate_store_images.py`

## 4. Mises à jour suivantes

1. Incrémente la version dans `manifest.xml` (ex. `1.0.1`).
2. `scripts\BUILD-IQ.bat`.
3. Portail développeur → ton app → **Upload new version**.

## 5. Usage perso sans store

Pas besoin de publier pour l'utiliser : `scripts\METTRE-SUR-IQ.bat` copie le `.prg`
sur le GPS (`GARMIN\APPS\`). Seul toi peux alors l'installer.

## Liens utiles

- [Soumettre une app (Garmin)](https://developer.garmin.com/connect-iq/submit-an-app/)
- [Guidelines de revue](https://developer.garmin.com/connect-iq/app-review-guidelines/)
