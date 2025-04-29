# Guide du Développeur

## Architecture du Projet

Le projet suit une architecture modulaire en couches :

### Couches Principales

1. **Couche Présentation (UI)** : `src/ui/`
   - Gestion de l'interface utilisateur Tkinter
   - Composants réutilisables
   - Dialogues et interactions utilisateur

2. **Couche Métier (Core)** : `src/core/`
   - Logique d'analyse de charge de travail
   - Transformations et calculs

3. **Couche Données (Data)** : `src/data/`
   - Lecture et extraction de données Excel
   - Modèles de données
   - Dépôts de données

4. **Couche Services** : `src/services/`
   - Services d'exportation
   - Services auxiliaires

## Structure des Répertoires

```
analyseur-charge/
├── src/                # Code source principal
│   ├── main.py         # Point d'entrée
│   ├── constants.py    # Constantes globales
│   ├── core/           # Logique métier
│   ├── data/           # Gestion des données
│   ├── services/       # Services divers
│   └── ui/             # Interface utilisateur
├── tests/              # Tests unitaires
├── docs/               # Documentation
└── config/             # Configurations
```

## Principes de Conception

- **Single Responsibility Principle** : Chaque classe a une responsabilité unique
- **Open/Closed Principle** : Ouvert à l'extension, fermé à la modification
- **Dependency Injection** : Injection de dépendances pour faciliter les tests

## Développement

### Configuration de l'Environnement

1. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows
```

2. Installer les dépendances
```bash
pip install -r requirements.txt
pip install -e .
```

### Exécution des Tests

```bash
pytest tests/
```

### Linting et Formatage

```bash
# Vérification du style
flake8 src/

# Formatage automatique
black src/
```

## Ajout de Nouvelles Fonctionnalités

1. Créez une nouvelle branche
```bash
git checkout -b feature/nom-de-la-fonctionnalite
```

2. Implémentez la fonctionnalité en suivant l'architecture existante
   - Ajoutez des tests unitaires
   - Respectez les principes de conception

3. Mise à jour de la documentation
   - Mettez à jour README.md si nécessaire
   - Documentez les nouvelles méthodes/classes

## Contribution

- Fork du projet
- Créez une branche de fonctionnalité
- Commits descriptifs
- Pull Request avec description détaillée

##Points d'Extension

- Ajout de nouvelles stratégies d'exportation
- Support de différents formats de fichiers
- Amélioration de l'analyse de charge de travail

## Dépendances Principales

- `openpyxl` : Lecture/écriture de fichiers Excel
- `reportlab` : Génération de PDF
- `tkinter` : Interface graphique
- `pandas` : Manipulation de données (optionnel)

## Conseils de Développement

- Utilisez des type hints
- Écrivez des docstrings détaillés
- Privilégiez la composition à l'héritage
- Gardez les méthodes petites et ciblées
- Testez unitairement chaque nouvelle fonctionnalité