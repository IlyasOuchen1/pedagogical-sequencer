import openai
import streamlit as st
import json
from typing import Dict, List, Any

class PedagogicalSequencer:
    def __init__(self, api_key: str):
        """Initialise le générateur avec la clé API OpenAI"""
        self.client = openai.OpenAI(api_key=api_key)
        
    def generate_sequencer(self, input_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Génère un séquenceur pédagogique à partir des données d'entrée
        """
        prompt = self._create_prompt(input_data)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            # Parser la réponse pour extraire le JSON
            content = response.choices[0].message.content
            sequencer_data = self._parse_response(content)
            return sequencer_data
            
        except Exception as e:
            st.error(f"Erreur lors de la génération : {str(e)}")
            return []
    
    def _get_system_prompt(self) -> str:
        """Prompt système pour définir le rôle de l'IA"""
        return """
        Vous êtes un expert en ingénierie pédagogique spécialisé dans la conception de parcours d'apprentissage structurés.
        Votre mission est de créer un séquenceur pédagogique détaillé respectant :
        
        1. La progression taxonomique de Bloom (Se souvenir → Comprendre → Appliquer → Analyser → Évaluer → Créer)
        2. Les principes SMART des objectifs pédagogiques
        3. Une progression logique et cohérente
        4. Une variété des modalités pédagogiques
        
        RÈGLES DE GÉNÉRATION :
        - Commencez toujours par une séquence d'introduction
        - Organisez le contenu en 4-6 séquences principales
        - Numérotez les écrans : 01-Intro-01, 02-Seq01-01, 03-Seq01-02, etc.
        - Variez les types d'activités selon la taxonomie de Bloom
        - Incluez des points d'évaluation réguliers
        - Terminez par une séquence de conclusion/synthèse
        
        TYPES D'ACTIVITÉS À UTILISER :
        - Présentation animée (pour Se souvenir/Comprendre)
        - Question à choix multiple avec feedback (pour Comprendre)
        - Glisser-déposer avec feedback (pour Appliquer)
        - Simulation interactive (pour Appliquer/Analyser)
        - Étude de cas (pour Analyser)
        - Évaluation par pairs (pour Évaluer)
        - Projet créatif (pour Créer)
        - Dialogue interactif (pour tous niveaux)
        
        Vous devez retourner UNIQUEMENT un JSON valide contenant un array d'objets avec les champs :
        - sequence : Nom de la séquence pédagogique
        - num_ecran : Numérotation unique (format XX-SeqYY-ZZ)
        - titre_ecran : Titre principal
        - sous_titre : Sous-titre spécifique
        - resume_contenu : Description détaillée du contenu
        - type_activite : Modalité pédagogique et interaction
        - commentaire : Notes additionnelles (optionnel)
        """
    
    def _create_prompt(self, input_data: Dict[str, Any]) -> str:
        """Crée le prompt utilisateur à partir des données d'entrée"""
        return f"""
        Créez un séquenceur pédagogique structuré à partir des données suivantes :

        **DOMAINE D'EXPERTISE :** {input_data.get('domaine', 'Non spécifié')}

        **OBJECTIFS CLASSIFIÉS SELON BLOOM :**
        {json.dumps(input_data.get('classification_bloom', {}), indent=2, ensure_ascii=False)}

        **OBJECTIFS SMART :**
        {json.dumps(input_data.get('objectifs_smart', {}), indent=2, ensure_ascii=False)}

        **ÉVALUATION DE DIFFICULTÉ :**
        {json.dumps(input_data.get('evaluation_difficulte', {}), indent=2, ensure_ascii=False)}

        INSTRUCTIONS SPÉCIFIQUES :
        1. Organisez en 4-6 séquences principales avec progression logique
        2. Respectez la numérotation : 01-Intro-01, 02-Seq01-01, 03-Seq01-02, etc.
        3. Adaptez les types d'activités selon le niveau taxonomique de Bloom
        4. Intégrez la progression de difficulté spécifiée
        5. Assurez-vous que chaque objectif SMART soit couvert
        6. Prévoyez des évaluations formatives et sommatives
        7. Incluez des éléments de contextualisation au domaine

        STRUCTURE ATTENDUE :
        - Séquence Introduction (3-4 écrans)
        - Séquences principales de contenu (selon les objectifs)
        - Séquence d'application pratique
        - Séquence de conclusion/évaluation

        Retournez UNIQUEMENT le JSON sans texte d'accompagnement.
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
    
    def validate_sequencer_data(self, data: List[Dict[str, str]]) -> bool:
        """Valide la structure des données du séquenceur"""
        required_fields = ['sequence', 'num_ecran', 'titre_ecran', 'resume_contenu', 'type_activite']
        
        for item in data:
            for field in required_fields:
                if field not in item or not item[field]:
                    st.warning(f"Champ manquant ou vide : {field}")
                    return False
        
        return True