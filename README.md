# 🎓 Générateur de Séquenceur Pédagogique

## 📋 Description

Application Streamlit qui automatise la création de séquenceurs pédagogiques structurés à partir d'objectifs d'apprentissage classifiés selon la taxonomie de Bloom et formatés selon les critères SMART.

## ✨ Fonctionnalités

- **Import JSON** : Chargement des données d'entrée structurées
- **Génération automatique** : Création de séquenceurs via LLM (GPT-4)
- **Taxonomie de Bloom** : Respect de la progression pédagogique
- **Objectifs SMART** : Intégration des critères de qualité
- **Export multiple** : CSV, JSON et Excel
- **Interface intuitive** : Navigation simple et claire

## 🚀 Installation

### Prérequis
- Python 3.8+
- Clé API OpenAI

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Configuration
1. Copiez `.env.example` vers `.env`
2. Ajoutez votre clé API OpenAI dans `.env`

```bash
cp .env.example .env
# Éditez .env avec votre clé API
```

## 📱 Utilisation

### Lancement de l'application
```bash
streamlit run app.py
```

### Format des données d'entrée (JSON)

```json
{
  "domaine": "Votre domaine d'expertise",
  "classification_bloom": {
    "se_souvenir": ["objectif 1", "objectif 2"],
    "comprendre": ["objectif 1", "objectif 2"],
    "appliquer": ["objectif 1", "objectif 2"],
    "analyser": ["objectif 1", "objectif 2"],
    "evaluer": ["objectif 1", "objectif 2"],
    "creer": ["objectif 1", "objectif 2"]
  },
  "objectifs_smart": [
    {
      "objectif": "Description complète",
      "specifique": "Quoi précisément",
      "mesurable": "Critères quantifiables",
      "atteignable": "Moyens disponibles",
      "pertinent": "Utilité/contexte",
      "temporel": "Délai/durée",
      "niveau_bloom": "niveau_taxonomique"
    }
  ],
  "evaluation_difficulte": {
    "facile": ["objectifs simples"],
    "moyen": ["objectifs intermédiaires"],
    "difficile": ["objectifs complexes"],
    "progression_temporelle": "durée totale",
    "prerequis": "connaissances requises",
    "public_cible": "description apprenants"
  }
}
```

## 📊 Format de sortie

Le séquenceur généré contient les colonnes suivantes :

| Colonne | Description |
|---------|-------------|
| `sequence` | Nom de la séquence pédagogique |
| `num_ecran` | Numérotation unique (XX-SeqYY-ZZ) |
| `titre_ecran` | Titre principal de l'écran |
| `sous_titre` | Sous-titre ou focus spécifique |
| `resume_contenu` | Description détaillée du contenu |
| `type_activite` | Modalité pédagogique et interaction |
| `commentaire` | Notes additionnelles (optionnel) |

## 🗂️ Structure du projet

```
📁 pedagogical-sequencer/
├── 📄 app.py                    # Application principale Streamlit
├── 📄 pedagogical_sequencer.py  # Classe de génération LLM
├── 📄 utils.py                  # Fonctions utilitaires
├── 📄 config.py                 # Configuration et constantes
├── 📄 requirements.txt          # Dépendances Python
├── 📄 .env.example              # Variables d'environnement
└── 📄 README.md                 # Documentation
```

## 🎯 Taxonomie de Bloom intégrée

L'application respecte les 6 niveaux de la taxonomie de Bloom :

1. **Se souvenir** → Présentations, flashcards
2. **Comprendre** → QCM avec feedback
3. **Appliquer** → Simulations, exercices
4. **Analyser** → Études de cas
5. **Évaluer** → Évaluations par pairs
6. **Créer** → Projets créatifs

## 📈 Types d'activités disponibles

- Présentation animée
- Question à choix multiple avec feedback
- Glisser-déposer avec feedback
- Simulation interactive
- Étude de cas
- Évaluation par pairs
- Projet créatif
- Dialogue interactif

## 🔧 Configuration avancée

### Personnalisation du modèle LLM
Modifiez `config.py` pour ajuster :
- Température de génération
- Nombre de tokens maximum
- Modèle OpenAI utilisé

### Ajout de nouveaux types d'activités
Étendez `ACTIVITY_TYPES` dans `config.py`

## 🐛 Dépannage

### Erreurs courantes

**Erreur de clé API**
```
Vérifiez que votre clé OpenAI est valide et active
```

**Fichier JSON invalide**
```
Utilisez le modèle fourni comme base
Vérifiez la syntaxe JSON
```

**Génération échoue**
```
Vérifiez votre connexion internet
Assurez-vous d'avoir des crédits OpenAI
Réduisez la complexité des données d'entrée
```

## 📄 Licence

MIT License - Voir le fichier LICENSE pour plus de détails

## 🤝 Contribution

Les contributions sont les bienvenues ! 

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation
- Vérifiez les exemples fournis