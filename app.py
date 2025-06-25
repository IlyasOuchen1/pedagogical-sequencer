import streamlit as st
import json
import pandas as pd
from datetime import datetime
from pedagogical_sequencer_v2 import PedagogicalSequencerV2
from utils_v2 import load_json_file, create_sample_json, export_to_csv, validate_new_format_data

# Configuration de la page
st.set_page_config(
    page_title="Générateur de Séquenceur Pédagogique v2.0",
    page_icon="🎓",
    layout="wide"
)

def main():
    st.title("🎓 Générateur de Séquenceur Pédagogique v2.0")
    st.markdown("*Version spécialisée pour le nouveau format JSON d'analyse d'objectifs*")
    st.markdown("---")
    
    # Sidebar pour la configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Clé API OpenAI
        api_key = st.text_input(
            "Clé API OpenAI",
            type="password",
            help="Votre clé API OpenAI pour utiliser GPT-4o"
        )
        
        # Validation de la clé API
        if api_key:
            if api_key.startswith('sk-') and len(api_key) > 20:
                st.success("✅ Clé API valide")
            else:
                st.error("❌ Format de clé API invalide")
                api_key = None
        
        st.markdown("---")
        
        # Téléchargement du modèle JSON
        st.subheader("📄 Modèle JSON")
        sample_json = create_sample_json()
        
        st.download_button(
            label="📥 Télécharger modèle JSON",
            data=json.dumps(sample_json, indent=2, ensure_ascii=False),
            file_name="modele_analyse_objectifs.json",
            mime="application/json",
            help="Téléchargez ce modèle et adaptez-le à vos données d'analyse"
        )
        
        # Informations sur le format
        with st.expander("ℹ️ Format JSON attendu"):
            st.markdown("""
            **Structure requise :**
            - `classification` : Classification Bloom détaillée
            - `formatted_objectives` : Objectifs SMART formatés  
            - `difficulty_evaluation` : Évaluation des difficultés
            
            **Champs optionnels :**
            - `domaine` : Domaine d'expertise
            - `contexte` : Contexte pédagogique
            """)
    
    # Interface principale
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Analyse d'Objectifs")
        
        # Upload du fichier JSON
        uploaded_file = st.file_uploader(
            "Choisissez votre fichier d'analyse JSON",
            type=['json'],
            help="Uploadez votre fichier JSON d'analyse d'objectifs pédagogiques"
        )
        
        # Affichage des données si fichier uploadé
        if uploaded_file is not None:
            input_data = load_json_file(uploaded_file)
            
            if input_data:
                st.success("✅ Fichier JSON chargé avec succès")
                
                # Validation du format spécialisé
                is_valid, validation_errors, stats = validate_new_format_data(input_data)
                
                if validation_errors:
                    st.error("❌ Erreurs de format détectées :")
                    for error in validation_errors:
                        st.error(f"  • {error}")
                else:
                    st.success("✅ Format validé - Données prêtes pour la génération")
                    
                    # Affichage des statistiques
                    col_stat1, col_stat2, col_stat3 = st.columns(3)
                    with col_stat1:
                        st.metric("📊 Objectifs détectés", stats.get('objectives_count', 0))
                    with col_stat2:
                        st.metric("🎯 Niveaux Bloom", stats.get('bloom_levels', 0))
                    with col_stat3:
                        st.metric("📈 Niveaux difficulté", stats.get('difficulty_levels', 0))
                
                # Aperçu des données
                with st.expander("🔍 Aperçu des données"):
                    st.json(input_data)
            else:
                input_data = None
                is_valid = False
    
    with col2:
        st.header("📋 Séquenceur Généré")
        
        # Génération du séquenceur
        if st.button("🚀 Générer le Séquenceur", type="primary", disabled=not api_key):
            if uploaded_file is not None and input_data and is_valid:
                with st.spinner("🔄 Génération en cours..."):
                    sequencer = PedagogicalSequencerV2(api_key)
                    sequencer_data = sequencer.generate_sequencer(input_data)
                    
                    if sequencer_data:
                        st.session_state.sequencer_data = sequencer_data
                        st.success("✅ Séquenceur généré avec succès !")
                        
                        # Affichage des métriques de génération
                        generation_stats = analyze_generated_sequencer(sequencer_data)
                        col_gen1, col_gen2 = st.columns(2)
                        with col_gen1:
                            st.metric("⏱️ Durée estimée", f"{generation_stats['duration']} min")
                        with col_gen2:
                            st.metric("🎯 Couverture Bloom", f"{generation_stats['bloom_coverage']}%")
                    else:
                        st.error("❌ Erreur lors de la génération")
            else:
                if not api_key:
                    st.error("❌ Veuillez saisir votre clé API OpenAI")
                elif not uploaded_file:
                    st.error("❌ Veuillez uploader un fichier JSON")
                elif not is_valid:
                    st.error("❌ Fichier JSON invalide ou incomplet")
        
        if not api_key:
            st.info("ℹ️ Veuillez saisir votre clé API OpenAI dans la sidebar")
    
    # Affichage du séquenceur généré
    if 'sequencer_data' in st.session_state:
        st.markdown("---")
        st.header("📊 Séquenceur Pédagogique")
        
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
            'niveau_bloom': 'Niveau Bloom',
            'difficulte': 'Difficulté',
            'duree_estimee': 'Durée (min)',
            'commentaire': 'Commentaire'
        }
        
        df_display = df.rename(columns=column_mapping)
        
        # Affichage du tableau avec filtres
        st.subheader("📋 Vue d'ensemble")
        
        # Filtres
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        with col_filter1:
            sequences = ['Toutes'] + list(df['sequence'].dropna().unique())
            selected_sequence = st.selectbox("Filtrer par séquence", sequences)
        
        with col_filter2:
            bloom_levels = ['Tous'] + list(df['niveau_bloom'].dropna().unique())
            selected_bloom = st.selectbox("Filtrer par niveau Bloom", bloom_levels)
        
        with col_filter3:
            difficulty_levels = ['Toutes'] + list(df['difficulte'].dropna().unique())
            selected_difficulty = st.selectbox("Filtrer par difficulté", difficulty_levels)
        
        # Application des filtres
        filtered_df = df_display.copy()
        if selected_sequence != 'Toutes':
            filtered_df = filtered_df[filtered_df['Séquence'] == selected_sequence]
        if selected_bloom != 'Tous':
            filtered_df = filtered_df[filtered_df['Niveau Bloom'] == selected_bloom]
        if selected_difficulty != 'Toutes':
            filtered_df = filtered_df[filtered_df['Difficulté'] == selected_difficulty]
        
        # Affichage du tableau filtré
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=400
        )
        
        # Validation des types d'activités
        from utils_v2 import validate_activity_types, generate_activity_statistics
        
        activity_errors = validate_activity_types(sequencer_data)
        if activity_errors:
            st.warning("⚠️ Types d'activités non conformes détectés :")
            for error in activity_errors:
                st.error(f"  • {error}")
        else:
            st.success("✅ Tous les types d'activités sont conformes")
        
        # Statistiques détaillées
        st.subheader("📈 Statistiques du Séquenceur")
        
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
            total_duration = df['duree_estimee'].fillna(5).sum()
            st.metric("⏱️ Durée totale", f"{int(total_duration)} min")
        
        # Statistiques spécialisées des activités
        activity_stats = generate_activity_statistics(sequencer_data)
        
        st.subheader("📊 Analyse des Types d'Activités")
        
        col_activity1, col_activity2 = st.columns(2)
        
        with col_activity1:
            st.metric(
                "🎯 Conformité Recommandations", 
                f"{activity_stats['recommendations_compliance']:.1f}%",
                help="Pourcentage d'activités conformes aux recommandations Bloom/Difficulté"
            )
        
        with col_activity2:
            authorized_count = sum(1 for item in sequencer_data 
                                 if item.get('type_activite') in ['text', 'quiz', 'accordion', 'video', 'image', 'flash-card'])
            st.metric(
                "✅ Types Autorisés", 
                f"{authorized_count}/{len(sequencer_data)}",
                help="Nombre d'écrans utilisant les types d'activités autorisés"
            )
        
        # Graphiques de répartition améliorés
        st.subheader("📊 Répartitions Détaillées")
        
        col_chart1, col_chart2, col_chart3 = st.columns(3)
        
        with col_chart1:
            # Répartition par type d'activité
            activity_distribution = activity_stats['distribution']
            if activity_distribution:
                st.bar_chart(activity_distribution, use_container_width=True)
                st.caption("Répartition par type d'activité")
        
        with col_chart2:
            # Répartition par niveau Bloom
            bloom_counts = df['niveau_bloom'].value_counts()
            if not bloom_counts.empty:
                st.bar_chart(bloom_counts, use_container_width=True)
                st.caption("Répartition par niveau de Bloom")
        
        with col_chart3:
            # Répartition par difficulté
            difficulty_counts = df['difficulte'].value_counts()
            if not difficulty_counts.empty:
                st.bar_chart(difficulty_counts, use_container_width=True)
                st.caption("Répartition par niveau de difficulté")
        
        # Durée par type d'activité
        st.subheader("⏱️ Analyse Temporelle par Type d'Activité")
        
        duration_by_type = activity_stats['total_duration_by_type']
        if duration_by_type:
            duration_df = pd.DataFrame(list(duration_by_type.items()), columns=['Type d\'Activité', 'Durée Totale (min)'])
            st.bar_chart(duration_df.set_index('Type d\'Activité'))
        
        # Recommandations d'amélioration
        st.subheader("💡 Recommandations d'Amélioration")
        
        if activity_stats['recommendations_compliance'] < 80:
            st.warning("📈 La conformité aux recommandations peut être améliorée :")
            
            # Analyser les écrans non conformes
            non_compliant_screens = []
            for i, item in enumerate(sequencer_data):
                activity_type = item.get('type_activite', '')
                bloom_level = item.get('niveau_bloom', '')
                difficulty = item.get('difficulte', '')
                
                from utils_v2 import get_activity_recommendations
                recommended = get_activity_recommendations(bloom_level, difficulty)
                
                if activity_type not in recommended:
                    non_compliant_screens.append({
                        'ecran': item.get('num_ecran', f'Écran {i+1}'),
                        'actuel': activity_type,
                        'recommande': ', '.join(recommended),
                        'bloom': bloom_level,
                        'difficulte': difficulty
                    })
            
            if non_compliant_screens:
                st.write("**Écrans à optimiser :**")
                for screen in non_compliant_screens[:5]:  # Limiter à 5 exemples
                    st.write(f"• {screen['ecran']} : {screen['actuel']} → Recommandé : {screen['recommande']}")
        else:
            st.success("🎉 Excellente conformité aux recommandations pédagogiques !")
        
        # Types d'activités manquants
        used_types = set(activity_stats['distribution'].keys())
        all_types = {'text', 'quiz', 'accordion', 'video', 'image', 'flash-card'}
        missing_types = all_types - used_types
        
        if missing_types:
            st.info(f"💡 Types d'activités non utilisés : {', '.join(missing_types)}")
            st.write("Considérez l'ajout de ces types pour diversifier l'expérience d'apprentissage.")
        
        # Boutons d'export
        st.markdown("---")
        st.subheader("📥 Export du Séquenceur")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Export CSV
            csv_data = export_to_csv(sequencer_data)
            st.download_button(
                label="📥 CSV Standard",
                data=csv_data,
                file_name=f"sequenceur_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Export JSON
            json_data = json.dumps(sequencer_data, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 JSON Détaillé", 
                data=json_data,
                file_name=f"sequenceur_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col3:
            # Export pour LMS
            lms_data = export_for_lms(sequencer_data)
            st.download_button(
                label="📥 Format LMS",
                data=lms_data,
                file_name=f"sequenceur_lms_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col4:
            if st.button("🔄 Nouvelle Génération"):
                del st.session_state.sequencer_data
                st.experimental_rerun()

def analyze_generated_sequencer(sequencer_data):
    """Analyse le séquenceur généré pour fournir des statistiques"""
    total_duration = sum(item.get('duree_estimee', 5) for item in sequencer_data)
    
    # Calcul de la couverture Bloom
    bloom_levels_present = set()
    for item in sequencer_data:
        if item.get('niveau_bloom'):
            bloom_levels_present.add(item['niveau_bloom'])
    
    bloom_coverage = (len(bloom_levels_present) / 6) * 100  # 6 niveaux de Bloom
    
    return {
        'duration': total_duration,
        'bloom_coverage': int(bloom_coverage)
    }

def export_for_lms(sequencer_data):
    """Export spécialisé pour les plateformes LMS"""
    import io
    import csv
    
    output = io.StringIO()
    fieldnames = [
        'module', 'lesson', 'activity_type', 'title', 'description', 
        'bloom_level', 'difficulty', 'estimated_time', 'prerequisites'
    ]
    
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    
    for item in sequencer_data:
        writer.writerow({
            'module': item.get('sequence', ''),
            'lesson': item.get('num_ecran', ''),
            'activity_type': item.get('type_activite', ''),
            'title': item.get('titre_ecran', ''),
            'description': item.get('resume_contenu', ''),
            'bloom_level': item.get('niveau_bloom', ''),
            'difficulty': item.get('difficulte', ''),
            'estimated_time': item.get('duree_estimee', 5),
            'prerequisites': item.get('commentaire', '')
        })
    
    return output.getvalue()

if __name__ == "__main__":
    main()