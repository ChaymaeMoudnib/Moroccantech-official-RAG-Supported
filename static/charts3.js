document.addEventListener('DOMContentLoaded', function() {
    // Define pastel colors with blue and green first
    const pastelColors = [
        '#A7C7E7',  // Pastel blue
        '#B5EAD7',  // Pastel green
        '#FFDAC1',  // Pastel orange
        '#E2F0CB',  // Pastel lime
        '#C7CEEA',  // Pastel lavender
        '#FFB7B2',  // Pastel pink
        '#B5EAD7',  // Pastel green (duplicate)
        '#A7C7E7'   // Pastel blue (duplicate)
    ];

    // Define global data arrays
    const all_roles = [
        "Développeur Backend", "Développeur Frontend", "Développeur Fullstack",
        "Data Scientist", "Data Engineer", "DevOps", "Chef de projet IT",
        "Manager IT", "Analyste de données", "UX/UI Designer", "Cybersecurity",
        "Professeur", "Autre :"
    ];

    const all_experience_levels = ["0-1 an", "2-3 ans", "4-6 ans", "7-10 ans", "10 ans et plus"];

    const all_seniority_levels = [
        "Stagiaire", "Junior", "Mid-Level", 
        "Senior", "Lead", "Manager", 
        "Directeur / Executive", "Autre :"
    ];

    // Add CSS for loading spinner
    const style = document.createElement('style');
    style.textContent = `
        .chart-loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: #666;
        }
        .spinner {
            border: 4px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            border-top: 4px solid #3498db;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin-bottom: 10px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);

    // Show loading overlay
    function showLoading() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex'; // Show the loading overlay
        }
    }

    // Hide loading overlay
    function hideLoading() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none'; // Hide the loading overlay
        }
    }

    // Animation configuration
    const animationSettings = {
        animation: {
            duration: 1000,
            easing: 'cubic-in-out'
        },
        transition: {
            duration: 500
        }
    };

    // Enhanced chart rendering function
    function renderChart(data, chartId, isPieChart) {
        console.log(`Rendering chart for ${chartId}:`, data); // Debugging line
        let trace;
        const colors = isPieChart ? 
            pastelColors.slice(0, data.data.length) : 
            [pastelColors[0], pastelColors[1]].concat(pastelColors.slice(2));

        if (isPieChart) {
            trace = {
                labels: data.data.map(item => item[data.labels]), // Access correct labels
                values: data.data.map(item => item[data.values]), // Access correct values
                type: 'pie',
                marker: { colors: colors },
                textposition: 'outside',
                hoverinfo: 'label+percent+value',
                textinfo: 'percent+value',
                texttemplate: '%{label}<br>%{value} (%{percent})',
                hovertemplate: '%{label}<br>%{value} participants<br>%{percent}<extra></extra>',
                sort: false,
                ...animationSettings
            };
        } else {
            const isHorizontal = data.orientation === 'h';
            const xData = isHorizontal ? data.data.map(item => item.Nombre) : data.data.map(item => item[data.labels]);
            const yData = isHorizontal ? data.data.map(item => item[data.labels]) : data.data.map(item => item.Nombre);
            
            trace = {
                x: xData,
                y: yData,
                type: 'bar',
                orientation: data.orientation || 'v',
                marker: { 
                    color: colors,
                    line: {
                        color: '#ffffff',
                        width: 1
                    }
                },
                text: data.data.map(item => item.Pourcentage ? item.Pourcentage.toFixed(1) + '%' : item.Nombre),
                textposition: 'auto',
                hoverinfo: 'x+y',
                hovertemplate: isHorizontal ?
                    '%{y}<br>%{x} participants<extra></extra>' :
                    '%{x}<br>%{y} participants<extra></extra>',
                ...animationSettings
            };
        }

        const layout = {
            title: {
                text: data.title,
                font: {
                    size: 16,
                    family: 'Arial, sans-serif'
                },
                x: 0.05,
                y: 0.95
            },
            plot_bgcolor: '#f5f7fd',
            paper_bgcolor: '#f5f7fd',
            margin: { t: 100, b: 80, l: 80, r: 50 },
            xaxis: { 
                title: isPieChart ? undefined : (data.x_axis || ''),
                automargin: true
            },
            yaxis: { 
                title: isPieChart ? undefined : (data.y_axis || ''),
                automargin: true
            },
            hoverlabel: {
                bgcolor: '#fff',
                font: {
                    family: 'Arial, sans-serif',
                    size: 12
                }
            },
            uniformtext: {
                minsize: 10,
                mode: 'hide'
            },
            showlegend: isPieChart
        };

        const config = {
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: ['toImage', 'sendDataToCloud'],
            locale: 'fr'
        };

        Plotly.newPlot(chartId, [trace], layout, config)
            .then(() => {
                console.log(`Chart rendered: ${chartId}`); // Debug log
            })
            .catch(err => {
                console.error(`Error rendering chart ${chartId}:`, err); // Error log
            });

        hideLoading(); // Hide loading overlay after rendering
    }

    // Fetch and render chart with error handling
    function fetchAndRenderChart(jsonPath, chartId, fallbackData, isPieChart = true) {
        showLoading(); // Show loading overlay

        fetch(jsonPath)
            .then(response => {
                if (!response.ok) throw new Error('Failed to fetch');
                return response.json();
            })
            .then(data => {
                console.log(`Data loaded for ${chartId}:`, data); // Log data loaded
                renderChart(data, chartId, isPieChart);
            })
            .catch(error => {
                console.warn(`Using fallback data for ${chartId} due to:`, error);
                renderChart(fallbackData, chartId, isPieChart);
            })
            .finally(() => {
                hideLoading(); // Hide loading overlay whether successful or not
            });
    }

    // Responsive chart resizing
    window.addEventListener('resize', function() {
        const chartIds = ['roleChart', 'experienceChart', 'seniorityChart', 'sectorChart', 'sector2Chart'];
        chartIds.forEach(id => {
            const chart = document.getElementById(id);
            if (chart) {
                Plotly.Plots.resize(chart);
            }
        });
    });

    // Initialize all charts
    function initializeAllCharts() {
        // Role Distribution Chart
        fetchAndRenderChart(
            './static/images/Role_distribution.json',
            'roleChart',
            {
                title: "📊 Distribution des rôles",
                data: all_roles.map(role => ({ Role: role, Nombre: 0, Pourcentage: 0 })),
                chart_type: "bar",
                x_axis: "Nombre",
                y_axis: "Role",
                orientation: "h"
            },
            false
        );

        // Experience Distribution Chart
        fetchAndRenderChart(
            './static/images/experience_distribution.json',
            'experienceChart',
            {
                title: "💼 Années d'expérience",
                data: all_experience_levels.map(exp => ({ Expérience: exp, Nombre: 0, Pourcentage: 0 })),
                chart_type: "pie",
                labels: "Expérience",
                values: "Nombre"
            },
            true
        );

        // Seniority Distribution Chart
        fetchAndRenderChart(
            './static/images/seniority2_distribution.json',
            'seniorityChart',
            {
                title: "📊 Niveaux de séniorité",
                data: all_seniority_levels.map(level => ({ "Niveau de Séniorité": level, Nombre: 0, Pourcentage: 0 })),
                chart_type: "bar",
                x_axis: "Nombre",
                y_axis: "Niveau de Séniorité",
                orientation: "h"
            },
            false
        );

        // Sector Distribution Chart
        fetchAndRenderChart(
            './static/images/sector_distribution.json',
            'sectorChart',
            {
                title: "📊 Secteurs d'activité",
                data: [
                    { Secteur: 'Technologie', Nombre: 0, Pourcentage: 0 },
                    { Secteur: 'Finance', Nombre: 0, Pourcentage: 0 },
                    { Secteur: 'Santé', Nombre: 0, Pourcentage: 0 },
                    { Secteur: 'Commerce/Retail', Nombre: 0, Pourcentage: 0 },
                    { Secteur: 'Gouvernement', Nombre: 0, Pourcentage: 0 },
                    { Secteur: 'Autre', Nombre: 0, Pourcentage: 0 }
                ],
                chart_type: "pie",
                labels: "Secteur",
                values: "Pourcentage"
            },
            true
        );

        // Sector 2 Distribution Chart
        fetchAndRenderChart(
            './static/images/sector_distribution_2.json',
            'sector2Chart',
            {
                title: "📊 Types d'entreprises",
                data: [
                    { Secteur: 'Public', Nombre: 0, Pourcentage: 0 },
                    { Secteur: 'Privé', Nombre: 0, Pourcentage: 0 },
                    { Secteur: 'Semi-public', Nombre: 0, Pourcentage: 0 },
                    { Secteur: 'Freelance', Nombre: 0, Pourcentage: 0 }
                ],
                chart_type: "bar",
                x_axis: "Secteur",
                y_axis: "Nombre",
                text: "Pourcentage"
            },
            false
        );
    }

    // Initialize charts when DOM is fully loaded
    initializeAllCharts();
});
