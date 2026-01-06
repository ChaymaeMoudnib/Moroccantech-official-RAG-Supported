import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px


pastel_colors = [
    "#A7C7E7",
    "#FFC1CC",
    "#C5E1A5",
    "#FFEB99",
    "#FF9999",
    "#D1B3FF",
    "#F7C6C7",
    "#FFDDC1",
    "#B5EAD7",
    "#E0BBE4",
    "#FDCB9E",
    "#A2D2FF",
    "#D4A5A5",
    "#BFD8D2",
    "#FFE4E1",
    "#FF5733",
    "#C70039",
    "#900C3F",
    "#581845",
    "#FFC300",
    "#FF5733",
    "#DAF7A6",
    "#33FF57",
    "#28A745",
    "#138D75",
    "#1F618D",
    "#154360",
    "#8E44AD",
    "#D35400",
    "#E74C3C",
    "#3498DB",
    "#2ECC71",
    "#F39C12",
    "#9B59B6",
    "#E91E63"
]


def visualize_bonus_frequency_by_seniority(df):
    bonus_column = "  À quelle fréquence recevez-vous des primes ou des bonus ?  "
    seniority_column = "Quel est votre niveau de séniorité ?"
    if bonus_column not in df.columns or seniority_column not in df.columns:
        raise ValueError("One or both columns not found in DataFrame.")
    bonus_frequency_levels = [
        "Chaque année",
        "Chaque six mois",
        "Chaque 3 mois"
    ]
    bonus_by_seniority = df.groupby(seniority_column)[bonus_column].value_counts().unstack(fill_value=0)
    bonus_by_seniority = bonus_by_seniority.reindex(columns=bonus_frequency_levels, fill_value=0).reset_index()
    bonus_by_seniority_long = bonus_by_seniority.melt(
        id_vars=[seniority_column], var_name=bonus_column, value_name='Nombre'
    )
    bonus_by_seniority_long[bonus_column] = pd.Categorical(
        bonus_by_seniority_long[bonus_column], 
        categories=bonus_frequency_levels, 
        ordered=True
    )
    fig = px.bar(
        bonus_by_seniority_long,
        x=seniority_column,
        y='Nombre',
        color=bonus_column,
        title='Fréquence des primes par séniorité',
        labels={'Nombre': 'Nombre de répondants', seniority_column: 'Séniorité'},
        barmode='group',
        text_auto=True,  
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig.update_traces(textposition='outside')
    fig.write_html('static/images/bonuses_distribution.html')

def visualize_salary_satisfaction_by_gender(df):
    column_name = "  Êtes-vous satisfait de votre salaire actuel ?"
    gender_column = "Quel est votre genre ? "
    if column_name not in df.columns or gender_column not in df.columns:
        raise ValueError(f"Required columns not found in DataFrame.")
    salary_satisfaction_levels = [
        "Très insatisfait", "Insatisfait", "Neutre", "Satisfait", "Très satisfait"
    ]
    satisfaction_counts = df.groupby(gender_column)[column_name].value_counts().unstack(fill_value=0)
    satisfaction_counts = satisfaction_counts.reindex(columns=salary_satisfaction_levels, fill_value=0)
    satisfaction_counts = satisfaction_counts.reset_index()
    satisfaction_counts_melted = satisfaction_counts.melt(id_vars=[gender_column], 
                                                           var_name="Satisfaction", 
                                                           value_name="Count")
    satisfaction_counts_melted["Satisfaction"] = pd.Categorical(
        satisfaction_counts_melted["Satisfaction"], 
        categories=salary_satisfaction_levels, 
        ordered=True
    )
    title = "Satisfaction avec le salaire par genre"
    fig = px.bar(
        satisfaction_counts_melted,
        x=gender_column,
        y="Count",
        color="Satisfaction",
        barmode='group',
        title=title,
        labels={'Count': 'Nombre', 'Satisfaction': 'Niveau de satisfaction'},
        text_auto=True,
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig.update_traces(textposition='outside')
    fig.write_html('static/images/salary_satisfaction_by_gender.html')
