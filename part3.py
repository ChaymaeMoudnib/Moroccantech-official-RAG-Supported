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
