import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
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
    "#FFE4E1" ,  # Pastel Blush  
    "#FF5733",  # Bright Red-Orange
    "#C70039",  # Deep Red
    "#900C3F",  # Dark Burgundy
    "#581845",  # Rich Purple
    "#FFC300",  # Vivid Yellow
    "#FF5733",  # Fiery Orange
    "#DAF7A6",  # Neon Green
    "#33FF57",  # Bright Lime
    "#28A745",  # Emerald Green
    "#138D75",  # Deep Teal
    "#1F618D",  # Royal Blue
    "#154360",  # Midnight Blue
    "#8E44AD",  # Amethyst Purple
    "#D35400",  # Deep Orange
    "#E74C3C",  # Strong Coral
    "#3498DB",  # Vibrant Sky Blue
    "#2ECC71",  # Fresh Green
    "#F39C12",  # Warm Amber
    "#9B59B6",  # Grape Purple
    "#E91E63"   # Hot Pink
]

all_roles = [
    "Développeur Backend", "Développeur Frontend", "Développeur Fullstack",
    "Data Scientist", "Data Engineer", "DevOps", "Chef de projet IT",
    "Manager IT", "Analyste de données", "UX/UI Designer", "Cybersecurity",
    "Professeur", "Autre :"
]

all_experience_levels = ["0-1 an", "2-3 ans", "4-6 ans", "7-10 ans", "10 ans et plus"]
    
all_seniority_levels = [
    "Stagiaire", "Junior", "Mid-Level", 
    "Senior", "Lead", "Manager", 
    "Directeur / Executive", "Autre :"
]

def visualize_role(df):
    counts = df['Quel est votre poste actuel ? (Sélectionner dans la liste ou choisir "Autre")'].value_counts().reset_index()
    counts.columns = ['Role', 'Nombre']
    total_count = counts['Nombre'].sum()
    counts['Pourcentage'] = (counts['Nombre'] / total_count * 100).round(1) if total_count > 0 else 0

    # Prepare data for JSON
    chart_data = {
        "title": f"📊 La majorité des participants ont le rôle {counts.iloc[0, 0]} avec {counts.iloc[0, 1]} participants !" if total_count > 0 else "📊 Aucune donnée disponible",
        "data": counts.to_dict(orient='records'),
        "chart_type": "bar",
        "x_axis": "Nombre",
        "y_axis": "Role",
        "orientation": "h"
    }
    with open('static/images/role_distribution.json', 'w') as f:
        json.dump(chart_data, f, indent=4)
        
        
        

def visualize_experience(df):
    counts = df["Années d'expérience dans le domaine tech :  "].value_counts().reset_index()
    counts.columns = ['Expérience', 'Nombre']
    all_exp_df = pd.DataFrame({'Expérience': all_experience_levels})
    counts = pd.merge(all_exp_df, counts, on="Expérience", how="left").fillna(0)
    counts["Nombre"] = counts["Nombre"].astype(int)
    total_count = counts["Nombre"].sum()
    counts["Pourcentage"] = (counts["Nombre"] / total_count * 100).round(1) if total_count > 0 else 0

    # Prepare data for JSON
    chart_data = {
        "title": f"💼 {counts.iloc[0, 1]} professionnels ont {counts.iloc[0, 0]} ans d'expérience dans la tech ! 🚀" if total_count > 0 else "💼 Aucune donnée disponible sur l'expérience.",
        "data": counts.to_dict(orient='records'),
        "chart_type": "pie",
        "labels": "Expérience",
        "values": "Nombre"
    }
    
    # Save as JSON
    with open('static/images/experience_distribution.json', 'w') as f:
        json.dump(chart_data, f, indent=4)
        
        
def visualize_seniorit(df):
    counts = df['Quel est votre niveau de séniorité ?'].value_counts().reset_index()
    counts.columns = ['Niveau de Séniorité', 'Nombre']
    all_seniority_df = pd.DataFrame({'Niveau de Séniorité': all_seniority_levels})
    counts = pd.merge(all_seniority_df, counts, on="Niveau de Séniorité", how="left").fillna(0)  
    counts["Nombre"] = counts["Nombre"].astype(int)  
    
    total_count = counts["Nombre"].sum()
    counts["Pourcentage"] = (counts["Nombre"] / total_count * 100).round(1) if total_count > 0 else 0

    chart_data = {
        "title": "📊 Répartition des niveaux de séniorité",
        "data": counts.to_dict(orient='records'),
        "chart_type": "bar",
        "x_axis": "Nombre",
        "y_axis": "Niveau de Séniorité",
        "orientation": "h"
    }
    
    with open('static/images/seniority_distribution.json', 'w') as f:
        json.dump(chart_data, f, indent=4)
    

def visualize_sector_2(df):
    column_name = "Dans quel secteur travaillez-vous 2 ? "
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    
    sector_counts = df[column_name].value_counts().reset_index()
    sector_counts.columns = ['Secteur', 'Nombre']
    
    all_sectors = {
        'Public': 0,
        'Prive': 0,
        'Semi-public': 0,
        'Freelance': 0
    }
    
    existing_counts = dict(zip(sector_counts['Secteur'], sector_counts['Nombre']))
    all_sectors.update(existing_counts)  
    
    sector_counts = pd.DataFrame(list(all_sectors.items()), columns=['Secteur', 'Nombre'])
    total_responses = sector_counts['Nombre'].sum()
    sector_counts['Pourcentage'] = (sector_counts['Nombre'] / total_responses) * 100 if total_responses > 0 else 0

    chart_data = {
        "title": "📊 Répartition des secteurs",
        "data": sector_counts.to_dict(orient='records'),
        "chart_type": "bar",
        "x_axis": "Nombre",
        "y_axis": "Secteur"
    }
    
    with open('static/images/sector_distribution.json', 'w') as f:
        json.dump(chart_data, f, indent=4)

def visualize_sectors(df):
    column_name = "  Dans quel secteur travaillez-vous ?  "
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    sector_counts = df[column_name].value_counts().reset_index()
    sector_counts.columns = ['Secteur', 'Nombre']
    all_sectors = {
        'Technologie': 0,
        'Finance': 0,
        'Santé': 0,
        'Commerce/Retail': 0,
        'Gouvernement': 0,
        'Autre': 0
    }
    existing_counts = dict(zip(sector_counts['Secteur'], sector_counts['Nombre']))
    all_sectors.update(existing_counts)  # Update the counts with existing data
    sector_counts = pd.DataFrame(list(all_sectors.items()), columns=['Secteur', 'Nombre'])
    total_responses = sector_counts['Nombre'].sum()
    sector_counts['Pourcentage'] = (sector_counts['Nombre'] / total_responses) * 100
    counts = sector_counts[sector_counts['Nombre'] > 0]
    if not counts.empty:
        title = f"📊 {counts.iloc[0, 1]} participants travaillent dans \n le secteur {counts.iloc[0, 0]} !"
    else:
        title = "📊 Aucune donnée disponible sur les secteurs de travail."
    fig = px.pie(
        sector_counts,
        values='Pourcentage',
        names='Secteur',
        color='Secteur',
        title=title,
        labels={'Secteur': 'Secteur', 'Nombre': 'Nombre'}
    )
    fig.update_layout(plot_bgcolor='#f5f7fd', paper_bgcolor='#f5f7fd')
    fig.update_traces(textposition='outside')
    fig.write_html('static/images/sector_distribution.html')

    
    
    
    
    
    
def visualize_company_type(df):
    column_name = "Travaillez-vous pour une entreprise locale ou internationale ?"
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    company_counts = df[column_name].value_counts().reset_index()
    company_counts.columns = ['Type', 'Nombre']
    all_types = {'Locale': 0, 'Internationale': 0}
    existing_counts = dict(zip(company_counts['Type'], company_counts['Nombre']))
    all_types.update(existing_counts)  # Update counts with existing data
    company_counts = pd.DataFrame(list(all_types.items()), columns=['Type', 'Nombre'])
    total_responses = company_counts['Nombre'].sum()
    if total_responses > 0:
        company_counts['Pourcentage'] = (company_counts['Nombre'] / total_responses) * 100
        title = f"🌍 {total_responses} professionnels évoluent dans une entreprise {company_counts.iloc[0, 0]}.\n Et vous ? 🏢"
    else:
        title = "🌍 Aucune donnée disponible sur le type d'entreprise."
    fig = px.pie(
        company_counts,
        values='Pourcentage',
        names='Type',
        color='Type',
        title=title,
        color_discrete_map={'Locale': 'lightblue', 'Internationale': 'lightgreen'},
        labels={'Type': 'Type', 'Nombre': 'Nombre'}
    )
    fig.update_layout(plot_bgcolor='#f5f7fd', paper_bgcolor='#f5f7fd')
    fig.update_traces(textposition='outside')
    fig.write_html('static/images/visualize_company_type.html')


def visualize_work_mode(df): 
    column_name = "Votre mode de travail :"
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    work_modes = ['En présentiel', 'Hybride', 'En distanciel']
    work_mode_counts = df[column_name].value_counts().reindex(work_modes, fill_value=0).reset_index()
    work_mode_counts.columns = ['Mode de Travail', 'Nombre']
    total_responses = work_mode_counts['Nombre'].sum()
    title = f"📊 {total_responses} participants ont choisi leur mode de travail."
    fig = px.pie(
        work_mode_counts,
        names='Mode de Travail',
        values='Nombre',
        title=title,
        color='Nombre',
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(plot_bgcolor='#f5f7fd', paper_bgcolor='#f5f7fd')
    fig.write_html('static/images/visualize_work_mode.html')
    

def visualize_company_size(df):
    column_name = "Quelle est la taille de votre entreprise ?"
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    size_counts = df[column_name].value_counts().reset_index()
    size_counts.columns = ['Taille', 'Nombre']
    all_sizes = {
        'Petite (1-50 employés)': 0,
        'Moyenne (51-500 employés)': 0,
        'Grande (501-5000 employés)': 0,
        'Très grande (+5000 employés)': 0
    }
    existing_counts = dict(zip(size_counts['Taille'], size_counts['Nombre']))
    all_sizes.update(existing_counts)
    size_counts = pd.DataFrame(list(all_sizes.items()), columns=['Taille', 'Nombre'])
    total_responses = size_counts['Nombre'].sum()
    if total_responses > 0:
        size_counts['Pourcentage'] = (size_counts['Nombre'] / total_responses) * 100
        title = f"🏢 {total_responses} participants travaillent dans une entreprise de taille \n {size_counts.iloc[0, 0]}."
    else:
        title = "🏢 Aucune donnée disponible sur la taille de l'entreprise."
    fig = px.pie(
        size_counts,
        values='Pourcentage',
        names='Taille',
        color='Taille',
        title=title,
        color_discrete_map={
            'Petite (1-50 employés)': 'lightblue',
            'Moyenne (51-500 employés)': 'lightgreen',
            'Grande (501-5000 employés)': 'lightcoral',
            'Très grande (+5000 employés)': 'lightsalmon'
        },
        labels={'Taille': 'Taille de l\'entreprise', 'Nombre': 'Nombre'}
    )
    fig.update_layout(plot_bgcolor='#f5f7fd', paper_bgcolor='#f5f7fd')
    fig.update_traces(textposition='outside')
    fig.write_html('static/images/visualize_company_size.html')
    
    
