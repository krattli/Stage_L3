# Projet xAI - Explicabilité des techniques d'IA

Ce projet a pour objectif de fournir une plateforme permettant aux utilisateurs de tester différentes techniques d'explicabilité des modèles d'IA. L'application permet à un utilisateur de créer un profil utilisateur, qui est ensuite utilisé pour personnaliser l'expérience et recommander des visualisations et des techniques adaptées aux besoins et préférences de l'utilisateur.

## Prérequis

Avant de pouvoir lancer l'app, il faut avoir sur votre machine:

- **Python 3.9+** : Langage principal du projet
- **Django 4.2+** : Framework web utilisé
- **SQLite3** : Base de données par défaut

mais normalement tout est géré par requirements.txt et l'environnement virtuel python se chargera du reste

## Installation

### 1. Cloner le repository

```bash
git clone https://github.com/votre_nom_utilisateur/Stage_L3.git
cd Stage_L3
```

### 2. Créer l'environnement virtuel python

```bash
python3 -m venv venv
```

### 3. Activer le venv

**Sur macOS/Linux :**
```bash
source venv/bin/activate
```

**Sur Windows :**
```bash
venv\Scripts\activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

## Lancer le projet

```bash
python manage.py runserver
```

Le serveur sera accessible à l'adresse : http://127.0.0.1:8000/
