document.addEventListener('DOMContentLoaded', function() {
    function fetchAndRenderRoleChart(jsonPath) {
        fetch(jsonPath)
            .then(response => {
                if (!response.ok) throw new Error('Failed to fetch data');
                return response.json();
            })
            .then(data => {
                console.log('Data loaded for role chart:', data);
                renderRoleChart(data);
            })
            .catch(error => {
                console.warn('Error fetching role chart data: ${error}');
                renderRoleChart({ title: "📊 Aucune donnée disponible", data: [] });
            });
    }

    function renderRoleChart(data) {
        const colors = generateDistinctColors(all_roles.length); // Use all_roles for distinct colors
        const xValues = data.data.map(item => item.Nombre);
        const yValues = data.data.map(item => item.Role);
        const roleCounts = {};

        // Prepare role counts for legend
        all_roles.forEach(role => {
            roleCounts[role] = 0; // Initialize all roles to 0
        });

        // Update counts from fetched data
        data.data.forEach(item => {
            if (roleCounts[item.Role] !== undefined) {
                roleCounts[item.Role] = item.Nombre;
            }
        });

        const traces = all_roles.map((role, index) => {
            return {
                x: [roleCounts[role]], // Only show counts for that role
                y: [role],
                type: 'bar',
                orientation: 'h',
                text: [roleCounts[role]],
                textposition: 'outside',
                name: role, // Set legend name to the role
                marker: {
                    color: colors[index] // Assign distinct colors from generated colors
                },
                showlegend: true // Show legend
            };
        });

        const layout = {
            title: data.title,
            xaxis: { title: 'Nombre' },
            yaxis: { title: 'Rôle' },
            plot_bgcolor: '#f5f7fd',
            paper_bgcolor: '#f5f7fd',
            margin: { t: 50, b: 50, l: 50, r: 50 },
            barmode: 'stack', // Stack bars to show total per role
        };

        Plotly.newPlot('roleChart', traces, layout);
    }

    // Function to generate distinct colors
    function generateDistinctColors(numColors) {
        const colors = [];
        const baseColors = ['#A7C7E7', '#FFC1CC', '#C5E1A5', '#FFEB99', '#FF9999', '#D1B3FF', '#F7C6C7', '#FFDDC1', '#B5EAD7', '#E0BBE4', '#FDCB9E', '#A2D2FF', '#D4A5A5', '#BFD8D2', '#FFE4E1', '#FF5733', '#C70039', '#900C3F', '#581845', '#FFC300', '#FF5733', '#DAF7A6', '#33FF57', '#28A745', '#138D75', '#1F618D', '#154360', '#8E44AD', '#D35400', '#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6', '#E91E63'];
        for (let i = 0; i < numColors; i++) {
            colors.push(baseColors[i % baseColors.length]); // Cycle through base colors
        }
        return colors;
    }

    // Define the possible roles
    const all_roles = [
        "Développeur Backend", "Développeur Frontend", "Développeur Fullstack",
        "Data Scientist", "Data Engineer", "DevOps", "Chef de projet IT",
        "Manager IT", "Analyste de données", "UX/UI Designer", "Cybersecurity",
        "Professeur", "Autre :"
    ];

    // Load Role Distribution Chart
    fetchAndRenderRoleChart('./static/images/role_distribution.json');
});  