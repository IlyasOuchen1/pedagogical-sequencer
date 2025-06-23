import streamlit as st
import json
import pandas as pd
from datetime import datetime
from pedagogical_sequencer import PedagogicalSequencer
from utils import load_json_file, create_sample_json, export_to_csv

# Configuration de la page
st.set_page_config(
    page_title="Générateur de Séquenceur Pédagogique",
    page_icon="🎓",
    layout="wide"
)

def main():
    st.title("🎓 Générateur de Séquenceur Pédagogique")
    st.markdown("---")
    
    # Sidebar pour la configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Clé API OpenAI
        api_key = st.text_input(
            "Clé API OpenAI",
            type="password",
            help="Votre clé API OpenAI pour utiliser GPT-4"
        )
        
        st.markdown("---")
        
        # Téléchargement du modèle JSON
        st.subheader("📄 Modèle JSON")
        sample_json = create_sample_json()
        
        st.download_button(
            label="📥 Télécharger modèle JSON",
            data=json.dumps(sample_json, indent=2, ensure_ascii=False),
            file_name="modele_sequenceur.json",
            mime="application/json",
            help="Téléchargez ce modèle et adaptez-le à vos besoins"
        )
    
    # Interface principale
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Données d'Entrée")
        
        # Upload du fichier JSON
        uploaded_file = st.file_uploader(
            "Choisissez votre fichier JSON",
            type=['json'],
            help="Uploadez votre fichier JSON contenant les objectifs pédagogiques"
        )
        
        # Affichage des données si fichier uploadé
        if uploaded_file is not None:
            input_data = load_json_file(uploaded_file)
            
            if input_data:
                st.success("✅ Fichier JSON chargé avec succès")
                
                # Aperçu des données
                with st.expander("🔍 Aperçu des données"):
                    st.json(input_data)
                
                # Validation des champs requis
                required_fields = ['domaine', 'classification_bloom', 'objectifs_smart', 'evaluation_difficulte']
                missing_fields = [field for field in required_fields if field not in input_data]
                
                if missing_fields:
                    st.warning(f"⚠️ Champs manquants : {', '.join(missing_fields)}")
                else:
                    st.success("✅ Tous les champs requis sont présents")
    
    with col2:
        st.header("📋 Séquenceur Généré")
        
        # Génération du séquenceur
        if st.button("🚀 Générer le Séquenceur", type="primary", disabled=not api_key):
            if uploaded_file is not None and input_data:
                with st.spinner("🔄 Génération en cours..."):
                    sequencer = PedagogicalSequencer(api_key)
                    sequencer_data = sequencer.generate_sequencer(input_data)
                    
                    if sequencer_data:
                        st.session_state.sequencer_data = sequencer_data
                        st.success("✅ Séquenceur généré avec succès !")
                    else:
                        st.error("❌ Erreur lors de la génération")
            else:
                st.error("❌ Veuillez d'abord uploader un fichier JSON valide")
        
        if not api_key:
            st.info("ℹ️ Veuillez saisir votre clé API OpenAI dans la sidebar")
    
    # Affichage du séquenceur généré
    if 'sequencer_data' in st.session_state:
        st.markdown("---")
        st.header("📊 Résultats")
        
        sequencer_data = st.session_state.sequencer_data
        
        # Conversion en DataFrame pour l'affichage
        df = pd.DataFrame(sequencer_data)
        
        # Renommage des colonnes pour l'affichage
        column_mapping = {
            'sequence': 'Séquence',
            'num_ecran': 'Num Écran',
            'titre_ecran': 'Titre Écran',
            'sous_titre': 'Sous-Titre',
            'resume_contenu': 'Résumé du Contenu',
            'type_activite': 'Type d\'Activité',
            'commentaire': 'Commentaire'
        }
        
        df_display = df.rename(columns=column_mapping)
        
        # Affichage du tableau
        st.dataframe(
            df_display,
            use_container_width=True,
            height=400
        )
        
        # Statistiques
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📱 Nombre d'écrans", len(sequencer_data))
        
        with col2:
            sequences = df['sequence'].dropna().unique()
            st.metric("📚 Nombre de séquences", len(sequences))
        
        with col3:
            activities = df['type_activite'].dropna().unique()
            st.metric("🎯 Types d'activités", len(activities))
        
        with col4:
            st.metric("⏱️ Temps estimé", f"{len(sequencer_data) * 3} min")
        
        # Boutons d'export
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Export CSV
            csv_data = export_to_csv(sequencer_data)
            st.download_button(
                label="📥 Exporter en CSV",
                data=csv_data,
                file_name=f"sequenceur_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Export JSON
            json_data = json.dumps(sequencer_data, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 Exporter en JSON",
                data=json_data,
                file_name=f"sequenceur_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col3:
            if st.button("🔄 Générer une nouvelle version"):
                del st.session_state.sequencer_data
                st.experimental_rerun()

if __name__ == "__main__":
    main()