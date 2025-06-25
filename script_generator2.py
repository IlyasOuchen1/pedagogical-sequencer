import streamlit as st
import json
import pandas as pd
from datetime import datetime
from openai import OpenAI
from typing import Dict, List, Any
import io

# Configuration de la page
st.set_page_config(
    page_title="Générateur de Prompts Pédagogiques",
    page_icon="🤖",
    layout="wide"
)

class PromptGenerator:
    def __init__(self, api_key: str):
        """Initialise le générateur de prompts avec la clé API OpenAI"""
        self.client = OpenAI(api_key=api_key)
    
    def generate_prompt(self, activity_data: Dict, activity_type: str) -> str:
        """Génère un prompt spécialisé pour une activité spécifique"""
        
        # Templates de prompts par type d'activité
        prompt_templates = {
            'text': self._get_text_prompt_template(),
            'quiz': self._get_quiz_prompt_template(),
            'accordion': self._get_accordion_prompt_template(),
            'video': self._get_video_prompt_template(),
            'image': self._get_image_prompt_template(),
            'flash-card': self._get_flashcard_prompt_template()
        }
        
        if activity_type not in prompt_templates:
            return f"Type d'activité '{activity_type}' non supporté"
        
        # Préparation du contexte pour la génération de prompt
        context = f"""
        DONNÉES DE L'ACTIVITÉ :
        
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
        
        Générez un PROMPT COMPLET et PRÊT À UTILISER pour créer cette activité de type "{activity_type}" dans un outil externe.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompt_templates[activity_type]},
                    {"role": "user", "content": context}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Erreur lors de la génération : {str(e)}"
    
    def _get_text_prompt_template(self) -> str:
        return """
        Vous êtes un expert en génération de prompts pour outils de création de contenu textuel.
        
        VOTRE MISSION : Générer un PROMPT COMPLET que l'utilisateur pourra copier-coller dans ChatGPT, Claude, ou tout autre outil IA pour créer automatiquement le contenu textuel pédagogique.
        
        LE PROMPT DOIT CONTENIR :
        1. Le rôle de l'IA (ex: "Tu es un expert en...")
        2. Le contexte et l'objectif pédagogique précis
        3. Les spécifications techniques (durée, niveau, difficulté)
        4. La structure exacte attendue
        5. Les critères de qualité
        6. Le format de sortie souhaité
        7. Les contraintes et adaptations
        
        GÉNÉREZ UN PROMPT COMME CELUI-CI :
        "Tu es un expert en rédaction pédagogique spécialisé en [domaine]. Crée un contenu textuel de [durée] minutes sur [sujet]...
        
        STRUCTURE ATTENDUE :
        - Titre accrocheur
        - Introduction (50 mots)
        - Corps principal (3 sections)
        - Conclusion avec points clés
        
        CRITÈRES :
        - Niveau de difficulté : [niveau]
        - Vocabulaire adapté à [public]
        - Exemples concrets inclus
        
        LIVRABLES : Texte formaté en markdown, prêt à intégrer."
        
        FORMAT DE SORTIE : UN PROMPT COMPLET PRÊT À COPIER-COLLER dans un outil IA.
        """
    
    def _get_quiz_prompt_template(self) -> str:
        return """
        Vous êtes un expert en génération de prompts pour outils de création de quiz.
        
        VOTRE MISSION : Générer un PROMPT COMPLET pour créer automatiquement un quiz pédagogique avec questions, réponses, et feedbacks.
        
        LE PROMPT DOIT SPÉCIFIER :
        1. Le rôle d'expert en évaluation pédagogique
        2. Le sujet et niveau de Bloom ciblé
        3. Le nombre de questions selon la durée
        4. Les types de questions adaptés
        5. La structure des feedbacks
        6. Le format de sortie (JSON, texte structuré)
        7. Les critères de difficulté
        
        EXEMPLE DE PROMPT À GÉNÉRER :
        "Tu es un expert en évaluation pédagogique. Crée un quiz de [X] questions sur [sujet] pour tester le niveau [Bloom]...
        
        SPÉCIFICATIONS :
        - Durée totale : [X] minutes
        - [X] questions QCM + [X] questions ouvertes
        - Difficulté : [niveau]
        - 4 options par QCM avec distracteurs plausibles
        
        POUR CHAQUE QUESTION :
        - Énoncé clair
        - Options de réponse
        - Bonne réponse avec explication
        - Feedback pour réponses incorrectes
        
        FORMAT : JSON structuré avec questions, réponses, feedbacks."
        
        GÉNÉREZ LE PROMPT COMPLET PRÊT À UTILISER.
        """
    
    def _get_accordion_prompt_template(self) -> str:
        return """
        Vous êtes un expert en génération de prompts pour outils de création d'accordéons interactifs.
        
        VOTRE MISSION : Générer un PROMPT COMPLET pour créer un accordion pédagogique avec sections dépliables organisées logiquement.
        
        LE PROMPT DOIT INCLURE :
        1. Le rôle d'expert en structuration d'informations
        2. Le contenu à organiser en sections
        3. La logique de progression pédagogique
        4. Les spécifications d'interactivité
        5. Le format de sortie structuré
        6. Les éléments visuels suggérés
        
        MODÈLE DE PROMPT :
        "Tu es un expert en design pédagogique interactif. Crée un accordion sur [sujet] avec [X] sections dépliables...
        
        STRUCTURE :
        - Introduction générale (visible)
        - [X] sections principales (titres visibles, contenu dépliable)
        - Progression logique du simple au complexe
        
        POUR CHAQUE SECTION :
        - Titre accrocheur (fermé)
        - Contenu détaillé (ouvert)
        - Éléments visuels suggérés
        - Temps de lecture estimé
        
        SPÉCIFICATIONS :
        - Durée totale : [X] minutes
        - Niveau : [difficulté]
        - Navigation : séquentielle/libre
        
        FORMAT : Structure JSON avec sections, titres, contenus."
        
        CRÉEZ LE PROMPT COMPLET POUR OUTIL EXTERNE.
        """
    
    def _get_video_prompt_template(self) -> str:
        return """
        Vous êtes un expert en génération de prompts pour outils de création vidéo pédagogique.
        
        VOTRE MISSION : Générer un PROMPT COMPLET pour créer un script vidéo avec narration, éléments visuels et timing.
        
        LE PROMPT DOIT CONTENIR :
        1. Le rôle de scénariste vidéo éducatif
        2. Les spécifications techniques (durée, style)
        3. La structure narrative (intro/développement/conclusion)
        4. Les descriptions d'éléments visuels
        5. Le texte de narration
        6. Les timecodes et transitions
        7. Les ressources nécessaires
        
        TEMPLATE DE PROMPT :
        "Tu es un scénariste vidéo spécialisé en contenu éducatif. Crée un script vidéo de [X] minutes sur [sujet]...
        
        STRUCTURE VIDÉO :
        - Introduction accrocheuse (10% du temps)
        - Développement en [X] parties (70%)
        - Conclusion synthétique (20%)
        
        POUR CHAQUE SÉQUENCE :
        - Timecode (début-fin)
        - Texte de narration
        - Description des visuels
        - Animations suggérées
        - Transitions
        
        SPÉCIFICATIONS :
        - Durée : [X] minutes
        - Style : [documentaire/explicatif/conversationnel]
        - Public : [niveau]
        - Rythme : adapté à la difficulté [niveau]
        
        LIVRABLES :
        - Script complet avec timecodes
        - Liste des ressources visuelles
        - Instructions de montage"
        
        GÉNÉREZ LE PROMPT PRÊT POUR OUTIL VIDÉO.
        """
    
    def _get_image_prompt_template(self) -> str:
        return """
        Vous êtes un expert en génération de prompts pour outils de création d'images pédagogiques interactives.
        
        VOTRE MISSION : Générer un PROMPT COMPLET pour créer une image/infographie interactive avec zones cliquables et annotations.
        
        LE PROMPT DOIT SPÉCIFIER :
        1. Le rôle de designer pédagogique visuel
        2. Le type d'image (schéma, carte, infographie, diagramme)
        3. Les éléments visuels principaux
        4. Les zones interactives
        5. Les styles graphiques
        6. Les spécifications techniques
        7. L'accessibilité et la lisibilité
        
        EXEMPLE DE PROMPT :
        "Tu es un designer pédagogique spécialisé en visualisation d'informations. Crée une [type d'image] interactive sur [sujet]...
        
        ÉLÉMENTS VISUELS :
        - Image principale : [description]
        - [X] zones interactives cliquables
        - Légendes et annotations
        - Palette de couleurs : [spécifications]
        
        INTERACTIVITÉ :
        - Zones cliquables avec pop-ups informatifs
        - Survol avec infobulles
        - Navigation entre éléments
        
        SPÉCIFICATIONS TECHNIQUES :
        - Résolution : 1920x1080
        - Style : [moderne/minimaliste/illustratif]
        - Accessibilité : contrastes élevés, texte lisible
        - Durée d'exploration : [X] minutes
        
        FORMAT DE SORTIE :
        - Fichier image principal
        - Coordonnées des zones interactives
        - Contenu des pop-ups
        - Guide d'utilisation"
        
        CRÉEZ LE PROMPT COMPLET POUR OUTIL GRAPHIQUE.
        """
    
    def _get_flashcard_prompt_template(self) -> str:
        return """
        Vous êtes un expert en génération de prompts pour outils de création de flash-cards pédagogiques.
        
        VOTRE MISSION : Générer un PROMPT COMPLET pour créer un jeu de flash-cards optimisé pour la mémorisation active.
        
        LE PROMPT DOIT INCLURE :
        1. Le rôle d'expert en mémorisation
        2. Le nombre de cartes selon la durée
        3. Les types d'associations (terme-définition, question-réponse)
        4. La progression par difficulté
        5. Le système de révision
        6. Le format de sortie
        7. Les principes de mémorisation
        
        MODÈLE DE PROMPT :
        "Tu es un expert en sciences cognitives et mémorisation active. Crée un jeu de [X] flash-cards sur [sujet]...
        
        SPÉCIFICATIONS :
        - [X] cartes pour [X] minutes d'utilisation
        - Types : [X]% définitions, [X]% questions, [X]% applications
        - Progression : du simple au complexe
        - Niveau : [difficulté]
        
        POUR CHAQUE CARTE :
        - RECTO : Question/terme/situation claire
        - VERSO : Réponse/définition/explication complète
        - Indices mnémotechniques si pertinent
        - Tags pour catégorisation
        
        PRINCIPES DE CONCEPTION :
        - Une information par carte
        - Questions précises
        - Réponses concises mais complètes
        - Exemples concrets inclus
        
        SYSTÈME DE RÉVISION :
        - Intervalle de répétition espacée
        - Algorithme de difficulté adaptative
        - Suivi des performances
        
        FORMAT : JSON avec cartes structurées recto/verso + métadonnées."
        
        GÉNÉREZ LE PROMPT COMPLET POUR OUTIL DE FLASHCARDS.
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
    st.title("🤖 Générateur de Prompts Pédagogiques")
    st.markdown("*Générez des prompts prêts à utiliser dans d'autres outils IA*")
    st.markdown("---")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Clé API OpenAI
        api_key = st.text_input(
            "Clé API OpenAI",
            type="password",
            help="Votre clé API OpenAI pour générer les prompts"
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
        with st.expander("ℹ️ À propos des prompts"):
            st.markdown("""
            **Output de cette app :**
            - Prompts **prêts à copier-coller**
            - Compatibles ChatGPT, Claude, Gemini
            - Spécialisés par type d'activité
            - Avec spécifications détaillées
            
            **Utilisation :**
            1. Générez vos prompts ici
            2. Copiez un prompt
            3. Collez dans votre outil IA préféré
            4. Obtenez le contenu pédagogique !
            """)
        
        with st.expander("📋 Types de prompts générés"):
            st.markdown("""
            - **text** → Prompt pour contenu textuel
            - **quiz** → Prompt pour quiz interactif
            - **accordion** → Prompt pour sections dépliables
            - **video** → Prompt pour script vidéo
            - **image** → Prompt pour visuel interactif
            - **flash-card** → Prompt pour cartes mémoire
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
        st.header("🤖 Génération de Prompts")
        
        if uploaded_file is not None and sequencer_data and api_key:
            
            # Sélection des activités
            st.subheader("🎯 Sélection des Activités")
            
            activity_options = []
            for i, activity in enumerate(sequencer_data):
                option_text = f"{activity.get('num_ecran', f'Act{i+1}')} - {activity.get('titre_ecran', 'Sans titre')} ({activity.get('type_activite', 'inconnu')})"
                activity_options.append(option_text)
            
            selected_activities = st.multiselect(
                "Choisissez les activités à prompter :",
                activity_options,
                default=activity_options[:3] if len(activity_options) >= 3 else activity_options
            )
            
            if st.button("🚀 Générer les Prompts", type="primary"):
                if selected_activities:
                    generator = PromptGenerator(api_key)
                    
                    with st.spinner("🔄 Génération des prompts en cours..."):
                        prompts = {}
                        
                        progress_bar = st.progress(0)
                        for i, selected in enumerate(selected_activities):
                            # Trouver l'index de l'activité sélectionnée
                            activity_index = activity_options.index(selected)
                            activity = sequencer_data[activity_index]
                            
                            # Générer le prompt
                            prompt = generator.generate_prompt(
                                activity, 
                                activity.get('type_activite', 'text')
                            )
                            
                            prompt_id = f"{activity.get('num_ecran', f'Act{activity_index+1}')}_{activity.get('type_activite', 'unknown')}"
                            prompts[prompt_id] = {
                                'activite': activity,
                                'prompt': prompt
                            }
                            
                            progress_bar.progress((i + 1) / len(selected_activities))
                        
                        st.session_state.generated_prompts = prompts
                        st.success(f"✅ {len(prompts)} prompts générés avec succès !")
                else:
                    st.warning("⚠️ Veuillez sélectionner au moins une activité")
        
        elif not api_key:
            st.info("ℹ️ Veuillez saisir votre clé API OpenAI")
        elif not uploaded_file:
            st.info("ℹ️ Veuillez uploader un fichier de séquenceur")
    
    # Affichage des prompts générés
    if 'generated_prompts' in st.session_state:
        st.markdown("---")
        st.header("🤖 Prompts Générés")
        
        prompts = st.session_state.generated_prompts
        
        # Onglets par prompt
        tab_names = list(prompts.keys())
        if tab_names:
            tabs = st.tabs(tab_names)
            
            for i, (prompt_id, prompt_data) in enumerate(prompts.items()):
                with tabs[i]:
                    activity = prompt_data['activite']
                    prompt_content = prompt_data['prompt']
                    
                    # Informations de l'activité
                    col_info1, col_info2, col_info3 = st.columns(3)
                    with col_info1:
                        st.metric("Type", activity.get('type_activite', 'N/A'))
                    with col_info2:
                        st.metric("Difficulté", activity.get('difficulte', 'N/A'))
                    with col_info3:
                        st.metric("Durée", f"{activity.get('duree_estimee', 'N/A')} min")
                    
                    # Prompt généré
                    st.subheader(f"🤖 Prompt : {activity.get('titre_ecran', 'Sans titre')}")
                    
                    # Zone de texte copiable
                    st.text_area(
                        "Prompt prêt à copier-coller :",
                        prompt_content,
                        height=300,
                        key=f"prompt_area_{i}"
                    )
                    
                    # Instructions d'utilisation
                    st.info("💡 **Utilisation :** Copiez ce prompt et collez-le dans ChatGPT, Claude, Gemini ou tout autre outil IA pour générer automatiquement le contenu pédagogique.")
                    
                    # Bouton de téléchargement
                    col_dl1, col_dl2 = st.columns(2)
                    with col_dl1:
                        st.download_button(
                            label=f"📥 Télécharger Prompt {prompt_id}",
                            data=prompt_content,
                            file_name=f"prompt_{prompt_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                    with col_dl2:
                        # Bouton pour copier dans le presse-papier (simulation)
                        if st.button(f"📋 Copier", key=f"copy_{i}"):
                            st.success("✅ Prompt copié ! (Utilisez Ctrl+A puis Ctrl+C dans la zone de texte)")
        
        # Export global
        st.markdown("---")
        st.subheader("📦 Export Global des Prompts")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            # Export tous les prompts en un fichier
            all_prompts_content = ""
            for prompt_id, prompt_data in prompts.items():
                activity = prompt_data['activite']
                all_prompts_content += f"""
# PROMPT {prompt_id} - {activity.get('titre_ecran', 'Sans titre')}

Type: {activity.get('type_activite', 'N/A')}
Durée: {activity.get('duree_estimee', 'N/A')} minutes
Difficulté: {activity.get('difficulte', 'N/A')}

## Prompt à copier-coller:

{prompt_data['prompt']}

{'='*80}

"""
            
            st.download_button(
                label="📥 Télécharger Tous les Prompts",
                data=all_prompts_content,
                file_name=f"tous_prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        with col_export2:
            # Export en JSON structuré
            json_export = {
                "metadata": {
                    "date_generation": datetime.now().isoformat(),
                    "nombre_prompts": len(prompts),
                    "types_activites": list(set(prompt_data['activite'].get('type_activite') for prompt_data in prompts.values())),
                    "usage": "Copiez-collez ces prompts dans ChatGPT, Claude, ou tout autre outil IA"
                },
                "prompts": {
                    prompt_id: {
                        "activite_info": prompt_data['activite'],
                        "prompt_ready_to_use": prompt_data['prompt']
                    }
                    for prompt_id, prompt_data in prompts.items()
                }
            }
            
            st.download_button(
                label="📥 Export JSON Structuré",
                data=json.dumps(json_export, indent=2, ensure_ascii=False),
                file_name=f"prompts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        # Bouton reset
        if st.button("🔄 Générer de Nouveaux Prompts"):
            del st.session_state.generated_prompts
            st.experimental_rerun()

if __name__ == "__main__":
    main()