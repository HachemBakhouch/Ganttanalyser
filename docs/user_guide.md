# Guide Utilisateur de l'Analyseur de Charge de Travail

## Introduction

L'Analyseur de Charge de Travail est un outil puissant pour analyser et visualiser la charge de travail à partir de fichiers Excel.

## Démarrage Rapide

### 1. Lancement de l'Application

- Ouvrez un terminal
- Naviguez jusqu'au répertoire du projet
- Exécutez : `python -m src.main`

### 2. Chargement d'un Fichier Excel

1. Cliquez sur le bouton "Sélectionner"
2. Choisissez votre fichier Excel
3. Configurez la plage de colonnes et de lignes si nécessaire

## Configuration des Paramètres

### Plage de Colonnes
- `De la colonne` : Colonne de début pour l'analyse
- `À la colonne` : Colonne de fin pour l'analyse
- `Colonne des profils` : Colonne contenant les noms de profils
- `Première ligne` : Ligne de début des données
- `Dernière ligne` : Ligne de fin des données

### Sélection des Profils

1. La liste des profils est automatiquement extraite du fichier
2. Sélectionnez un ou plusieurs profils à analyser
3. Vous pouvez ajouter manuellement des profils si nécessaire

## Calcul de la Charge de Travail

1. Après avoir configuré vos paramètres, cliquez sur "Calculer la charge de travail"
2. Les résultats s'afficheront dans deux onglets :
   - Résultats Globaux : Charge totale par profil
   - Résultats Détaillés : Répartition par chef de projet et projet

## Exportation des Résultats

1. Cliquez sur "Exporter les résultats"
2. Choisissez le format :
   - Texte (.txt)
   - Excel (.xlsx)
   - PDF (.pdf)
3. Sélectionnez un emplacement de sauvegarde

## Conseils et Bonnes Pratiques

- Assurez-vous que votre fichier Excel respecte la structure attendue
- Vérifiez les en-têtes et la numérotation des colonnes
- Utilisez des noms de profils cohérents
- Pour de grands fichiers, la sélection de plages spécifiques peut améliorer les performances

## Dépannage

- Si un profil n'apparaît pas, vérifiez l'orthographe et la colonne des profils
- En cas d'erreur de lecture, assurez-vous que le fichier n'est pas ouvert dans un autre programme
- Consultez les logs pour plus de détails en cas de problème

## Configuration Avancée

Des paramètres supplémentaires peuvent être configurés dans `config/settings.json`