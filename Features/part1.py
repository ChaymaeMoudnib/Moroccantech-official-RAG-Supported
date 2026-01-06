import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import re
import numpy as np
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
import json

pastel_colors = [
    "#A7C7E7",  # Baby Blue
    "#FFC1CC",  # Baby Pink
    "#C5E1A5",  # Baby Green
    "#FFEB99",  # Baby Yellow
    "#FF9999",  # Baby Red
    "#D1B3FF",   # Baby Purple
    "#F7C6C7",  # Pastel Coral  
    "#FFDDC1",  # Pastel Peach  
    "#B5EAD7",  # Pastel Mint  
    "#E0BBE4",  # Pastel Lavender  
    "#FDCB9E",  # Pastel Orange  
    "#A2D2FF",  # Pastel Sky Blue  
    "#D4A5A5",  # Pastel Rose  
    "#BFD8D2",  # Pastel Teal  
    "#FFE4E1"
]

def visualize_gender(df):
    column_name = "Quel est votre genre ? "
    
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    
    gender_counts = df[column_name].value_counts().reset_index()
    gender_counts.columns = ['Genre', 'Nombre']
    all_genders = {'Homme': 0, 'Femme': 0}  
    existing_counts = dict(zip(gender_counts['Genre'], gender_counts['Nombre']))  
    all_genders.update(existing_counts)  
    gender_counts = pd.DataFrame(list(all_genders.items()), columns=['Genre', 'Nombre'])  
    chart_data = {
        'labels': gender_counts['Genre'].tolist(),
        'values': gender_counts['Nombre'].tolist(),
        'colors': [pastel_colors[0], pastel_colors[1]],
        'title': f"Parmi les participants, {all_genders['Femme']} étaient des femmes et {all_genders['Homme']} étaient des hommes 🎉"
    }
    with open('static/images/gender_distribution.json', 'w') as f:
        json.dump(chart_data, f)


# 📌 Age Distribution (Bar Chart)
def visualize_age(df):
    column_name = "Quelle est votre tranche d'âge ?"
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    
    age_counts = df[column_name].value_counts().reset_index()
    age_counts.columns = ['Tranche d\'âge', 'Nombre']
    
    all_ages = {"18-24 ans": 0, "25-34 ans": 0, "35-44 ans": 0, "45-54 ans": 0, "55 ans et plus": 0}
    existing_counts = dict(zip(age_counts['Tranche d\'âge'], age_counts['Nombre']))
    all_ages.update(existing_counts)
    
    age_counts = pd.DataFrame(list(all_ages.items()), columns=['Tranche d\'âge', 'Nombre'])
    total_responses = age_counts['Nombre'].sum()
    age_counts['Pourcentage'] = (age_counts['Nombre'] / total_responses) * 100
    
    age_counts_sorted = age_counts.sort_values(by='Nombre', ascending=False)
    most_common_age = age_counts_sorted.iloc[0]['Tranche d\'âge'] if not age_counts_sorted.empty else "Inconnu"
    most_common_count = age_counts_sorted.iloc[0]['Nombre'] if not age_counts_sorted.empty else 0
    age_data = {
        "age_groups": age_counts['Tranche d\'âge'].tolist(),
        "counts": age_counts['Nombre'].tolist(),
        "percentages": age_counts['Pourcentage'].round(1).tolist(),
        "colors": ["#FFD1DC", "#FFECB8", "#C1E1C1", "#B5D8EB", "#D8BFD8"],  # Pastel colors
        "title": f"📊 La majorité des participants ({most_common_count}) ont entre {most_common_age} ! 🕒"
    }
    with open('static/images/age_distribution.json', 'w') as f:
        json.dump(age_data, f)
    
    
def visualize_diploma(df):
    column_name = "Quel est votre plus haut niveau de diplôme ?  "
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    
    diploma_counts = df[column_name].value_counts().reset_index()
    diploma_counts.columns = ['Diplôme', 'Nombre']
    
    all_dip = {"Aucun diplôme": 0, "Bac+2": 0, "Bac+3": 0, "Bac+5": 0, "Doctorat (PhD)": 0, "Autre": 0}
    existing_counts = dict(zip(diploma_counts['Diplôme'], diploma_counts['Nombre']))
    all_dip.update(existing_counts)
    
    diploma_counts_df = pd.DataFrame(list(all_dip.items()), columns=['Diplôme', 'Nombre'])
    diploma_counts_df["Pourcentage"] = (diploma_counts_df["Nombre"] / diploma_counts_df["Nombre"].sum() * 100).round(1)
    
    most_common_diploma = diploma_counts_df.iloc[diploma_counts_df['Nombre'].idxmax()]['Diplôme']
    most_common_count = diploma_counts_df['Nombre'].max()
    
    diploma_data = {
        "labels": diploma_counts_df['Diplôme'].tolist(),
        "values": diploma_counts_df['Nombre'].tolist(),
        "percentages": diploma_counts_df['Pourcentage'].tolist(),
        "colors": ["#A7C7E7", "#FFC1CC", "#FFD1DC", "#FFECB8", "#C1E1C1", "#D8BFD8"],
        "title": f"🎓 {most_common_count} c'est le nombre de La majorité des participants qui ont le Diplôme {most_common_diploma} ! 📚"
    }
    
    with open('static/images/diploma_distribution.json', 'w') as f:
        json.dump(diploma_data, f)

def visualize_diploma2(df):
    column_name = "Avez-vous un diplôme en informatique ou dans un domaine connexe ?"
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    
    diploma_counts = df[column_name].value_counts().reset_index()
    diploma_counts.columns = ['Réponse', 'Nombre']
    diploma_counts["Pourcentage"] = (diploma_counts["Nombre"] / diploma_counts["Nombre"].sum() * 100).round(1)
    
    top_response = diploma_counts.iloc[0, 0]
    top_count = diploma_counts.iloc[0, 1]
    
    diploma2_data = {
        "labels": diploma_counts['Réponse'].tolist(),
        "values": diploma_counts['Nombre'].tolist(),
        "percentages": diploma_counts['Pourcentage'].tolist(),
        "colors": ["#FFD1DC", "#FFECB8"],
        "title": f"🎓 {top_count} participants ont un diplôme en informatique ou dans un domaine connexe : {top_response} ! 📚"
    }
    
    with open('static/images/diploma2_distribution.json', 'w') as f:
        json.dump(diploma2_data, f)
        
        

def visualize_diploma_clusters(df):
    diploma_column = "Si oui, veuillez préciser le diplôme ainsi que l'institut où vous l'avez obtenu (séparée par '',''')"
    highest_degree_column = "Quel est votre plus haut niveau de diplôme ?  "
    if diploma_column not in df.columns or highest_degree_column not in df.columns:
        raise ValueError("Required columns not found in DataFrame.")
    diploma_details = df[diploma_column].dropna()
    diploma_institution = diploma_details.str.rsplit(',', n=1, expand=True)
    diploma_institution.columns = ['Diplôme', 'Institut']
    diploma_institution['Institut'] = diploma_institution['Institut'].str.strip().str.title()
    diploma_institution = diploma_institution.dropna(subset=['Institut'])
    df_merged = df[[highest_degree_column]].join(diploma_institution)
    df_merged = df_merged.dropna(subset=['Institut'])  
    degree_mapping = {
        "Bac+2": "Bac+2",
        "Bac+3": "Licence",
        "Bac+5": "Master",
        "Doctorat (PhD)": "Doctorat",
        "Aucun diplôme": "Autre"
    }
    df_merged['Catégorie'] = df_merged[highest_degree_column].map(degree_mapping)
    df_hierarchy_counts = df_merged.groupby(['Institut', 'Catégorie', 'Diplôme']).size().reset_index(name='Nombre')
    fig = px.icicle(
        df_hierarchy_counts,
        path=['Institut', 'Catégorie', 'Diplôme'],  
        values='Nombre',
        title="📊 Clustering des Diplômes par Institution 🎓",
        color='Catégorie',
        color_discrete_sequence=px.colors.sequential.Blues[::-1],  
    )
    fig.write_html('static/images/cluster_diplomas.html')