import pandas as pd
import plotly.express as px
from flask import Blueprint ,redirect, url_for,request,jsonify


comp_bp=('compare',__name__)

role_col = 'Quel est votre poste actuel ? (Sélectionner dans la liste ou choisir "Autre")'.strip()
salary_col = 'Quel est votre salaire brut mensuel en dirhams (MAD) ?'.strip()
# @comp_bp.route('/compare_salary', methods=["POST"])
# def compare_salary(df):
#     role = request.form.get("role", "").strip()
#     user_salary = request.form.get("salary", "").strip()

#     # Validate user input
#     if not role or not user_salary.isdigit():
#         return jsonify({"error": "Veuillez fournir un poste valide et un salaire numérique. ⚠️"}), 400

#     user_salary = int(user_salary)

#     # Normalize role in DataFrame
#     df['normalized_role'] = df[role_col].str.strip().str.lower()
#     normalized_role = role.lower()

#     # Filter by role
#     filtered_df = df[df['normalized_role'] == normalized_role]

#     if filtered_df.empty:
#         return jsonify({
#             "error": f"Aucune donnée disponible pour le poste '{role}' spécifié. 😕 Essayez un autre intitulé de poste ou revenez plus tard ! 🚀"
#         }), 404

#     # Get the actual role name
#     actual_role = filtered_df[role_col].iloc[0]
    
#     # Salary statistics
#     avg_salary = filtered_df[salary_col].mean()
#     above_count = len(filtered_df[filtered_df[salary_col] > user_salary])
#     total_count = len(filtered_df)
#     percentage = (above_count / total_count) * 100 if total_count > 0 else 0  # Prevent division by zero

#     # Construct result message
#     if user_salary < avg_salary:
#         result_message = (
#             f"🚀 Ne vous découragez pas ! Votre salaire de {user_salary} MAD est **inférieur** à la moyenne pour le poste de '{actual_role}'. "
#             f"💡 Continuez à développer vos compétences et à explorer des opportunités ! 🌟"
#         )
#     elif user_salary > avg_salary:
#         result_message = (
#             f"🎉 Bravo ! Votre salaire de {user_salary} MAD est **supérieur** à la moyenne pour le poste de '{actual_role}'. "
#             f"🔥 Continuez sur cette lancée et visez encore plus haut ! 💪"
#         )
#     else:
#         result_message = (
#             f"⚖️ Votre salaire de {user_salary} MAD est **égal** à la moyenne pour le poste de '{actual_role}'. "
#             f"📊 Vous êtes bien positionné(e) dans le marché, mais il y a toujours de la place pour progresser ! 🚀"
#         )

#     result_message += f" 📈 Votre salaire est **au-dessus** de **{round(100 - percentage, 2)}%** des personnes avec le même poste. 💪"

#     # Generate salary distribution visualizations
#     chart1, chart2 = generate_salary_dis_visualizations(df, selected_role=actual_role, user_salary=user_salary)

#     return jsonify({
#         "result": result_message,
#         "chart1": chart1,  # Include visualization
#         "chart2": chart2   # Include visualization
#     })


# # Define pastel color palette
# pastel_colors = [
#     "#A7C7E7", "#FFC1CC", "#C5E1A5", "#FFEB99", "#FF9999", "#D1B3FF", "#F7C6C7", 
#     "#FFDDC1", "#B5EAD7", "#E0BBE4", "#FDCB9E", "#A2D2FF", "#D4A5A5", "#BFD8D2"
# ]
# def generate_salary_dis_visualizations(df, selected_role=None, user_salary=None):
#     salary_col = "Quel est votre salaire brut mensuel en dirhams (MAD) ?"
#     gender_col = "Quel est votre genre ? "
#     role_col = 'Quel est votre poste actuel ? (Sélectionner dans la liste ou choisir "Autre")'
    
#     df[salary_col] = pd.to_numeric(df[salary_col], errors='coerce')
    
#     bins = [-float('inf'), 5000, 10000, 15000, 20000, 30000, float('inf')]
#     labels = ["< 5 000", "5 000 - 10 000", "10 000 - 15 000", "15 000 - 20 000", "20 000 - 30 000", "> 30 000"]
    
#     df["Salary Range"] = pd.cut(df[salary_col], bins=bins, labels=labels, include_lowest=True)
    
#     if selected_role:
#         # Filter data for the selected role
#         role_df = df[df[role_col] == selected_role]
        
#         # 1. Salary Distribution for the Role with User's Salary Highlighted
#         role_salary_total = role_df.groupby("Salary Range").size().reset_index(name="count")
#         role_salary_fig = px.bar(
#             role_salary_total, x="Salary Range", y="count",
#             title=f"Salary Distribution for {selected_role}",
#             labels={"count": "Number of Participants", "Salary Range": "Salary Range (MAD)"},
#             color_discrete_sequence=["#A7C7E7"]
#         )
#         if user_salary is not None:
#             salary_interval = pd.cut([user_salary], bins=bins, labels=labels, include_lowest=True)[0]
#             user_count = role_salary_total[role_salary_total['Salary Range'] == salary_interval]['count'].values
#             if user_count.size > 0:
#                 role_salary_fig.add_scatter(
#                     x=[salary_interval],
#                     y=[user_count[0]],
#                     mode='markers',
#                     marker=dict(color='red', size=12, symbol='star'),
#                     name="Your Salary"
#                 )
#         role_salary_path = f'static/images/role_salary_distribution.html'
#         role_salary_fig.write_html(role_salary_path)
        
#         # 2. Gender Salary Comparison for the Role
#         gender_salary_df = role_df.groupby([gender_col, "Salary Range"]).size().reset_index(name="count")
#         gender_salary_df["Percentage"] = gender_salary_df.groupby("Salary Range")["count"].transform(lambda x: x / x.sum() * 100)
#         gender_salary_fig = px.line(
#             gender_salary_df, x="Salary Range", y="Percentage", color=gender_col,
#             title=f"Gender Salary Comparison for {selected_role}",
#             markers=True, line_shape="spline",
#             labels={"Percentage": "Percentage (%)", "Salary Range": "Salary Range (MAD)"},
#             color_discrete_map={"Male": "blue", "Female": "pink"}
#         )
#         gender_salary_path = f'static/images/role_gender_comparison.html'
#         gender_salary_fig.write_html('static/images/role_gender_comparison.html')
        
#         return role_salary_path, gender_salary_path
#     else:
#         # Generate general charts if no role is selected
#         salary_distribution_fig = px.histogram(
#             df, x="Salary Range", title="Overall Salary Distribution",
#             labels={"count": "Number of Participants"}, color_discrete_sequence=["#A7C7E7"]
#         )
#         salary_distribution_fig.write_html('static/images/salary_distribution.html')
        
#         gender_salary_df = df.groupby([gender_col, "Salary Range"], observed=True).size().reset_index(name="count")
#         gender_salary_df["Percentage"] = gender_salary_df.groupby("Salary Range", observed=True)["count"].transform(lambda x: x / x.sum() * 100)
#         gender_salary_fig = px.line(
#             gender_salary_df, x="Salary Range", y="Percentage", color=gender_col,
#             title="Gender Salary Comparison (All Roles)",
#             markers=True, line_shape="spline",
#             color_discrete_map={"Male": "blue", "Female": "pink"}
#         )
#         gender_salary_fig.write_html('static/images/gender_comparison.html')
        
#         return 'static/images/salary_distribution.html', 'static/images/gender_comparison.html'
