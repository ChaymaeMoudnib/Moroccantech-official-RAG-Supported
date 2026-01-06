document.addEventListener('DOMContentLoaded', function() {

    function fetchAndRenderChart(jsonPath, chartId, fallbackData, isPieChart = true) {
        fetch(jsonPath)
            .then(response => {
                if (!response.ok) throw new Error('Failed to fetch');
                return response.json();
            })
            .then(data => {
                console.log(`Data loaded for ${chartId}:`, data);
                renderChart(data, chartId, isPieChart);
            })
            .catch(error => {
                console.warn(`Using fallback data for ${chartId} due to:`, error);
                renderChart(fallbackData, chartId, isPieChart);
            });
    }

    function renderChart(data, chartId, isPieChart) {
        let trace;
        if (isPieChart) {
            trace = {
                labels: data.labels,
                values: data.values,
                type: 'pie',
                marker: { colors: data.colors },
                textposition: 'outside',
                hoverinfo: 'label+percent+value',
                textinfo: 'percent+value'
            };
        } else {
            trace = {
                x: data.age_groups || data.diplomas,
                y: data.percentages || data.counts,
                type: 'bar',
                marker: { color: data.colors },
                text: (data.percentages || data.counts).map(p => p.toFixed(1) + '%'),
                textposition: 'outside',
                hoverinfo: 'x+y',
            };
        }

        const layout = {
            title: data.title,
            plot_bgcolor: '#f5f7fd',
            paper_bgcolor: '#f5f7fd',
            margin: { t: 50, b: 50, l: 50, r: 50 }
        };

        Plotly.newPlot(chartId, [trace], layout);
    }

    function fetchAndRenderDiplomaClusterChart(jsonPath, chartId) {
        fetch(jsonPath)
            .then(response => {
                if (!response.ok) throw new Error('Failed to fetch');
                return response.json();
            })
            .then(data => {
                console.log(`Data loaded for ${chartId}:`, data);
                renderDiplomaClusterChart(data, chartId);
            })
            .catch(error => console.warn(`Failed to fetch diploma cluster data for ${chartId}:`, error));
    }

    function renderDiplomaClusterChart(data, chartId) {
        let trace = {
            type: "icicle",
            labels: data.labels,
            parents: data.parents,
            values: data.values,
            branchvalues: 'total',
            textinfo: "label+value",
            marker: { colors: data.colors }
        };

        const layout = {
            title: data.title,
            paper_bgcolor: '#f5f7fd',
            margin: { t: 50, b: 50, l: 50, r: 50 }
        };

        Plotly.newPlot(chartId, [trace], layout);
    }

    // Load Gender Distribution Chart
    fetchAndRenderChart(
        './static/images/gender_distribution.json',
        'genderChart',
        {
            labels: ["Homme", "Femme"],
            values: [1, 1],
            colors: ["#A7C7E7", "#FFC1CC"],
            title: "Parmi les participants, 1 étaient des femmes et 1 étaient des hommes 🎉"
        },
        true
    );

    // Load Age Distribution Chart
    fetchAndRenderChart(
        './static/images/age_distribution.json',
        'ageChart',
        {
            age_groups: ["18-24 ans", "25-34 ans", "35-44 ans", "45-54 ans", "55 ans et plus"],
            counts: [1, 1, 1, 1, 1],
            percentages: [20, 20, 20, 20, 20],
            colors: ["#A7C7E7", "#FFECB8", "#C1E1C1", "#B5D8EB", "#D8BFD8"],
            title: "📊 La majorité des participants (1) ont entre 18-24 ans ! 🕒"
        },
        false
    );

    // Load Diploma Distribution Chart
    fetchAndRenderChart(
        './static/images/diploma_distribution.json',
        'diplomaChart',
        {
            diplomas: ["Aucun diplôme", "Bac+2", "Bac+3", "Bac+5", "Doctorat (PhD)", "Autre"],
            counts: [1, 1, 1, 1, 1, 1],
            percentages: [16.7, 16.7, 16.7, 16.7, 16.7, 16.7],
            colors: ["#A7C7E7", "#20B2AA", "#778899", "#9370DB", "#FFD700", "#DC143C"],
            title: "🎓 Distribution des diplômes parmi les participants 📚"
        },
        false
    );

    // Load IT-Related Diploma Chart
    fetchAndRenderChart(
        './static/images/diploma2_distribution.json',
        'diploma2Chart',
        {
            labels: ["Oui", "Non"],
            values: [1, 1],
            colors: ["#A7C7E7", "#FF5722"],
            title: "🎓 Répartition des participants ayant un diplôme en informatique ou domaine connexe 📚"
        },
        true
    );


});
