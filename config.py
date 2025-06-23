# Configuration générale de l'application
APP_CONFIG = {
    "title": "Générateur de Séquenceur Pédagogique",
    "icon": "🎓",
    "layout": "wide",
    "version": "1.0.0"
}

# Configuration OpenAI
OPENAI_CONFIG = {
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 3000
}

# Taxonomie de Bloom - Niveaux et descriptions
BLOOM_TAXONOMY = {
    "se_souvenir": {
        "description": "Rappeler des faits, concepts, termes",
        "verbes_action": ["identifier", "reconnaître", "mémoriser", "lister", "nommer"],
        "activites_recommandees": ["Présentation animée", "Flashcards", "Quiz simple"]
    },
    "comprendre": {
        "description": "Expliquer, interpréter, donner des exemples",
        "verbes_action": ["expliquer", "interpréter", "distinguer", "résumer", "classer"],
        "activites_recommandees": ["Question à choix multiple avec feedback", "Schémas à compléter"]
    },
    "appliquer": {
        "description": "Utiliser des connaissances dans des situations nouvelles",
        "verbes_action": ["appliquer", "utiliser", "mettre en œuvre", "exécuter", "résoudre"],
        "activites_recommandees": ["Simulation interactive", "Exercices pratiques", "Glisser-déposer"]
    },
    "analyser": {
        "description": "Décomposer en parties, identifier relations",
        "verbes_action": ["analyser", "examiner", "comparer", "contraster", "organiser"],
        "activites_recommandees": ["Étude de cas", "Analyse comparative", "Diagrammes"]
    },
    "evaluer": {
        "description": "Porter des jugements basés sur des critères",
        "verbes_action": ["évaluer", "critiquer", "juger", "justifier", "recommander"],
        "activites_recommandees": ["Évaluation par pairs", "Grilles d'évaluation", "Débats"]
    },
    "creer": {
        "description": "Combiner des éléments pour créer quelque chose de nouveau",
        "verbes_action": ["créer", "concevoir", "développer", "élaborer", "construire"],
        "activites_recommandees": ["Projet créatif", "Conception de solutions", "Production"]
    }
}

# Types d'activités pédagogiques disponibles
ACTIVITY_TYPES = {
    "presentation": {
        "nom": "Présentation animée",
        "description": "Contenu présenté de manière interactive",
        "bloom_adapte": ["se_souvenir", "comprendre"],
        "duree_moyenne": 2
    },
    "qcm": {
        "nom": "Question à choix multiple avec feedback",
        "description": "Questions avec réponses multiples et explications",
        "bloom_adapte": ["comprendre", "appliquer"],
        "duree_moyenne": 3
    },
    "glisser_deposer": {
        "nom": "Glisser-déposer avec feedback",
        "description": "Activité de manipulation d'éléments",
        "bloom_adapte": ["appliquer", "analyser"],
        "duree_moyenne": 4
    },
    "simulation": {
        "nom": "Simulation interactive",
        "description": "Environnement simulé pour la pratique",
        "bloom_adapte": ["appliquer", "analyser"],
        "duree_moyenne": 8
    },
    "etude_cas": {
        "nom": "Étude de cas",
        "description": "Analyse de situations réelles",
        "bloom_adapte": ["analyser", "evaluer"],
        "duree_moyenne": 10
    },
    "evaluation_pairs": {
        "nom": "Évaluation par pairs",
        "description": "Évaluation mutuelle entre apprenants",
        "bloom_adapte": ["evaluer"],
        "duree_moyenne": 15
    },
    "projet_creatif": {
        "nom": "Projet créatif",
        "description": "Création d'un livrable original",
        "bloom_adapte": ["creer"],
        "duree_moyenne": 20
    },
    "dialogue_interactif": {
        "nom": "Dialogue interactif",
        "description": "Conversation guidée avec personnage virtuel",
        "bloom_adapte": ["comprendre", "appliquer", "analyser"],
        "duree_moyenne": 5
    }
}

# Modèles de séquences par défaut
SEQUENCE_TEMPLATES = {
    "introduction": {
        "nom": "Introduction générale au module",
        "ecrans_type": [
            "Aide de navigation",
            "Présentation personnage/contexte",
            "Objectifs et séquencement"
        ]
    },
    "contenu_principal": {
        "nom": "Séquence de contenu principal",
        "structure": "Présentation → Interaction → Application → Évaluation"
    },
    "application": {
        "nom": "Application pratique",
        "focus": "Mise en situation et exercices concrets"
    },
    "evaluation": {
        "nom": "Évaluation et synthèse",
        "ecrans_type": [
            "Évaluation formative",
            "Synthèse des apprentissages",
            "Plan d'action personnel"
        ]
    }
}

# Critères SMART - Validation
SMART_CRITERIA = {
    "specifique": {
        "description": "Objectif précis et clairement défini",
        "questions": ["Que doit faire l'apprenant ?", "Dans quel contexte ?"]
    },
    "mesurable": {
        "description": "Critères quantifiables de réussite",
        "questions": ["Comment mesurer la réussite ?", "Quels indicateurs ?"]
    },
    "atteignable": {
        "description": "Objectif réaliste selon le niveau",
        "questions": ["L'objectif est-il réaliste ?", "Quels moyens disponibles ?"]
    },
    "pertinent": {
        "description": "Aligné avec les besoins et le contexte",
        "questions": ["Pourquoi cet objectif ?", "Quelle utilité pratique ?"]
    },
    "temporel": {
        "description": "Délai défini pour l'atteinte",
        "questions": ["Dans quel délai ?", "Quelle durée d'activité ?"]
    }
}

# Niveaux de difficulté
DIFFICULTY_LEVELS = {
    "facile": {
        "description": "Concepts de base, peu de prérequis",
        "duree_moyenne": 2,
        "activites_preferees": ["presentation", "qcm"],
        "bloom_associe": ["se_souvenir", "comprendre"]
    },
    "moyen": {
        "description": "Application avec support, prérequis modérés",
        "duree_moyenne": 5,
        "activites_preferees": ["glisser_deposer", "simulation", "dialogue_interactif"],
        "bloom_associe": ["appliquer", "analyser"]
    },
    "difficile": {
        "description": "Création autonome, expertise requise",
        "duree_moyenne": 12,
        "activites_preferees": ["etude_cas", "evaluation_pairs", "projet_creatif"],
        "bloom_associe": ["evaluer", "creer"]
    }
}

# Messages d'aide et tooltips
HELP_MESSAGES = {
    "classification_bloom": "Organisez vos objectifs selon les 6 niveaux de la taxonomie de Bloom",
    "objectifs_smart": "Chaque objectif doit respecter les 5 critères SMART",
    "evaluation_difficulte": "Évaluez la complexité de chaque groupe d'objectifs",
    "api_key": "Votre clé API OpenAI est nécessaire pour la génération automatique",
    "export_csv": "Format compatible avec les outils de conception pédagogique",
    "generation": "La génération peut prendre 30 secondes à 2 minutes selon la complexité"
}

# Formats d'export disponibles
EXPORT_FORMATS = {
    "csv": {
        "extension": ".csv",
        "mime_type": "text/csv",
        "description": "Format tableur compatible"
    },
    "json": {
        "extension": ".json", 
        "mime_type": "application/json",
        "description": "Format données structurées"
    },
    "xlsx": {
        "extension": ".xlsx",
        "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "description": "Format Excel (nécessite xlsxwriter)"
    }
}

# Validation des données d'entrée
VALIDATION_RULES = {
    "min_objectifs_smart": 2,
    "max_objectifs_smart": 20,
    "min_bloom_levels": 2,
    "max_sequence_length": 25,
    "required_fields": [
        "domaine",
        "classification_bloom", 
        "objectifs_smart",
        "evaluation_difficulte"
    ]
}