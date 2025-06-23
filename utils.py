import streamlit as st
import json
import csv
import io
from typing import Dict, List, Any

def load_json_file(uploaded_file) -> Dict[str, Any]:
    """Charge et valide un fichier JSON"""
    try:
        content = uploaded_file.read().decode('utf-8')
        return json.loads(content)
    except json.JSONDecodeError:
        st.error("Fichier JSON invalide")
        return {}
    except Exception as e:
        st.error(f"Erreur lors du chargement : {str(e)}")
        return {}

def create_sample_json() -> Dict[str, Any]:
    """Crée un exemple de fichier JSON d'entrée"""
    return {
        "domaine": "Cybersécurité - Formation aux bonnes pratiques",
        "classification_bloom": {
            "se_souvenir": [
                "Identifier les principales menaces cybersécurité",
                "Reconnaître les signes d'une tentative de phishing",
                "Mémoriser les bonnes pratiques de sécurité informatique"
            ],
            "comprendre": [
                "Expliquer les principes de base de la sécurité informatique",
                "Interpréter les niveaux de risque cybersécurité",
                "Distinguer les différents types de malwares"
            ],
            "appliquer": [
                "Mettre en œuvre les bonnes pratiques de mots de passe",
                "Configurer un antivirus sur son poste de travail",
                "Utiliser correctement un VPN"
            ],
            "analyser": [
                "Analyser les vulnérabilités d'un système informatique",
                "Évaluer la fiabilité d'un email suspect",
                "Examiner les logs de sécurité"
            ],
            "evaluer": [
                "Juger de l'efficacité des mesures de sécurité en place",
                "Critiquer les politiques de sécurité existantes",
                "Évaluer les risques d'un nouvel outil numérique"
            ],
            "creer": [
                "Concevoir un plan de réponse aux incidents",
                "Élaborer une charte de sécurité informatique",
                "Développer une stratégie de sensibilisation"
            ]
        },
        "objectifs_smart": [
            {
                "objectif": "À la fin de la formation, l'apprenant sera capable d'identifier 90% des tentatives de phishing dans un test de 20 emails en moins de 10 minutes",
                "specifique": "Identifier les tentatives de phishing",
                "mesurable": "90% de réussite sur 20 emails",
                "atteignable": "Test adapté au niveau débutant avec indices visuels",
                "pertinent": "Compétence essentielle en cybersécurité quotidienne",
                "temporel": "10 minutes maximum",
                "niveau_bloom": "se_souvenir"
            },
            {
                "objectif": "L'apprenant créera un mot de passe fort de 12 caractères minimum respectant 4 critères de complexité en 5 minutes",
                "specifique": "Créer un mot de passe fort",
                "mesurable": "12 caractères, 4 critères respectés",
                "atteignable": "Outils d'aide et générateur disponibles",
                "pertinent": "Base de la sécurité personnelle",
                "temporel": "5 minutes",
                "niveau_bloom": "appliquer"
            },
            {
                "objectif": "L'apprenant analysera et évaluera 5 politiques de sécurité différentes en 30 minutes pour en identifier les failles",
                "specifique": "Analyser les politiques de sécurité",
                "mesurable": "5 politiques, identification des failles",
                "atteignable": "Grille d'analyse fournie",
                "pertinent": "Compétence managériale en cybersécurité",
                "temporel": "30 minutes",
                "niveau_bloom": "analyser"
            }
        ],
        "evaluation_difficulte": {
            "facile": [
                "Reconnaissance phishing de base",
                "Création mot de passe",
                "Installation antivirus"
            ],
            "moyen": [
                "Configuration VPN",
                "Analyse logs simples",
                "Évaluation politiques existantes"
            ],
            "difficile": [
                "Conception plan incident",
                "Élaboration charte sécurité",
                "Stratégie sensibilisation complète"
            ],
            "progression_temporelle": "6 heures de formation réparties sur 3 sessions de 2h",
            "prerequis": "Connaissances informatiques de base",
            "public_cible": "Employés de bureau, managers, équipes IT"
        }
    }

def export_to_csv(sequencer_data: List[Dict[str, str]]) -> str:
    """Export le séquenceur au format CSV"""
    output = io.StringIO()
    fieldnames = [
        'sequence', 
        'num_ecran', 
        'titre_ecran', 
        'sous_titre', 
        'resume_contenu', 
        'type_activite', 
        'commentaire'
    ]
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in sequencer_data:
        writer.writerow({
            'sequence': row.get('sequence', ''),
            'num_ecran': row.get('num_ecran', ''),
            'titre_ecran': row.get('titre_ecran', ''),
            'sous_titre': row.get('sous_titre', ''),
            'resume_contenu': row.get('resume_contenu', ''),
            'type_activite': row.get('type_activite', ''),
            'commentaire': row.get('commentaire', '')
        })
    
    return output.getvalue()

def validate_input_data(data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """Valide les données d'entrée et retourne les erreurs éventuelles"""
    errors = []
    
    # Vérification des champs obligatoires
    required_fields = ['domaine', 'classification_bloom', 'objectifs_smart', 'evaluation_difficulte']
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Champ manquant : {field}")
        elif not data[field]:
            errors.append(f"Champ vide : {field}")
    
    # Vérification de la structure classification_bloom
    if 'classification_bloom' in data:
        bloom_levels = ['se_souvenir', 'comprendre', 'appliquer', 'analyser', 'evaluer', 'creer']
        bloom_data = data['classification_bloom']
        
        if not isinstance(bloom_data, dict):
            errors.append("classification_bloom doit être un objet JSON")
        else:
            # Vérifier qu'au moins un niveau de Bloom est présent
            valid_levels = [level for level in bloom_levels if level in bloom_data and bloom_data[level]]
            if not valid_levels:
                errors.append("Aucun niveau de Bloom valide trouvé")
    
    # Vérification de la structure objectifs_smart
    if 'objectifs_smart' in data:
        objectifs = data['objectifs_smart']
        if not isinstance(objectifs, list):
            errors.append("objectifs_smart doit être une liste")
        elif len(objectifs) == 0:
            errors.append("Aucun objectif SMART défini")
        else:
            required_smart_fields = ['objectif', 'specifique', 'mesurable', 'atteignable', 'pertinent', 'temporel']
            for i, obj in enumerate(objectifs):
                if not isinstance(obj, dict):
                    errors.append(f"Objectif {i+1} : doit être un objet")
                else:
                    for field in required_smart_fields:
                        if field not in obj or not obj[field]:
                            errors.append(f"Objectif {i+1} : champ manquant ou vide - {field}")
    
    return len(errors) == 0, errors

def generate_statistics(sequencer_data: List[Dict[str, str]]) -> Dict[str, Any]:
    """Génère des statistiques sur le séquenceur"""
    if not sequencer_data:
        return {}
    
    # Compter les séquences uniques
    sequences = set()
    activity_types = []
    
    for item in sequencer_data:
        if item.get('sequence'):
            sequences.add(item['sequence'])
        if item.get('type_activite'):
            activity_types.append(item['type_activite'])
    
    # Estimation du temps (3 minutes par écran en moyenne)
    estimated_time = len(sequencer_data) * 3
    
    # Distribution des types d'activités
    activity_distribution = {}
    for activity in activity_types:
        activity_distribution[activity] = activity_distribution.get(activity, 0) + 1
    
    return {
        'total_screens': len(sequencer_data),
        'total_sequences': len(sequences),
        'unique_activities': len(set(activity_types)),
        'estimated_time_minutes': estimated_time,
        'activity_distribution': activity_distribution,
        'sequences_list': list(sequences)
    }