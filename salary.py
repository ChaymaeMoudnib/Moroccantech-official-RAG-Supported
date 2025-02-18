import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def visualize_salary_by_gender(df):
    gender_column = 'Quel est votre genre ? '
    salary_column = 'Quel est votre salaire brut mensuel en dirhams (MAD) ?'
    if gender_column not in df.columns or salary_column not in df.columns:
        raise ValueError(f"Required columns not found in DataFrame: '{gender_column}' or '{salary_column}'.")
    salary_bins = [0, 5000, 10000, 15000, 20000, 30000, np.inf]
    salary_labels = ["< 5 000", "5 000 - 10 000", "10 000 - 15 000", "15 000 - 20 000", "20 000 - 30 000", "> 30 000"]
    df['salary_numeric'] = pd.to_numeric(df[salary_column].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce')
    df = df.dropna(subset=['salary_numeric'])
    df['salary_category'] = pd.cut(df['salary_numeric'], bins=salary_bins, labels=salary_labels, right=False)
    salary_counts = df.groupby([gender_column, 'salary_category']).size().reset_index(name='count')
    total_per_category = salary_counts.groupby('salary_category')['count'].transform('sum')
    salary_counts['percentage'] = (salary_counts['count'] / total_per_category * 100).round(1)
    highest_paid_category = df.groupby(gender_column)['salary_numeric'].median().idxmax()
    title = f"📊 {len(df)} participants ont partagé leur salaire. Le genre le mieux rémunéré est {highest_paid_category}."
    fig = px.line(
        salary_counts, 
        x='salary_category', 
        y='percentage', 
        color=gender_column,
        title=title,
        markers=True,
        labels={'percentage': 'Pourcentage (%)', 'salary_category': 'Intervalle de Salaire', gender_column: 'Genre'},
        color_discrete_map={'Homme': 'blue', 'Femme': 'pink'}
    )
    fig.update_traces(line=dict(width=3))
    fig.update_layout(
        xaxis_title='Intervalle de Salaire',
        yaxis_title='Pourcentage (%)',
        plot_bgcolor='#f5f7fd',
        paper_bgcolor='#f5f7fd',
        legend_title='Genre'
    )
    fig.write_html('static/images/visualize_salary_by_gender.html')
    
    

def visualize_salary_by_role(df):
    role_column = 'Quel est votre poste actuel ? (Sélectionner dans la liste ou choisir "Autre")'
    salary_column = 'Quel est votre salaire brut mensuel en dirhams (MAD) ?'
    if role_column not in df.columns or salary_column not in df.columns:
        raise ValueError("Colonnes requises non trouvées dans le DataFrame.")
    df['salary_numeric'] = pd.to_numeric(df[salary_column], errors='coerce')
    salary_counts = df.groupby(role_column)[salary_column].value_counts().unstack(fill_value=0)
    median_salaries = df.groupby(role_column)['salary_numeric'].median()
    highest_paid_role = median_salaries.idxmax()
    highest_salary = median_salaries.max()
    total_responses = salary_counts.sum().sum()
    title = f"💰 Le poste le mieux payé est **{highest_paid_role}**, avec un salaire médian de **{highest_salary:,.0f} MAD** 💥 soit {round((highest_salary / median_salaries.median()) * 100, 1)}% de plus que la médiane !"
    fig = px.bar(
        salary_counts,
        title=title,
        color_discrete_sequence=px.colors.sequential.Plasma,
        barmode='stack'
    )
    fig.update_layout(
        xaxis_title="Poste",
        yaxis_title='Nombre de participants',
        plot_bgcolor='#f5f7fd',
        paper_bgcolor='#f5f7fd'
    )
    fig.write_html('static/images/visualize_salary_by_role.html')

def visualize_salary_by_age(df):
    age_column = "Quelle est votre tranche d'âge ?"
    salary_column = 'Quel est votre salaire brut mensuel en dirhams (MAD) ?'
    if age_column not in df.columns or salary_column not in df.columns:
        raise ValueError("Required columns not found in DataFrame.")
    salary_counts = df.groupby(age_column)[salary_column].value_counts().unstack(fill_value=0)
    total_responses = salary_counts.sum().sum()
    highest_paid_age = salary_counts.sum(axis=1).idxmax()
    highest_paid_percentage = (salary_counts.sum(axis=1).max() / total_responses) * 100 if total_responses > 0 else 0
    title = f"📊 {total_responses} participants ont partagé leur salaire par tranche d'âge.\n💰 La tranche d'âge la mieux payée est {highest_paid_age} avec {highest_paid_percentage:.2f}% des réponses." if total_responses > 0 else "📊 Aucune donnée disponible"
    fig = px.bar(
        salary_counts,
        title=title,
        color_discrete_sequence=px.colors.sequential.Plasma,
        barmode='stack'
    )
    fig.update_layout(
        xaxis_title="Tranche d'âge",
        yaxis_title='Nombre de participants',
        plot_bgcolor='#f5f7fd',
        paper_bgcolor='#f5f7fd'
    )
    fig.write_html('static/images/visualize_salary_by_age.html')

def visualize_salary_by_diploma(df):
    diploma_column = 'Quel est votre plus haut niveau de diplôme ?  '
    salary_column = 'Quel est votre salaire brut mensuel en dirhams (MAD) ?'
    if diploma_column not in df.columns or salary_column not in df.columns:
        raise ValueError("Required columns not found in DataFrame.")
    salary_counts = df.groupby(diploma_column)[salary_column].value_counts().unstack(fill_value=0)
    total_responses = salary_counts.sum().sum()
    highest_paid_diploma = salary_counts.sum(axis=1).idxmax()
    highest_paid_percentage = (salary_counts.sum(axis=1).max() / total_responses) * 100 if total_responses > 0 else 0
    title = f"📊 {total_responses} participants ont partagé leur salaire par niveau de diplôme.\n🎓 Le diplôme le mieux payé est {highest_paid_diploma} avec {highest_paid_percentage:.2f}% des réponses." if total_responses > 0 else "📊 Aucune donnée disponible"
    fig = px.bar(
        salary_counts,
        title=title,
        color_discrete_sequence=px.colors.sequential.Plasma,
        barmode='stack'
    )
    fig.update_layout(
        xaxis_title="Niveau de diplôme",
        yaxis_title='Nombre de participants',
        plot_bgcolor='#f5f7fd',
        paper_bgcolor='#f5f7fd'
    )
    fig.write_html('static/images/visualize_salary_by_diploma.html')

def visualize_salary_by_experience(df):
    experience_column = "Années d'expérience dans le domaine tech :  "
    salary_column = 'Quel est votre salaire brut mensuel en dirhams (MAD) ?'
    if experience_column not in df.columns or salary_column not in df.columns:
        raise ValueError("Required columns not found in DataFrame.")
    salary_counts = df.groupby(experience_column)[salary_column].value_counts().unstack(fill_value=0)
    total_responses = salary_counts.sum().sum()
    highest_paid_experience = salary_counts.sum(axis=1).idxmax()
    highest_paid_percentage = (salary_counts.sum(axis=1).max() / total_responses) * 100 if total_responses > 0 else 0
    title = f"📊 {total_responses} participants ont partagé leur salaire par années d'expérience.\n💼 L'expérience la mieux payée est {highest_paid_experience} avec {highest_paid_percentage:.2f}% des réponses." if total_responses > 0 else "📊 Aucune donnée disponible"
    fig = px.bar(
        salary_counts,
        title=title,
        color_discrete_sequence=px.colors.sequential.Plasma,
        barmode='stack'
    )
    fig.update_layout(
        xaxis_title="Années d'expérience",
        yaxis_title='Nombre de participants',
        plot_bgcolor='#f5f7fd',
        paper_bgcolor='#f5f7fd'
    )
    fig.write_html('static/images/visualize_salary_by_experience.html')



def visualize_salary_by_seniority(df):
    seniority_column = 'Quel est votre niveau de séniorité ?'
    salary_column = 'Quel est votre salaire brut mensuel en dirhams (MAD) ?'
    if seniority_column not in df.columns or salary_column not in df.columns:
        raise ValueError("Required columns not found in DataFrame.")
    salary_counts = df.groupby(seniority_column)[salary_column].value_counts().unstack(fill_value=0)
    total_responses = salary_counts.sum().sum()
    title = f"📊 {total_responses} participants ont partagé leur salaire par niveau de séniorité. 🎯 Le salaire médian des plus expérimentés est à {salary_counts.max().max():,.0f} MAD!" if total_responses > 0 else "📊 Aucune donnée disponible"
    fig = px.bar(
        salary_counts,
        title=title,
        color_discrete_sequence=px.colors.sequential.Plasma,
        barmode='stack'
    )
    fig.update_layout(
        xaxis_title="Niveau de séniorité",
        yaxis_title='Nombre de participants',
        plot_bgcolor='#f5f7fd',
        paper_bgcolor='#f5f7fd'
    )
    fig.write_html('static/images/visualize_salary_by_seniority.html')

def visualize_salary_by_work_mode(df):
    work_mode_column = 'Votre mode de travail :'
    salary_column = 'Quel est votre salaire brut mensuel en dirhams (MAD) ?'
    if work_mode_column not in df.columns or salary_column not in df.columns:
        raise ValueError("Required columns not found in DataFrame.")
    salary_counts = df.groupby(work_mode_column)[salary_column].value_counts().unstack(fill_value=0)
    total_responses = salary_counts.sum().sum()
    title = f"📊 {total_responses} participants ont partagé leur salaire par mode de travail. 🌍 Le télétravail offre un salaire moyen de **{salary_counts.max().max():,.0f} MAD**!" if total_responses > 0 else "📊 Aucune donnée disponible"
    fig = px.bar(
        salary_counts,
        title=title,
        color_discrete_sequence=px.colors.sequential.Plasma,
        barmode='stack'
    )
    fig.update_layout(
        xaxis_title="Mode de travail",
        yaxis_title='Nombre de participants',
        plot_bgcolor='#f5f7fd',
        paper_bgcolor='#f5f7fd'
    )
    fig.write_html('static/images/visualize_salary_by_work_mode.html')

def visualize_salary_by_company_type(df):
    company_type_column = 'Travaillez-vous pour une entreprise locale ou internationale ?'
    salary_column = 'Quel est votre salaire brut mensuel en dirhams (MAD) ?'
    if company_type_column not in df.columns or salary_column not in df.columns:
        raise ValueError("Required columns not found in DataFrame.")
    salary_counts = df.groupby(company_type_column)[salary_column].value_counts().unstack(fill_value=0)
    total_responses = salary_counts.sum().sum()
    title = f"📊 {total_responses} participants ont partagé leur salaire par type d'entreprise. 🌐 Les entreprises internationales offrent des salaires moyens de **{salary_counts.max().max():,.0f} MAD**!" if total_responses > 0 else "📊 Aucune donnée disponible"
    fig = px.bar(
        salary_counts,
        title=title,
        color_discrete_sequence=px.colors.sequential.Plasma,
        barmode='stack'
    )
    fig.update_layout(
        xaxis_title="Type d'entreprise",
        yaxis_title='Nombre de participants',
        plot_bgcolor='#f5f7fd',
        paper_bgcolor='#f5f7fd'
    )
    fig.write_html('static/images/visualize_salary_by_company_type.html')