import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px


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

def visualize_role(df):
    counts = df['Quel est votre poste actuel ? (Sélectionner dans la liste ou choisir "Autre")'].value_counts().reset_index()
    counts.columns = ['Role', 'Nombre']
    all_roles_df = pd.DataFrame({'Role': all_roles})
    counts = pd.merge(all_roles_df, counts, on="Role", how="left").fillna(0)  # Fill missing roles with 0
    counts["Nombre"] = counts["Nombre"].astype(int)  # Ensure integer count
    total_count = counts["Nombre"].sum()
    counts["Pourcentage"] = (counts["Nombre"] / total_count * 100).round(1) if total_count > 0 else 0
    legend_text = "ℹ️ Les Rôles : " 
    top_roles = counts[counts["Nombre"] == counts["Nombre"].max()]
    if len(top_roles) == 1:
        top_role = top_roles.iloc[0, 0]
        top_count = top_roles.iloc[0, 1]
        title = f"📊 La majorité des participants ont le rôle {top_role} avec \n {top_count} participants !" if total_count > 0 else "📊 Aucune donnée disponible"
    else:
        top_roles_list = ", ".join(top_roles["Role"].values)
        title = f"📊 Les rôles les plus fréquents sont {top_roles_list} avec \n {top_roles['Nombre'].sum()} participants au total !" if total_count > 0 else "📊 Aucune donnée disponible"
    fig = px.bar(
        counts, 
        x='Nombre', 
        y='Role', 
        title=title,
        text='Nombre', 
        color='Role',
        color_discrete_sequence=pastel_colors,  
        orientation='h'  
    )
    fig.update_traces(textposition='outside')
    fig.add_annotation(
        text=legend_text,
        showarrow=False,
        xref="paper", yref="paper",
        x=0.5, y=1.05,
        font=dict(size=11)
    )
    fig.write_html('static/images/Role_distribution.html')
    
    

all_experience_levels = ["0-1 an", "2-3 ans", "4-6 ans", "7-10 ans", "10 ans et plus"]
def visualize_experience(df):
    counts = df["Années d'expérience dans le domaine tech :  "].value_counts().reset_index()
    counts.columns = ['Expérience', 'Nombre']
    all_exp_df = pd.DataFrame({'Expérience': all_experience_levels})
    counts = pd.merge(all_exp_df, counts, on="Expérience", how="left").fillna(0)
    counts["Nombre"] = counts["Nombre"].astype(int)

    total_count = counts["Nombre"].sum()
    counts["Pourcentage"] = (counts["Nombre"] / total_count * 100).round(1) if total_count > 0 else 0

    legend_text = " "

    if total_count > 0:
        top_experience = counts.iloc[counts["Nombre"].idxmax(), 0]
        top_count = counts.iloc[counts["Nombre"].idxmax(), 1]
        title = f"💼 {top_count} professionnels ont {top_experience} ans d'expérience dans la tech ! 🚀"
    else:
        title = "💼 Aucune donnée disponible sur l'expérience."
    fig = px.pie(
        counts, 
        names='Expérience', 
        values='Nombre', 
        title=title,
        color_discrete_sequence=pastel_colors  
    )
    fig.update_traces(textposition='outside')
    fig.add_annotation(
        text=legend_text,
        showarrow=False,
        xref="paper", yref="paper",
        x=0.5, y=1.05,
        font=dict(size=12)
    )
    fig.write_html('static/images/experience_distribution.html')
    # print(counts)
    
    
    
all_seniority_levels = [
    "Stagiaire", "Junior", "Mid-Level", 
    "Senior", "Lead", "Manager", 
    "Directeur / Executive", "Autre :"
]

def visualize_seniorit(df):
    counts = df['Quel est votre niveau de séniorité ?'].value_counts().reset_index()
    counts.columns = ['Niveau de Séniorité', 'Nombre']
    all_seniority_df = pd.DataFrame({'Niveau de Séniorité': all_seniority_levels})
    counts = pd.merge(all_seniority_df, counts, on="Niveau de Séniorité", how="left").fillna(0)  # Fill missing roles with 0
    counts["Nombre"] = counts["Nombre"].astype(int)  # Ensure integer count
    
    total_count = counts["Nombre"].sum()
    counts["Pourcentage"] = (counts["Nombre"] / total_count * 100).round(1) if total_count > 0 else 0
    legend_text = "ℹ️ Niveaux de Séniorité : " 
    top_levels = counts[counts["Nombre"] == counts["Nombre"].max()]
    if len(top_levels) == 1:
        top_level = top_levels.iloc[0, 0]
        top_count = top_levels.iloc[0, 1]
        title = f"📊 La majorité des participants se situent au niveau {top_level} avec \n {top_count} participants !" if total_count > 0 else "📊 Aucune donnée disponible"
    else:
        top_levels_list = ", ".join(top_levels["Niveau de Séniorité"].values)
        title = f"📊 Les niveaux les plus fréquents sont {top_levels_list} avec \n {top_levels['Nombre'].sum()} participants au total !" if total_count > 0 else "📊 Aucune donnée disponible"
        fig = px.bar(
        counts, 
        x='Nombre', 
        y='Niveau de Séniorité', 
        title=title,
        text='Nombre', 
        color='Niveau de Séniorité',
        color_discrete_sequence=pastel_colors,  
        orientation='h'  
    )
    fig.update_traces(textposition='outside')
    fig.add_annotation(
        text=legend_text,
        showarrow=False,
        xref="paper", yref="paper",
        x=0.5, y=1.05,
        font=dict(size=12)
    )
    fig.write_html('static/images/seniority2_distribution.html')
    
    
    
    
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
    max_count = sector_counts['Nombre'].max()
    top_sectors = sector_counts[sector_counts['Nombre'] == max_count]
    
    if not top_sectors.empty and max_count > 0:
        if len(top_sectors) > 1:
            top_sector_names = ', '.join(top_sectors['Secteur'].tolist())
            title = f"📊 {max_count} participants travaillent dans les secteurs {top_sector_names}! ({round((max_count / total_responses) * 100, 2)}%)"
        else:
            title = f"📊 {max_count} participants travaillent dans le secteur \n {top_sectors.iloc[0, 0]}! ({round((max_count / total_responses) * 100, 2)}%)"
    else:
        title = "📊 Aucune donnée disponible sur les secteurs de travail."
    fig = px.bar(
        sector_counts,
        x='Secteur',
        y='Nombre',
        title=title,
        labels={'Secteur': 'Secteur', 'Nombre': 'Nombre de Participants'},
        color='Secteur',
        text=sector_counts['Pourcentage'].apply(lambda x: f"{x:.2f}%")
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        plot_bgcolor='#f5f7fd',
        paper_bgcolor='#f5f7fd',
        xaxis_title='Secteur',
        yaxis_title='Nombre de Participants',
        yaxis=dict(title_standoff=10),
        xaxis=dict(title_standoff=10)
    )
    fig.write_html('static/images/sector_distribution_2.html')

    
    
    
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