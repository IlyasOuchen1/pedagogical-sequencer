import streamlit as st
import json
import csv
import io
import re
from typing import Dict, List, Any, Tuple

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
    """Crée un exemple de fichier JSON pour le nouveau format"""
    return {
        "classification": {
            "classification": "Objectif: L'apprenant sera capable de décrire les événements clés de l'histoire du Maroc au 19ème siècle.\nVerbe principal: décrire\nNiveau de Bloom: Comprendre\nJustification: Le verbe \"décrire\" implique que l'apprenant doit déterminer le sens des événements et les communiquer de manière claire, ce qui correspond au niveau de compréhension de la taxonomie de Bloom.\n\n---\n\nObjectif: L'apprenant sera capable d'analyser les impacts des changements politiques et sociaux sur le Maroc durant le 19ème siècle.\nVerbe principal: analyser\nNiveau de Bloom: Analyser\nJustification: Le verbe \"analyser\" indique que l'apprenant doit décomposer les impacts en leurs parties constitutives et examiner comment ces parties sont liées, ce qui correspond au niveau d'analyse de la taxonomie de Bloom.\n\n---\n\nObjectif: L'apprenant sera capable d'évaluer l'influence des puissances étrangères sur le Maroc au 19ème siècle.\nVerbe principal: évaluer\nNiveau de Bloom: Évaluer\nJustification: Le verbe \"évaluer\" implique que l'apprenant doit porter des jugements basés sur des critères concernant l'influence des puissances étrangères, ce qui correspond au niveau d'évaluation de la taxonomie de Bloom."
        },
        "formatted_objectives": {
            "formatted_objectives": "1. À la fin de la semaine 4, l'apprenant sera capable de décrire au moins cinq événements clés de l'histoire du Maroc au 19ème siècle en fournissant des détails sur leur contexte et leur importance.\n\n2. À la fin de la semaine 6, l'apprenant sera capable d'analyser les impacts de trois changements politiques et sociaux majeurs sur le Maroc durant le 19ème siècle en utilisant des exemples concrets et des références historiques.\n\n3. À la fin de la semaine 8, l'apprenant sera capable d'évaluer l'influence de deux puissances étrangères sur le Maroc au 19ème siècle en fournissant des exemples précis et en discutant des conséquences de cette influence sur la politique marocaine."
        },
        "difficulty_evaluation": {
            "difficulty_evaluation": "1. **Objectif : L'apprenant sera capable de décrire les événements clés de l'histoire du Maroc au 19ème siècle.**\n   - **Niveau de difficulté : 2**\n   - **Justification :** Cet objectif nécessite une compréhension des faits historiques, mais il s'agit principalement de mémorisation et de restitution d'informations.\n   - **Temps nécessaire :** Environ 5-7 heures pour la recherche et la révision.\n   - **Conseils :** Encourager l'apprenant à créer une chronologie des événements pour faciliter la mémorisation.\n\n2. **Objectif : L'apprenant sera capable d'analyser les impacts des changements politiques et sociaux sur le Maroc durant le 19ème siècle.**\n   - **Niveau de difficulté : 3**\n   - **Justification :** Cet objectif demande une compréhension plus profonde des relations de cause à effet et une capacité d'analyse critique des événements.\n   - **Temps nécessaire :** Environ 10-15 heures pour la recherche, l'analyse et la rédaction.\n   - **Conseils :** Décomposer en sous-objectifs comme identifier les changements politiques, explorer les impacts sociaux, et établir des liens entre les deux.\n\n3. **Objectif : L'apprenant sera capable d'évaluer l'influence des puissances étrangères sur le Maroc au 19ème siècle.**\n   - **Niveau de difficulté : 4**\n   - **Justification :** Cet objectif demande une évaluation complexe des influences externes, nécessitant une analyse critique des sources et des impacts historiques.\n   - **Temps nécessaire :** Environ 15-20 heures pour la recherche, l'analyse et la rédaction.\n   - **Conseils :** Décomposer en sous-objectifs comme identifier les puissances étrangères, analyser leurs motivations, et évaluer les conséquences de leur influence sur le Maroc."
        },
        "domaine": "Histoire du Maroc au 19ème siècle",
        "contexte": "Formation universitaire niveau L2, étudiants en histoire"
    }

def validate_new_format_data(data: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
    """
    Valide les données du nouveau format et retourne des statistiques
    """
    errors = []
    stats = {
        'objectives_count': 0,
        'bloom_levels': 0,
        'difficulty_levels': 0,
        'temporal_indicators': 0
    }
    
    # Vérification des champs obligatoires
    required_fields = ['classification', 'formatted_objectives', 'difficulty_evaluation']
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Champ principal manquant : {field}")
        elif not isinstance(data[field], dict):
            errors.append(f"Le champ {field} doit être un objet")
        elif field not in data[field]:
            errors.append(f"Sous-champ manquant : {field}.{field}")
        elif not data[field][field]:
            errors.append(f"Contenu vide : {field}.{field}")
    
    # Analyse de la classification si présente
    if 'classification' in data and 'classification' in data['classification']:
        classification_text = data['classification']['classification']
        
        # Compter les objectifs (séparés par ---)
        objectives = classification_text.split('---')
        stats['objectives_count'] = len([obj for obj in objectives if obj.strip()])
        
        # Compter les niveaux de Bloom uniques
        bloom_levels = set()
        for line in classification_text.split('\n'):
            if 'Niveau de Bloom:' in line:
                level = line.split('Niveau de Bloom:')[1].strip()
                bloom_levels.add(level.lower())
        stats['bloom_levels'] = len(bloom_levels)
    
    # Analyse des objectifs formatés
    if 'formatted_objectives' in data and 'formatted_objectives' in data['formatted_objectives']:
        objectives_text = data['formatted_objectives']['formatted_objectives']
        
        # Vérifier la numérotation
        numbered_objectives = re.findall(r'\d+\.', objectives_text)
        if len(numbered_objectives) != stats['objectives_count'] and stats['objectives_count'] > 0:
            errors.append("Le nombre d'objectifs SMART ne correspond pas à la classification")
        
        # Compter les indicateurs temporels
        temporal_matches = re.findall(r'semaine \d+|fin de.*?semaine', objectives_text, re.IGNORECASE)
        stats['temporal_indicators'] = len(temporal_matches)
    
    # Analyse de l'évaluation de difficulté
    if 'difficulty_evaluation' in data and 'difficulty_evaluation' in data['difficulty_evaluation']:
        difficulty_text = data['difficulty_evaluation']['difficulty_evaluation']
        
        # Compter les niveaux de difficulté
        difficulty_levels = set()
        difficulty_matches = re.findall(r'Niveau de difficulté\s*:\s*(\d+)', difficulty_text)
        for match in difficulty_matches:
            difficulty_levels.add(int(match))
        stats['difficulty_levels'] = len(difficulty_levels)
        
        # Vérifier la cohérence avec les objectifs
        difficulty_objectives = re.findall(r'\d+\.\s*\*\*Objectif', difficulty_text)
        if len(difficulty_objectives) != stats['objectives_count'] and stats['objectives_count'] > 0:
            errors.append("Le nombre d'évaluations de difficulté ne correspond pas aux objectifs")
    
    return len(errors) == 0, errors, stats

def extract_bloom_progression(classification_text: str) -> List[str]:
    """Extrait la progression des niveaux de Bloom dans l'ordre"""
    bloom_progression = []
    
    objectives = classification_text.split('---')
    for obj in objectives:
        if obj.strip():
            for line in obj.split('\n'):
                if 'Niveau de Bloom:' in line:
                    level = line.split('Niveau de Bloom:')[1].strip()
                    bloom_progression.append(level)
                    break
    
    return bloom_progression

def extract_temporal_sequence(formatted_objectives: str) -> List[Dict[str, str]]:
    """Extrait la séquence temporelle des objectifs"""
    temporal_sequence = []
    
    # Pattern pour extraire objectifs numérotés avec détails temporels
    pattern = r'(\d+)\.\s*(.*?)(?=\n\n|\n\d+\.|\Z)'
    matches = re.findall(pattern, formatted_objectives, re.DOTALL)
    
    for num, content in matches:
        # Extraire la semaine
        week_match = re.search(r'semaine (\d+)', content.lower())
        week = week_match.group(1) if week_match else None
        
        # Extraire le verbe d'action principal
        verb_match = re.search(r'capable de (\w+)', content.lower())
        verb = verb_match.group(1) if verb_match else None
        
        temporal_sequence.append({
            'numero': int(num),
            'semaine': week,
            'verbe': verb,
            'objectif_complet': content.strip()
        })
    
    return sorted(temporal_sequence, key=lambda x: (int(x['semaine']) if x['semaine'] else 999, x['numero']))

def extract_difficulty_matrix(difficulty_text: str) -> Dict[str, Dict[str, Any]]:
    """Extrait une matrice de difficulté détaillée"""
    matrix = {}
    
    # Pattern pour extraire toutes les informations de difficulté
    pattern = r'(\d+)\.\s*\*\*Objectif\s*:\s*(.*?)\*\*\s*\n\s*-\s*\*\*Niveau de difficulté\s*:\s*(\d+)\*\*\s*\n\s*-\s*\*\*Justification\s*:\*\*\s*(.*?)\n\s*-\s*\*\*Temps nécessaire\s*:\*\*\s*(.*?)\n'
    
    matches = re.findall(pattern, difficulty_text, re.DOTALL)
    
    for num, objectif, niveau, justification, temps in matches:
        matrix[f"objectif_{num}"] = {
            'objectif': objectif.strip(),
            'niveau_difficulte': int(niveau),
            'justification': justification.strip(),
            'temps_estime': temps.strip(),
            'numero': int(num)
        }
    
    return matrix

def export_to_csv(sequencer_data: List[Dict[str, str]]) -> str:
    """Export le séquenceur au format CSV avec les nouveaux champs"""
    output = io.StringIO()
    fieldnames = [
        'sequence', 
        'num_ecran', 
        'titre_ecran', 
        'sous_titre', 
        'resume_contenu', 
        'type_activite',
        'niveau_bloom',
        'difficulte',
        'duree_estimee',
        'objectif_lie',
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
            'niveau_bloom': row.get('niveau_bloom', ''),
            'difficulte': row.get('difficulte', ''),
            'duree_estimee': row.get('duree_estimee', ''),
            'objectif_lie': row.get('objectif_lie', ''),
            'commentaire': row.get('commentaire', '')
        })
    
    return output.getvalue()

def validate_activity_types(sequencer_data: List[Dict[str, str]]) -> List[str]:
    """Valide que seuls les types d'activités autorisés sont utilisés"""
    authorized_types = ['text', 'quiz', 'accordion', 'video', 'image', 'flash-card']
    errors = []
    
    for i, item in enumerate(sequencer_data):
        activity_type = item.get('type_activite', '')
        if activity_type not in authorized_types:
            errors.append(f"Écran {i+1}: Type d'activité non autorisé '{activity_type}'. Types autorisés: {', '.join(authorized_types)}")
    
    return errors

def get_activity_recommendations(bloom_level: str, difficulty: str) -> List[str]:
    """Retourne les types d'activités recommandés selon Bloom et difficulté"""
    
    # Recommandations par niveau de Bloom
    bloom_recommendations = {
        'se_souvenir': ['text', 'flash-card', 'image'],
        'comprendre': ['text', 'video', 'accordion', 'quiz'],
        'appliquer': ['quiz', 'accordion'],
        'analyser': ['accordion', 'quiz', 'image'],
        'evaluer': ['quiz', 'accordion'],
        'creer': ['accordion', 'quiz']
    }
    
    # Recommandations par difficulté
    difficulty_recommendations = {
        'facile': ['text', 'flash-card', 'image', 'video'],
        'moyen': ['quiz', 'accordion', 'text', 'image'],
        'difficile': ['accordion', 'quiz']
    }
    
    bloom_types = bloom_recommendations.get(bloom_level, ['text'])
    difficulty_types = difficulty_recommendations.get(difficulty, ['text'])
    
    # Intersection des recommandations
    recommended = list(set(bloom_types) & set(difficulty_types))
    
    # Si aucune intersection, prendre les types Bloom
    if not recommended:
        recommended = bloom_types
    
    return recommended

def generate_activity_statistics(sequencer_data: List[Dict[str, str]]) -> Dict[str, Any]:
    """Génère des statistiques spécifiques aux types d'activités"""
    
    activity_stats = {
        'distribution': {},
        'by_bloom': {},
        'by_difficulty': {},
        'by_sequence': {},
        'total_duration_by_type': {},
        'recommendations_compliance': 0
    }
    
    authorized_types = ['text', 'quiz', 'accordion', 'video', 'image', 'flash-card']
    compliant_count = 0
    
    for item in sequencer_data:
        activity_type = item.get('type_activite', 'unknown')
        bloom_level = item.get('niveau_bloom', 'unknown')
        difficulty = item.get('difficulte', 'unknown')
        sequence = item.get('sequence', 'unknown')
        duration = int(item.get('duree_estimee', 0))
        
        # Distribution générale
        activity_stats['distribution'][activity_type] = activity_stats['distribution'].get(activity_type, 0) + 1
        
        # Par niveau Bloom
        if bloom_level not in activity_stats['by_bloom']:
            activity_stats['by_bloom'][bloom_level] = {}
        activity_stats['by_bloom'][bloom_level][activity_type] = activity_stats['by_bloom'][bloom_level].get(activity_type, 0) + 1
        
        # Par difficulté
        if difficulty not in activity_stats['by_difficulty']:
            activity_stats['by_difficulty'][difficulty] = {}
        activity_stats['by_difficulty'][difficulty][activity_type] = activity_stats['by_difficulty'][difficulty].get(activity_type, 0) + 1
        
        # Par séquence
        if sequence not in activity_stats['by_sequence']:
            activity_stats['by_sequence'][sequence] = {}
        activity_stats['by_sequence'][sequence][activity_type] = activity_stats['by_sequence'][sequence].get(activity_type, 0) + 1
        
        # Durée totale par type
        activity_stats['total_duration_by_type'][activity_type] = activity_stats['total_duration_by_type'].get(activity_type, 0) + duration
        
        # Vérification de conformité
        if activity_type in authorized_types:
            recommended_types = get_activity_recommendations(bloom_level, difficulty)
            if activity_type in recommended_types:
                compliant_count += 1
    
    # Pourcentage de conformité aux recommandations
    if sequencer_data:
        activity_stats['recommendations_compliance'] = (compliant_count / len(sequencer_data)) * 100
    
    return activity_stats
    """Génère des statistiques détaillées sur le séquenceur"""
    if not sequencer_data:
        return {}
    
    stats = {
        'total_screens': len(sequencer_data),
        'total_sequences': 0,
        'bloom_distribution': {},
        'difficulty_distribution': {},
        'activity_distribution': {},
        'duration_stats': {},
        'sequence_breakdown': {}
    }
    
    # Collecte des données
    sequences = set()
    bloom_levels = []
    difficulties = []
    activities = []
    durations = []
    
    for item in sequencer_data:
        if item.get('sequence'):
            sequences.add(item['sequence'])
        if item.get('niveau_bloom'):
            bloom_levels.append(item['niveau_bloom'])
        if item.get('difficulte'):
            difficulties.append(item['difficulte'])
        if item.get('type_activite'):
            activities.append(item['type_activite'])
        if item.get('duree_estimee'):
            try:
                durations.append(int(item['duree_estimee']))
            except (ValueError, TypeError):
                durations.append(5)  # Valeur par défaut
    
    # Calcul des statistiques
    stats['total_sequences'] = len(sequences)
    
    # Distribution par niveau de Bloom
    for level in bloom_levels:
        stats['bloom_distribution'][level] = stats['bloom_distribution'].get(level, 0) + 1
    
    # Distribution par difficulté
    for diff in difficulties:
        stats['difficulty_distribution'][diff] = stats['difficulty_distribution'].get(diff, 0) + 1
    
    # Distribution par type d'activité
    for activity in activities:
        stats['activity_distribution'][activity] = stats['activity_distribution'].get(activity, 0) + 1
    
    # Statistiques de durée
    if durations:
        stats['duration_stats'] = {
            'total_minutes': sum(durations),
            'average_per_screen': sum(durations) / len(durations),
            'min_duration': min(durations),
            'max_duration': max(durations)
        }
    
    # Répartition par séquence
    sequence_data = {}
    for item in sequencer_data:
        seq = item.get('sequence', 'Non défini')
        if seq not in sequence_data:
            sequence_data[seq] = {
                'screen_count': 0,
                'total_duration': 0,
                'bloom_levels': set(),
                'difficulties': set()
            }
        
        sequence_data[seq]['screen_count'] += 1
        if item.get('duree_estimee'):
            try:
                sequence_data[seq]['total_duration'] += int(item['duree_estimee'])
            except (ValueError, TypeError):
                sequence_data[seq]['total_duration'] += 5
        
        if item.get('niveau_bloom'):
            sequence_data[seq]['bloom_levels'].add(item['niveau_bloom'])
        if item.get('difficulte'):
            sequence_data[seq]['difficulties'].add(item['difficulte'])
    
    # Convertir les sets en listes pour la sérialisation
    for seq_name, seq_data in sequence_data.items():
        seq_data['bloom_levels'] = list(seq_data['bloom_levels'])
        seq_data['difficulties'] = list(seq_data['difficulties'])
    
    stats['sequence_breakdown'] = sequence_data
    
    return stats

def validate_temporal_coherence(formatted_objectives: str, difficulty_evaluation: str) -> List[str]:
    """Valide la cohérence temporelle entre objectifs et évaluations"""
    warnings = []
    
    # Extraire les progressions temporelles
    temporal_sequence = extract_temporal_sequence(formatted_objectives)
    difficulty_matrix = extract_difficulty_matrix(difficulty_evaluation)
    
    # Vérifier la cohérence des numérotations
    objective_numbers = {item['numero'] for item in temporal_sequence}
    difficulty_numbers = {data['numero'] for data in difficulty_matrix.values()}
    
    if objective_numbers != difficulty_numbers:
        warnings.append("Incohérence dans la numérotation des objectifs entre SMART et évaluation de difficulté")
    
    # Vérifier la progression logique des semaines
    weeks = [int(item['semaine']) for item in temporal_sequence if item['semaine']]
    if weeks and weeks != sorted(weeks):
        warnings.append("La progression temporelle des semaines n'est pas logique")
    
    return warnings