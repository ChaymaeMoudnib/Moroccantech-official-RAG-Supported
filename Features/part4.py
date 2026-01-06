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

def visualize_company_name_sharing(df):
    column_name = "Souhaitez-vous partager le nom de votre entreprise ? (Facultatif )"
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    sharing_counts = df[column_name].dropna().astype(str).str.strip().replace("", "Inconnu")
    sharing_counts = sharing_counts.value_counts().reset_index()
    sharing_counts.columns = ["Nom de l'entreprise", "Nombre"]
    sharing_counts["Initial"] = sharing_counts["Nom de l'entreprise"].apply(lambda name: name[0].upper() if name else "?")
    clustered_counts = sharing_counts.groupby("Initial", as_index=False)["Nombre"].sum()
    total_responses = clustered_counts["Nombre"].sum()
    if total_responses > 0:
        clustered_counts["Pourcentage"] = (clustered_counts["Nombre"] / total_responses * 100).round(2)
    else:
        clustered_counts["Pourcentage"] = 0
    clustered_counts["Label"] = clustered_counts.apply(lambda row: f"{row['Initial']} ({row['Pourcentage']}%)", axis=1)
    title = f"📊 {total_responses} participants ont partagé le nom de leur entreprise.\n" if total_responses > 0 else "📊 Aucune donnée disponible"
    fig = px.icicle(
        clustered_counts,
        path=["Label"],
        values="Nombre",
        title=title,
        color="Nombre",
        color_continuous_scale=px.colors.sequential.Blues[::-1]
    )
    fig.update_layout(
        xaxis_title="Nom de l'entreprise",
        yaxis_title="Nombre",
        plot_bgcolor="#f5f7fd",
        paper_bgcolor="#f5f7fd"
    )
    fig.write_html("static/images/visualize_company_sharing.html")
    # fig.show()
    

all_languages = [
    "Python", "JavaScript", "TypeScript", "Java", 
    "C++", "Swift", "Kotlin", "R", "Ruby", 
    "Scala", "C", "MATLAB", "PHP", "C#", 
    "Node.js", "React.js", "HTML", "CSS", "Autre :"
]

def visualize_programming_languages(df):
    column_name = "Quels langages de programmation utilisez-vous le plus ? (Sélection multiple possible)"
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    lang_counts = df[column_name].str.split(',').explode().str.strip().value_counts().reset_index()
    lang_counts.columns = ['Langage', 'Nombre']
    all_languages_df = pd.DataFrame({'Langage': all_languages})
    lang_counts = pd.merge(all_languages_df, lang_counts, on='Langage', how='left').fillna(0)
    lang_counts['Nombre'] = lang_counts['Nombre'].astype(int)
    total_count = lang_counts['Nombre'].sum()
    lang_counts['Pourcentage'] = (lang_counts['Nombre'] / total_count * 100).round(1) if total_count > 0 else 0
    max_value = lang_counts['Nombre'].max()
    top_languages = lang_counts[lang_counts['Nombre'] == max_value]['Langage'].tolist()
    if total_count > 0:
        if len(top_languages) == 1:
            title = f"📊 {total_count} la plus des participants utilise {top_languages[0]} est le langage \n le plus utilisé."
        else:
            title = f"📊 {total_count} participants ont indiqué que les langages les plus utilisés sont \n: {','.join(top_languages)}."
    else:
        title = "📊 Aucune donnée disponible."
    fig = px.bar(
        lang_counts,
        x='Nombre',
        y='Langage',
        title=title,
        text='Nombre',
        color='Langage',
        color_discrete_sequence=px.colors.qualitative.Plotly,
        orientation='h'
    )
    fig.update_traces(textposition='outside')
    fig.write_html('static/images/programming_languages_distribution.html')

    
    
all_databases = [
    "MySQL", "Cassandra", "IBM Db2", 
    "Apache Hive", "MariaDB", "Oracle Database", 
    "SQLite", "MongoDB", "PostgreSQL"
]

def visualize_database_usage(df):
    column_name = "Quels base de données utilisez-vous le plus?  (Sélection multiple possible)"
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    db_counts = df[column_name].str.split(',').explode().str.strip().value_counts().reset_index()
    db_counts.columns = ['Base de données', 'Nombre']
    all_databases_df = pd.DataFrame({'Base de données': all_databases})
    db_counts = pd.merge(all_databases_df, db_counts, on='Base de données', how='left').fillna(0)
    db_counts['Nombre'] = db_counts['Nombre'].astype(int)
    total_count = db_counts['Nombre'].sum()
    db_counts['Pourcentage'] = (db_counts['Nombre'] / total_count * 100).round(1) if total_count > 0 else 0
    max_value = db_counts['Nombre'].max()
    top_databases = db_counts[db_counts['Nombre'] == max_value]['Base de données'].tolist()
    if total_count > 0:
        if len(top_databases) == 1:
            title = f"📊 {total_count} La majorite des participants utilise {top_databases[0]} \n comme leur base de données intiale."
        else:
            title = f"📊 {total_count} participants ont indiqué que les bases de données \n les plus utilisées sont : {', '.join(top_databases)}."
    else:
        title = "📊 Aucune donnée disponible."
    fig = px.bar(
        db_counts, 
        x='Nombre', 
        y='Base de données', 
        title=title,
        text='Nombre', 
        color='Base de données',
        color_discrete_sequence=px.colors.qualitative.Plotly,
        orientation='h'
    )    
    fig.update_traces(textposition='outside')
    fig.write_html('static/images/database_usage_distribution.html')
    
    
    
all_cloud_services = [
    "AWS", "GCP", "CloudFlare", "Azure", 
    "Firebase", "OCI", "Self-hosted", "Rien", "Autre :"
]

def visualize_cloud_services_usage(df):
    column_name = "Quels services cloud utilisez-vous le plus?  (Sélection multiple possible)"
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    cloud_counts = df[column_name].str.split(',').explode().str.strip().value_counts().reset_index()
    cloud_counts.columns = ['Service Cloud', 'Nombre']
    all_cloud_df = pd.DataFrame({'Service Cloud': all_cloud_services})
    cloud_counts = pd.merge(all_cloud_df, cloud_counts, on='Service Cloud', how='left').fillna(0)
    cloud_counts['Nombre'] = cloud_counts['Nombre'].astype(int)
    total_count = cloud_counts['Nombre'].sum()
    cloud_counts['Pourcentage'] = (cloud_counts['Nombre'] / total_count * 100).round(1) if total_count > 0 else 0
    max_value = cloud_counts['Nombre'].max()
    top_cloud_services = cloud_counts[cloud_counts['Nombre'] == max_value]['Service Cloud'].tolist()
    if total_count > 0:
        if len(top_cloud_services) == 1:
            title = f"📊 {total_count} participants ont indiqué que {top_cloud_services[0]} est \n le service cloud le plus utilisé."
        else:
            title = f"📊 {total_count} participants ont indiqué que les services cloud les plus utilisés sont \n : {', '.join(top_cloud_services)}."
    else:
        title = "📊 Aucune donnée disponible."
    fig = px.bar(
        cloud_counts, 
        x='Nombre', 
        y='Service Cloud', 
        title=title,
        text='Nombre', 
        color='Service Cloud',
        color_discrete_sequence=px.colors.qualitative.Plotly,
        orientation='h'
    )
    fig.update_traces(textposition='outside')
    fig.write_html('static/images/cloud_services_usage_distribution.html')
    
    
all_tools = [
    "Jira", "Figma", "Trello", "Notion", 
    "Rien", "Autre :"
]

def visualize_daily_work_tools(df):
    column_name = "Quels outils utilisez-vous dans votre travail quotidien ? (Sélection multiple possible)"
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    tool_counts = df[column_name].str.split(',').explode().str.strip().value_counts().reset_index()
    tool_counts.columns = ['Outil', 'Nombre']
    all_tools_df = pd.DataFrame({'Outil': all_tools})
    tool_counts = pd.merge(all_tools_df, tool_counts, on='Outil', how='left').fillna(0)
    tool_counts['Nombre'] = tool_counts['Nombre'].astype(int)
    total_count = tool_counts['Nombre'].sum()
    tool_counts['Pourcentage'] = (tool_counts['Nombre'] / total_count * 100).round(1) if total_count > 0 else 0
    max_value = tool_counts['Nombre'].max()
    top_tools = tool_counts[tool_counts['Nombre'] == max_value]['Outil'].tolist()
    if total_count > 0:
        if len(top_tools) == 1:
            title = f"📊 {total_count} participants ont indiqué que {top_tools[0]} est l'outil \n le plus utilisé quotidiennement."
        else:
            title = f"📊 {total_count} participants ont indiqué que les outils les plus utilisés sont \n : {', '.join(top_tools)}."
    else:
        title = "📊 Aucune donnée disponible."
    fig = px.bar(
        tool_counts, 
        x='Nombre', 
        y='Outil', 
        title=title,
        text='Nombre', 
        color='Outil',
        color_discrete_sequence=px.colors.qualitative.Plotly,
        orientation='h'
    )
    fig.update_traces(textposition='outside')
    fig.write_html('static/images/daily_work_tools_distribution.html')


all_certifications = [
    "Google Data Analytics", "AWS Certified Solutions Architect",
    "Microsoft Certified: Azure Fundamentals", "Certified Scrum Master (CSM)",
    "Cisco Certified Network Associate (CCNA)", "Oracle Certified Java Programmer (OCJP)",
    "Professional Data Engineer (Google Cloud)", "IBM Data Science Professional Certificate"
]

def visualize_certifications(df):
    column_name = "Quelles certifications possédez-vous ? (Sélection multiple possible)"
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")
    cert_counts = df[column_name].str.split(',').explode().str.strip().value_counts().reset_index()
    cert_counts.columns = ['Certification', 'Nombre']
    all_certifications_df = pd.DataFrame({'Certification': all_certifications})
    cert_counts = pd.merge(all_certifications_df, cert_counts, on='Certification', how='left').fillna(0)
    cert_counts['Nombre'] = cert_counts['Nombre'].astype(int)
    total_count = cert_counts['Nombre'].sum()
    cert_counts['Pourcentage'] = (cert_counts['Nombre'] / total_count * 100).round(1) if total_count > 0 else 0
    max_value = cert_counts['Nombre'].max()
    top_certs = cert_counts[cert_counts['Nombre'] == max_value]['Certification'].tolist()
    if total_count > 0:
        if len(top_certs) == 1:
            title = f"📊 {total_count} participants ont indiqué que {top_certs[0]} est la certification \n la plus détenue."
        else:
            title = f"📊 {total_count} participants ont indiqué que les certifications les plus détenues sont \n : {', '.join(top_certs)}."
    else:
        title = "📊 Aucune donnée disponible."
    fig = px.bar(
        cert_counts, 
        x='Nombre', 
        y='Certification', 
        title=title,
        text='Nombre', 
        color='Certification',
        color_discrete_sequence=px.colors.qualitative.Plotly,
        orientation='h'
    )
    fig.update_traces(textposition='outside')
    fig.write_html('static/images/certifications_distribution.html')