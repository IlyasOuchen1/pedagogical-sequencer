from openai import OpenAI
import streamlit as st
import json
import re
from typing import Dict, List, Any

class PedagogicalSequencerV2:
    def __init__(self, api_key: str):
        """Initialise le générateur spécialisé avec la clé API OpenAI"""
        self.client = OpenAI(api_key=api_key)
        
    def generate_sequencer(self, input_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Génère un séquenceur pédagogique à partir du nouveau format de données
        """
        # Analyser les données d'entrée
        analysis = self._analyze_input_data(input_data)
        
        # Créer le prompt spécialisé
        prompt = self._create_specialized_prompt(input_data, analysis)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self._get_specialized_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            # Parser la réponse pour extraire le JSON
            content = response.choices[0].message.content
            sequencer_data = self._parse_response(content)
            
            # Enrichir avec les métadonnées analysées
            enriched_data = self._enrich_with_metadata(sequencer_data, analysis)
            
            return enriched_data
            
        except Exception as e:
            st.error(f"Erreur lors de la génération : {str(e)}")
            return []
    
    def _analyze_input_data(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse approfondie des données d'entrée du nouveau format"""
        analysis = {
            'domain': None,
            'objectives': [],
            'bloom_distribution': {},
            'difficulty_mapping': {},
            'temporal_progression': [],
            'estimated_total_hours': 0
        }
        
        # Analyser la classification
        if 'classification' in input_data and 'classification' in input_data['classification']:
            analysis['objectives'] = self._extract_objectives_from_classification(
                input_data['classification']['classification']
            )
            analysis['bloom_distribution'] = self._analyze_bloom_distribution(analysis['objectives'])
        
        # Analyser les objectifs formatés
        if 'formatted_objectives' in input_data and 'formatted_objectives' in input_data['formatted_objectives']:
            analysis['temporal_progression'] = self._extract_temporal_progression(
                input_data['formatted_objectives']['formatted_objectives']
            )
        
        # Analyser l'évaluation de difficulté
        if 'difficulty_evaluation' in input_data and 'difficulty_evaluation' in input_data['difficulty_evaluation']:
            analysis['difficulty_mapping'] = self._extract_difficulty_mapping(
                input_data['difficulty_evaluation']['difficulty_evaluation']
            )
            analysis['estimated_total_hours'] = self._calculate_total_hours(
                input_data['difficulty_evaluation']['difficulty_evaluation']
            )
        
        # Détection du domaine via LLM plutôt que par mots-clés
        analysis['domain'] = "Domaine à détecter automatiquement par le LLM"
        
        return analysis
    
    def _extract_objectives_from_classification(self, classification_text: str) -> List[Dict[str, str]]:
        """Extrait les objectifs détaillés de la classification"""
        objectives = []
        
        # Diviser par les séparateurs "---"
        objective_blocks = classification_text.split('---')
        
        for block in objective_blocks:
            if block.strip():
                objective = {}
                lines = block.strip().split('\n')
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('Objectif:'):
                        objective['objectif'] = line.replace('Objectif:', '').strip()
                    elif line.startswith('Verbe principal:'):
                        objective['verbe'] = line.replace('Verbe principal:', '').strip()
                    elif line.startswith('Niveau de Bloom:'):
                        objective['bloom'] = line.replace('Niveau de Bloom:', '').strip()
                    elif line.startswith('Justification:'):
                        objective['justification'] = line.replace('Justification:', '').strip()
                
                if objective.get('objectif'):
                    objectives.append(objective)
        
        return objectives
    
    def _analyze_bloom_distribution(self, objectives: List[Dict[str, str]]) -> Dict[str, int]:
        """Analyse la distribution des niveaux de Bloom"""
        distribution = {}
        
        for obj in objectives:
            bloom_level = obj.get('bloom', '').lower()
            # Normaliser les niveaux
            if 'comprendre' in bloom_level:
                bloom_level = 'comprendre'
            elif 'analyser' in bloom_level or 'analyse' in bloom_level:
                bloom_level = 'analyser'
            elif 'évaluer' in bloom_level or 'evaluer' in bloom_level:
                bloom_level = 'evaluer'
            elif 'appliquer' in bloom_level:
                bloom_level = 'appliquer'
            elif 'créer' in bloom_level or 'creer' in bloom_level:
                bloom_level = 'creer'
            elif 'se souvenir' in bloom_level or 'souvenir' in bloom_level:
                bloom_level = 'se_souvenir'
            
            distribution[bloom_level] = distribution.get(bloom_level, 0) + 1
        
        return distribution
    
    def _extract_temporal_progression(self, formatted_objectives: str) -> List[Dict[str, str]]:
        """Extrait la progression temporelle des objectifs SMART"""
        progression = []
        
        # Extraire les objectifs numérotés
        pattern = r'(\d+)\.\s*(.*?)(?=\n\n|\n\d+\.|\Z)'
        matches = re.findall(pattern, formatted_objectives, re.DOTALL)
        
        for num, content in matches:
            # Extraire la semaine si mentionnée
            week_match = re.search(r'semaine (\d+)', content)
            week = week_match.group(1) if week_match else None
            
            progression.append({
                'numero': num,
                'objectif': content.strip(),
                'semaine': week
            })
        
        return progression
    
    def _extract_difficulty_mapping(self, difficulty_text: str) -> Dict[str, Any]:
        """Extrait le mapping des difficultés"""
        mapping = {}
        
        # Extraire les niveaux de difficulté
        pattern = r'(\d+)\.\s*\*\*Objectif\s*:\s*(.*?)\*\*.*?Niveau de difficulté\s*:\s*(\d+).*?Temps nécessaire\s*:\s*(.*?)(?=\n\s*-|\n\n|\Z)'
        matches = re.findall(pattern, difficulty_text, re.DOTALL)
        
        for num, objectif, niveau, temps in matches:
            mapping[objectif.strip()] = {
                'niveau': int(niveau),
                'temps': temps.strip(),
                'numero': num
            }
        
        return mapping
    
    def _calculate_total_hours(self, difficulty_text: str) -> int:
        """Calcule le nombre total d'heures estimées"""
        # Extraire tous les temps mentionnés
        time_pattern = r'(\d+)-?(\d+)?\s*heures?'
        matches = re.findall(time_pattern, difficulty_text)
        
        total_hours = 0
        for match in matches:
            if match[1]:  # Range (ex: 10-15 heures)
                total_hours += int(match[1])  # Prendre la valeur haute
            else:  # Valeur unique
                total_hours += int(match[0])
        
        return total_hours
    
    def _get_specialized_system_prompt(self) -> str:
        """Prompt système spécialisé pour le nouveau format"""
        return """
        Vous êtes un expert en ingénierie pédagogique spécialisé dans la création de séquenceurs détaillés.
        Vous travaillez avec des analyses d'objectifs pédagogiques précises incluant la taxonomie de Bloom et l'évaluation SMART.
        
        VOTRE MISSION :
        Créer un séquenceur pédagogique détaillé et structuré qui respecte :
        1. La progression taxonomique de Bloom détectée dans l'analyse
        2. Les niveaux de difficulté spécifiés
        3. La progression temporelle des objectifs SMART
        4. Les spécificités du domaine d'expertise
        
        RÈGLES DE CONCEPTION :
        - Commencez par une séquence d'introduction contextuelle
        - Organisez le contenu selon la progression Bloom détectée
        - Respectez les niveaux de difficulté (2=facile, 3=moyen, 4=difficile)
        - Intégrez la progression temporelle (semaines)
        - Utilisez UNIQUEMENT les 6 types d'activités autorisés
        - Terminez par une évaluation et synthèse
        
        TYPES D'ACTIVITÉS AUTORISÉS (OBLIGATOIRE) :
        Vous devez utiliser UNIQUEMENT ces 6 types d'activités :
        
        1. **text** : Contenu textuel structuré, explications, définitions, contextualisations
           - Usage : Présentation de concepts, introductions, explications théoriques
           - Bloom : Se souvenir, Comprendre
           - Exemple : "Présentation textuelle des événements historiques clés"
        
        2. **quiz** : Questions interactives avec réponses multiples ou ouvertes
           - Usage : Évaluation, vérification des acquis, auto-évaluation
           - Bloom : Comprendre, Appliquer, Analyser
           - Exemple : "Quiz sur l'identification des dynasties marocaines"
        
        3. **accordion** : Contenu organisé en sections dépliables/repliables
           - Usage : Organisation d'informations complexes, comparaisons, chronologies
           - Bloom : Comprendre, Analyser, Évaluer
           - Exemple : "Accordion comparatif des différentes dynasties"
        
        4. **video** : Contenu vidéo explicatif, démonstrations, témoignages
           - Usage : Démonstrations, contextualisations visuelles, témoignages
           - Bloom : Se souvenir, Comprendre, Analyser
           - Exemple : "Vidéo documentaire sur les relations internationales du Maroc"
        
        5. **image** : Supports visuels interactifs, cartes, schémas, infographies
           - Usage : Visualisation, localisation, schématisation, illustration
           - Bloom : Se souvenir, Comprendre, Analyser
           - Exemple : "Carte interactive du Maroc au 19ème siècle"
        
        6. **flash-card** : Cartes d'apprentissage interactives recto-verso
           - Usage : Mémorisation, révision, associations concept-définition
           - Bloom : Se souvenir, Comprendre
           - Exemple : "Flash-cards des personnages historiques et leurs rôles"
        
        ADAPTATION SELON LE NIVEAU DE BLOOM :
        - **Se souvenir** : text, flash-card, image
        - **Comprendre** : text, video, accordion, quiz (simple)
        - **Appliquer** : quiz (pratique), accordion (procédures)
        - **Analyser** : accordion (comparaisons), quiz (analyse), image (schémas)
        - **Évaluer** : quiz (évaluation), accordion (critères)
        - **Créer** : accordion (construction), quiz (création guidée)
        
        ADAPTATION SELON LA DIFFICULTÉ :
        - **Facile (niveau 2)** : text, flash-card, image, video
        - **Moyen (niveau 3)** : quiz, accordion, combinaisons text+image
        - **Difficile (niveau 4)** : accordion complexes, quiz d'analyse, séquences multimodales
        
        FORMAT DE SORTIE :
        Retournez UNIQUEMENT un JSON valide avec un array d'objets contenant :
        - sequence : Nom de la séquence
        - num_ecran : Numérotation (XX-Seq-ZZ)
        - titre_ecran : Titre principal
        - sous_titre : Sous-titre spécifique
        - resume_contenu : Description détaillée
        - type_activite : UN SEUL des 6 types (text, quiz, accordion, video, image, flash-card)
        - niveau_bloom : Niveau taxonomique ciblé
        - difficulte : Niveau de difficulté (facile/moyen/difficile)
        - duree_estimee : Durée en minutes
        - objectif_lie : Objectif principal couvert
        - commentaire : Notes pédagogiques et instructions techniques
        """
    
    def _create_specialized_prompt(self, input_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Crée un prompt spécialisé basé sur l'analyse"""
        
        return f"""
        Créez un séquenceur pédagogique détaillé basé sur cette analyse d'objectifs :

        **ANALYSE AUTOMATIQUE DU DOMAINE :**
        Détectez automatiquement le domaine d'expertise à partir du contenu des objectifs et adaptez le séquenceur en conséquence.

        **OBJECTIFS ANALYSÉS ({len(analysis['objectives'])} objectifs) :**
        {json.dumps(analysis['objectives'], indent=2, ensure_ascii=False)}

        **DISTRIBUTION DES NIVEAUX DE BLOOM :**
        {json.dumps(analysis['bloom_distribution'], indent=2, ensure_ascii=False)}

        **PROGRESSION TEMPORELLE :**
        {json.dumps(analysis['temporal_progression'], indent=2, ensure_ascii=False)}

        **MAPPING DES DIFFICULTÉS :**
        {json.dumps(analysis['difficulty_mapping'], indent=2, ensure_ascii=False)}

        **ESTIMATION TOTALE :** {analysis['estimated_total_hours']} heures de formation

        **CONTENU COMPLET POUR ANALYSE DU DOMAINE :**
        Classification: {input_data.get('classification', {}).get('classification', '')[:500]}...
        Objectifs: {input_data.get('formatted_objectives', {}).get('formatted_objectives', '')[:500]}...

        INSTRUCTIONS SPÉCIALISÉES :
        1. **DÉTECTION AUTOMATIQUE DU DOMAINE** : Analysez le contenu pour identifier le domaine d'expertise et adaptez :
           - La terminologie spécialisée du secteur
           - Les exemples concrets et contextualisés
           - Les références appropriées (historiques, techniques, scientifiques, etc.)
           - Les modalités pédagogiques les plus efficaces pour ce domaine
           - Le niveau de langage et la complexité adaptés

        2. Adaptez les types d'activités selon le domaine détecté :
           - **Histoire/Sciences humaines** : text (chronologies), accordion (comparaisons), image (cartes/documents)
           - **Sciences/Techniques** : video (démonstrations), quiz (calculs), accordion (procédures)
           - **Langues** : flash-card (vocabulaire), quiz (grammaire), video (conversations)
           - **Formation professionnelle** : accordion (processus), quiz (situations), video (techniques)

        3. Créez 5-7 séquences principales selon la progression Bloom détectée et chaque séquence mentionne son role dans le champ 
        4. Numérotez les écrans : 01-Intro-01, 02-Seq-01, etc.
        5. Respectez les niveaux de difficulté spécifiés (2/3/4)
        6. Intégrez la progression temporelle (semaines) dans l'organisation
        7. Prévoyez 3-5 minutes par niveau de difficulté 2, 5-8 min pour niveau 3, 8-12 min pour niveau 4
        8. Assurez une couverture complète de tous les objectifs analysés
        9. **CONTEXTUALISATION MAXIMALE** : Chaque écran doit refléter le domaine spécifique détecté

        STRUCTURE ATTENDUE :
        - Introduction et contextualisation du domaine (2-3 écrans)
        - Séquences par niveau Bloom croissant
        - Intégration des objectifs selon leur progression temporelle
        - Évaluations formatives régulières adaptées au domaine
        - Synthèse et évaluation finale contextualisée

        Retournez UNIQUEMENT le JSON structuré.
        """
    
    def _parse_response(self, content: str) -> List[Dict[str, str]]:
        """Parse la réponse de l'IA et extrait le JSON"""
        try:
            # Nettoyer le contenu
            content = content.strip()
            
            # Chercher le JSON dans la réponse
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback: essayer de parser toute la réponse
                return json.loads(content)
                
        except json.JSONDecodeError as e:
            st.error(f"Erreur de parsing JSON : {str(e)}")
            st.error(f"Contenu reçu : {content[:500]}...")
            return []
    
    def _enrich_with_metadata(self, sequencer_data: List[Dict[str, str]], analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Enrichit les données du séquenceur avec les métadonnées d'analyse"""
        enriched_data = []
        
        for item in sequencer_data:
            enriched_item = item.copy()
            
            # Ajouter des métadonnées par défaut si manquantes
            if 'niveau_bloom' not in enriched_item:
                enriched_item['niveau_bloom'] = self._infer_bloom_level(item.get('type_activite', ''))
            
            if 'difficulte' not in enriched_item:
                enriched_item['difficulte'] = self._infer_difficulty(item.get('resume_contenu', ''), analysis)
            
            if 'duree_estimee' not in enriched_item:
                enriched_item['duree_estimee'] = self._estimate_duration(enriched_item)
            
            if 'objectif_lie' not in enriched_item:
                enriched_item['objectif_lie'] = self._match_objective(item, analysis['objectives'])
            
            enriched_data.append(enriched_item)
        
        return enriched_data
    
    def _infer_bloom_level(self, activity_type: str) -> str:
        """Infère le niveau de Bloom à partir du type d'activité"""
        if activity_type == 'text':
            return 'comprendre'
        elif activity_type == 'quiz':
            return 'appliquer'  # Par défaut, quiz d'application
        elif activity_type == 'accordion':
            return 'analyser'   # Souvent pour comparaisons/analyses
        elif activity_type == 'video':
            return 'comprendre'
        elif activity_type == 'image':
            return 'comprendre'
        elif activity_type == 'flash-card':
            return 'se_souvenir'
        else:
            return 'comprendre'
    
    def _infer_difficulty(self, content: str, analysis: Dict[str, Any]) -> str:
        """Infère le niveau de difficulté à partir du contenu"""
        content_lower = content.lower()
        
        # Chercher des correspondances avec les objectifs analysés
        for objective_text, difficulty_info in analysis.get('difficulty_mapping', {}).items():
            if any(word in content_lower for word in objective_text.lower().split()[:3]):
                niveau = difficulty_info.get('niveau', 2)
                if niveau == 2:
                    return 'facile'
                elif niveau == 3:
                    return 'moyen'
                elif niveau == 4:
                    return 'difficile'
        
        # Par défaut selon des mots-clés
        if any(word in content_lower for word in ['introduction', 'découverte', 'présentation']):
            return 'facile'
        elif any(word in content_lower for word in ['analyse', 'application', 'exercice']):
            return 'moyen'
        elif any(word in content_lower for word in ['évaluation', 'création', 'projet']):
            return 'difficile'
        
        return 'moyen'
    
    def _estimate_duration(self, item: Dict[str, str]) -> int:
        """Estime la durée d'un écran selon sa difficulté et son type"""
        difficulty = item.get('difficulte', 'moyen')
        activity_type = item.get('type_activite', 'text')
        
        # Durée de base selon le type d'activité
        base_durations = {
            'text': 3,
            'quiz': 5,
            'accordion': 4,
            'video': 6,
            'image': 2,
            'flash-card': 3
        }
        
        base_duration = base_durations.get(activity_type, 4)
        
        # Ajustement selon la difficulté
        difficulty_multipliers = {
            'facile': 0.8,
            'moyen': 1.0,
            'difficile': 1.4
        }
        
        multiplier = difficulty_multipliers.get(difficulty, 1.0)
        final_duration = int(base_duration * multiplier)
        
        return max(2, final_duration)  # Minimum 2 minutes
    
    def _match_objective(self, item: Dict[str, str], objectives: List[Dict[str, str]]) -> str:
        """Trouve l'objectif le plus pertinent pour cet écran"""
        content = (item.get('titre_ecran', '') + ' ' + item.get('resume_contenu', '')).lower()
        
        best_match = ""
        best_score = 0
        
        for obj in objectives:
            objective_text = obj.get('objectif', '').lower()
            
            # Compter les mots communs
            content_words = set(content.split())
            objective_words = set(objective_text.split())
            common_words = content_words.intersection(objective_words)
            
            score = len(common_words)
            if score > best_score:
                best_score = score
                best_match = obj.get('objectif', '')
        
        return best_match[:100] + "..." if len(best_match) > 100 else best_match
    
    def validate_sequencer_data(self, data: List[Dict[str, str]]) -> bool:
        """Valide la structure des données du séquenceur"""
        required_fields = ['sequence', 'num_ecran', 'titre_ecran', 'resume_contenu', 'type_activite']
        
        for item in data:
            for field in required_fields:
                if field not in item or not item[field]:
                    st.warning(f"Champ manquant ou vide : {field}")
                    return False
        
        return True