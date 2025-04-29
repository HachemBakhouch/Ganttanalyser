# Analyseur de Charge de Travail

## Description

L'Analyseur de Charge de Travail est une application Python qui permet d'analyser et de visualiser la charge de travail à partir de fichiers Excel. Cette application offre des fonctionnalités avancées pour comprendre la répartition des tâches par profil, projet et chef de projet.

## Fonctionnalités Principales

- Chargement de fichiers Excel
- Analyse de charge de travail par profil
- Visualisation détaillée des résultats
- Exportation des résultats (TXT, Excel, PDF)
- Interface utilisateur conviviale

## Prérequis

- Python 3.8+
- Tkinter (généralement inclus avec Python)

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-utilisateur/analyseur-charge-travail.git
cd analyseur-charge-travail
```

2. Créez un environnement virtuel (optionnel mais recommandé) :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Installez l'application :
```bash
pip install -e .
```

## Utilisation

### Depuis l'interface graphique

```bash
python -m src.main
```

### Configuration

Le fichier `config/settings.json` permet de personnaliser certains paramètres par défaut.

## Structure du Projet

```
analyseur-charge/
│
├── src/                # Code source principal
│   ├── main.py         # Point d'entrée
│   ├── core/           # Logique métier
│   ├── data/           # Gestion des données
│   ├── services/       # Services divers
│   └── ui/             # Interface utilisateur
│
├── tests/              # Tests unitaires
├── docs/               # Documentation
├── config/             # Configurations
└── resources/          # Ressources statiques
```

## Contribution

1. Forkez le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commitez vos modifications (`git commit -m 'Add some AmazingFeature'`)
4. Poussez votre branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## License

Distribué sous la license MIT. Voir `LICENSE` pour plus d'informations.

## Contact

Votre Nom - votre.email@exemple.com

Lien du projet : [https://github.com/votre-utilisateur/analyseur-charge-travail](https://github.com/votre-utilisateur/analyseur-charge-travail)
