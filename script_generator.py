import streamlit as st
import json
import pandas as pd
from datetime import datetime
from openai import OpenAI
from typing import Dict, List, Any
import io

# Configuration de la page
st.set_page_config(
    page_title="Générateur de Scripts Pédagogiques",
    page_icon="📝",
    layout="wide"
)

class ScriptGenerator:
    def __init__(self, api_key: str):
        """Initialise le générateur de scripts avec la clé API OpenAI"""
        self.client = OpenAI(api_key=api_key)
    
    def generate_script(self, activity_data: Dict, activity_type: str) -> str:
        """Génère un script pédagogique pour une activité spécifique"""
        
        # Prompts spécialisés par type d'activité
        prompts = {
            'text': self._get_text_prompt(),
            'quiz': self._get_quiz_prompt(),
            'accordion': self._get_accordion_prompt(),
            'video': self._get_video_prompt(),
            'image': self._get_image_prompt(),
            'flash-card': self._get_flashcard_prompt()
        }
        
        if activity_type not in prompts:
            return f"Type d'activité '{activity_type}' non supporté"
        
        # Préparation du contexte
        context = f"""
        ACTIVITÉ À SCRIPTER :
        
        Numéro d'écran : {activity_data.get('num_ecran', 'Non défini')}
        Titre : {activity_data.get('titre_ecran', 'Non défini')}
        Sous-titre : {activity_data.get('sous_titre', 'Non défini')}
        Contenu : {activity_data.get('resume_contenu', 'Non défini')}
        Niveau Bloom : {activity_data.get('niveau_bloom', 'Non défini')}
        Difficulté : {activity_data.get('difficulte', 'Non défini')}
        Durée : {activity_data.get('duree_estimee', 'Non défini')} minutes
        Objectif : {activity_data.get('objectif_lie', 'Non défini')}
        Commentaires : {activity_data.get('commentaire', 'Non défini')}
        Séquence : {activity_data.get('sequence', 'Non défini')}
        
        Générez le script pédagogique détaillé pour cette activité de type "{activity_type}".
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompts[activity_type]},
                    {"role": "user", "content": context}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Erreur lors de la génération : {str(e)}"
    
    def _get_text_prompt(self) -> str:
        return """
        Vous êtes un expert en rédaction pédagogique. Votre mission : créer un script de contenu textuel structuré et engageant.

        GÉNÉREZ UN SCRIPT TEXTUEL avec :
        1. Un titre accrocheur
        2. Une introduction captivante (2-3 phrases)
        3. Le contenu principal organisé en sections claires
        4. Des exemples concrets et pertinents
        5. Des éléments de mise en forme (gras, italique, listes)
        6. Une conclusion avec points clés à retenir
        7. Une transition vers la suite

        ADAPTEZ selon la difficulté :
        - Facile : langage simple, exemples de base
        - Moyen : vocabulaire technique modéré
        - Difficile : terminologie spécialisée, concepts avancés

        FORMAT : Script en texte formaté, prêt à intégrer dans un outil de formation.
        """
    
    def _get_quiz_prompt(self) -> str:
        return """
        Vous êtes un expert en évaluation pédagogique. Votre mission : créer un script de quiz interactif.

        GÉNÉREZ UN SCRIPT DE QUIZ avec :
        1. Instructions claires pour l'apprenant
        2. 3-8 questions selon la durée (environ 2 min par question)
        3. Questions adaptées au niveau de Bloom spécifié
        4. Options de réponses plausibles
        5. Bonnes réponses avec explications
        6. Feedbacks constructifs pour les mauvaises réponses
        7. Score et bilan final

        TYPES DE QUESTIONS selon Bloom :
        - Comprendre : QCM de définition, vrai/faux
        - Appliquer : Questions de mise en situation
        - Analyser : Questions de comparaison, analyse de cas
        - Évaluer : Questions d'argumentation, critiques

        FORMAT : Script détaillé avec questions, réponses et feedbacks.
        """
    
    def _get_accordion_prompt(self) -> str:
        return """
        Vous êtes un expert en structuration d'informations. Votre mission : créer un script d'accordion pédagogique.

        GÉNÉREZ UN SCRIPT D'ACCORDION avec :
        1. Introduction générale du contenu
        2. 4-8 sections dépliables selon la durée
        3. Titres de sections engageants (fermés)
        4. Contenu détaillé pour chaque section (ouvert)
        5. Progression logique entre les sections
        6. Éléments visuels suggérés (images, schémas)
        7. Interactions recommandées (clic, survol)

        USAGES selon Bloom :
        - Comprendre : Définitions expandables, explications détaillées
        - Analyser : Comparaisons structurées, décompositions
        - Évaluer : Critères d'évaluation, grilles d'analyse

        FORMAT : Script avec sections titrées et contenu détaillé pour chaque partie.
        """
    
    def _get_video_prompt(self) -> str:
        return """
        Vous êtes un expert en scénarisation vidéo éducative. Votre mission : créer un script vidéo pédagogique.

        GÉNÉREZ UN SCRIPT VIDÉO avec :
        1. Synopsis et objectif de la vidéo
        2. Structure temporelle (intro 10%, développement 70%, conclusion 20%)
        3. Texte de narration (voix off)
        4. Descriptions des éléments visuels
        5. Animations et transitions suggérées
        6. Moments d'interaction ou de pause
        7. Ressources visuelles nécessaires

        STYLES selon difficulté :
        - Facile : narration simple, visuels clairs
        - Moyen : rythme modéré, animations explicatives
        - Difficile : contenu dense, schémas complexes

        FORMAT : Script détaillé avec timecodes, narration et indications visuelles.
        """
    
    def _get_image_prompt(self) -> str:
        return """
        Vous êtes un expert en design pédagogique visuel. Votre mission : créer un script d'image interactive.

        GÉNÉREZ UN SCRIPT D'IMAGE avec :
        1. Description générale de l'image principale
        2. Éléments visuels clés à inclure
        3. Zones interactives (cliquables, hover)
        4. Contenu des pop-ups/infobulles
        5. Légendes et annotations
        6. Palette de couleurs suggérée
        7. Style graphique recommandé

        TYPES selon Bloom :
        - Se souvenir : Schémas simples, illustrations mnémotechniques
        - Comprendre : Infographies, diagrammes explicatifs
        - Analyser : Cartes conceptuelles, comparaisons visuelles

        FORMAT : Script descriptif avec spécifications visuelles et interactions.
        """
    
    def _get_flashcard_prompt(self) -> str:
        return """
        Vous êtes un expert en mémorisation active. Votre mission : créer un script de flash-cards pédagogiques.

        GÉNÉREZ UN SCRIPT DE FLASH-CARDS avec :
        1. Introduction au jeu de cartes
        2. 8-20 cartes selon la durée (1-2 min par carte)
        3. Questions/termes au recto
        4. Réponses/définitions au verso
        5. Indices ou mnémotechniques
        6. Progression par difficulté
        7. Système de révision suggéré

        TYPES DE CARTES :
        - Concept ↔ Définition
        - Question ↔ Réponse
        - Terme ↔ Explication
        - Situation ↔ Solution

        FORMAT : Script avec cartes numérotées, recto/verso et conseils d'utilisation.
        """

def load_sequencer_json(uploaded_file) -> List[Dict]:
    """Charge le fichier JSON de séquenceur"""
    try:
        content = uploaded_file.read().decode('utf-8')
        return json.loads(content)
    except json.JSONDecodeError:
        st.error("Fichier JSON invalide")
        return []
    except Exception as e:
        st.error(f"Erreur lors du chargement : {str(e)}")
        return []

def main():
    st.title("📝 Générateur de Scripts Pédagogiques")
    st.markdown("*Générez des scripts détaillés à partir de votre séquenceur pédagogique*")
    st.markdown("---")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Clé API OpenAI
        api_key = st.text_input(
            "Clé API OpenAI",
            type="password",
            help="Votre clé API OpenAI pour générer les scripts"
        )
        
        # Validation de la clé API
        if api_key:
            if api_key.startswith('sk-') and len(api_key) > 20:
                st.success("✅ Clé API valide")
            else:
                st.error("❌ Format de clé API invalide")
                api_key = None
        
        st.markdown("---")
        
        # Informations
        with st.expander("ℹ️ Format JSON attendu"):
            st.markdown("""
            **Structure requise :**
            ```json
            [
              {
                "sequence": "Nom de la séquence",
                "num_ecran": "01-Intro-01",
                "titre_ecran": "Titre",
                "type_activite": "text|quiz|accordion|video|image|flash-card",
                "niveau_bloom": "Comprendre",
                "difficulte": "facile|moyen|difficile",
                "duree_estimee": 15,
                "objectif_lie": "Objectif pédagogique",
                "resume_contenu": "Description...",
                "commentaire": "Notes..."
              }
            ]
            ```
            """)
    
    # Interface principale
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Séquenceur d'Entrée")
        
        # Upload du fichier JSON
        uploaded_file = st.file_uploader(
            "Choisissez votre fichier de séquenceur JSON",
            type=['json'],
            help="Uploadez votre fichier JSON de séquenceur pédagogique"
        )
        
        if uploaded_file is not None:
            sequencer_data = load_sequencer_json(uploaded_file)
            
            if sequencer_data:
                st.success(f"✅ {len(sequencer_data)} activités chargées")
                
                # Analyse des types d'activités
                activity_types = {}
                for activity in sequencer_data:
                    act_type = activity.get('type_activite', 'inconnu')
                    activity_types[act_type] = activity_types.get(act_type, 0) + 1
                
                st.info(f"📊 Types détectés : {dict(activity_types)}")
                
                # Aperçu des données
                with st.expander("🔍 Aperçu du séquenceur"):
                    df = pd.DataFrame(sequencer_data)
                    st.dataframe(df[['num_ecran', 'titre_ecran', 'type_activite', 'duree_estimee']])
    
    with col2:
        st.header("📋 Génération de Scripts")
        
        if uploaded_file is not None and sequencer_data and api_key:
            
            # Sélection des activités à scripter
            st.subheader("🎯 Sélection des Activités")
            
            activity_options = []
            for i, activity in enumerate(sequencer_data):
                option_text = f"{activity.get('num_ecran', f'Act{i+1}')} - {activity.get('titre_ecran', 'Sans titre')} ({activity.get('type_activite', 'inconnu')})"
                activity_options.append(option_text)
            
            selected_activities = st.multiselect(
                "Choisissez les activités à scripter :",
                activity_options,
                default=activity_options[:3] if len(activity_options) >= 3 else activity_options
            )
            
            if st.button("🚀 Générer les Scripts", type="primary"):
                if selected_activities:
                    generator = ScriptGenerator(api_key)
                    
                    with st.spinner("🔄 Génération des scripts en cours..."):
                        scripts = {}
                        
                        progress_bar = st.progress(0)
                        for i, selected in enumerate(selected_activities):
                            # Trouver l'index de l'activité sélectionnée
                            activity_index = activity_options.index(selected)
                            activity = sequencer_data[activity_index]
                            
                            # Générer le script
                            script = generator.generate_script(
                                activity, 
                                activity.get('type_activite', 'text')
                            )
                            
                            script_id = f"{activity.get('num_ecran', f'Act{activity_index+1}')}_{activity.get('type_activite', 'unknown')}"
                            scripts[script_id] = {
                                'activite': activity,
                                'script': script
                            }
                            
                            progress_bar.progress((i + 1) / len(selected_activities))
                        
                        st.session_state.generated_scripts = scripts
                        st.success(f"✅ {len(scripts)} scripts générés avec succès !")
                else:
                    st.warning("⚠️ Veuillez sélectionner au moins une activité")
        
        elif not api_key:
            st.info("ℹ️ Veuillez saisir votre clé API OpenAI")
        elif not uploaded_file:
            st.info("ℹ️ Veuillez uploader un fichier de séquenceur")
    
    # Affichage des scripts générés
    if 'generated_scripts' in st.session_state:
        st.markdown("---")
        st.header("📄 Scripts Générés")
        
        scripts = st.session_state.generated_scripts
        
        # Onglets par script
        tab_names = list(scripts.keys())
        if tab_names:
            tabs = st.tabs(tab_names)
            
            for i, (script_id, script_data) in enumerate(scripts.items()):
                with tabs[i]:
                    activity = script_data['activite']
                    script_content = script_data['script']
                    
                    # Informations de l'activité
                    col_info1, col_info2, col_info3 = st.columns(3)
                    with col_info1:
                        st.metric("Type", activity.get('type_activite', 'N/A'))
                    with col_info2:
                        st.metric("Difficulté", activity.get('difficulte', 'N/A'))
                    with col_info3:
                        st.metric("Durée", f"{activity.get('duree_estimee', 'N/A')} min")
                    
                    # Script généré
                    st.subheader(f"📝 Script : {activity.get('titre_ecran', 'Sans titre')}")
                    st.markdown(script_content)
                    
                    # Bouton de téléchargement
                    st.download_button(
                        label=f"📥 Télécharger Script {script_id}",
                        data=script_content,
                        file_name=f"script_{script_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
        
        # Export global
        st.markdown("---")
        st.subheader("📦 Export Global")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            # Export tous les scripts en un fichier
            all_scripts_content = ""
            for script_id, script_data in scripts.items():
                activity = script_data['activite']
                all_scripts_content += f"""
# {script_id} - {activity.get('titre_ecran', 'Sans titre')}

**Type :** {activity.get('type_activite', 'N/A')}  
**Durée :** {activity.get('duree_estimee', 'N/A')} minutes  
**Difficulté :** {activity.get('difficulte', 'N/A')}  

{script_data['script']}

---

"""
            
            st.download_button(
                label="📥 Télécharger Tous les Scripts",
                data=all_scripts_content,
                file_name=f"tous_scripts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
        
        with col_export2:
            # Export en JSON structuré
            json_export = {
                "metadata": {
                    "date_generation": datetime.now().isoformat(),
                    "nombre_scripts": len(scripts),
                    "types_activites": list(set(script_data['activite'].get('type_activite') for script_data in scripts.values()))
                },
                "scripts": scripts
            }
            
            st.download_button(
                label="📥 Export JSON Structuré",
                data=json.dumps(json_export, indent=2, ensure_ascii=False),
                file_name=f"scripts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Bouton reset
        if st.button("🔄 Générer de Nouveaux Scripts"):
            del st.session_state.generated_scripts
            st.experimental_rerun()

if __name__ == "__main__":
    main()