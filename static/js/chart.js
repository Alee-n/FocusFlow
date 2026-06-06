document.addEventListener("DOMContentLoaded", () => {

    const chartElement = document.getElementById("focusChart");

    if (!chartElement) {
        return;
    }

    const chartData = JSON.parse(
        chartElement.dataset.chart
    );

    if (chartData.length === 0) {
        return;
    }

    const labels = chartData.map(
        (_, index) => `Session ${index + 1}`
    );

    new Chart(chartElement, {

        type: "line",

        data: {

            labels: labels,

            datasets: [{

                label: "Focus Time (Minutes)",

                data: chartData,

                borderWidth: 3,

                tension: 0.3,

                fill: false
            }]
        },

        options: {

            responsive: true,

            maintainAspectRatio: false
        }
    });

});