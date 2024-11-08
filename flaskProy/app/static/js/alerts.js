// Fetch alerts from the backend
function loadAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(alerts => {
            const alertsList = document.getElementById('alerts-list');
            alertsList.innerHTML = '';

            alerts.forEach(alert => {
                const alertItem = document.createElement('li');
                alertItem.textContent = alert;
                alertItem.classList.add('alert-item');

                if (alert.includes("above")) {
                    alertItem.classList.add('alert-high');
                } else if (alert.includes("below")) {
                    alertItem.classList.add('alert-low');
                }

                alertsList.appendChild(alertItem);
            });
        });
}

function updateGauge(gaugeId, percentage) {
    const gauge = document.getElementById(gaugeId);
    const needle = gauge.querySelector('.needle');

    if (needle) {
        // Map the percentage to an angle between -90deg and 90deg
        const angle = (percentage / 100) * 180 - 90;
        needle.style.transform = `rotate(${angle}deg)`;
    } else {
        console.error(`Needle element not found in gauge: ${gaugeId}`);
    }
}

// Example usage:
// If 25% of sensors are over/under threshold, needle should point to 25%
updateGauge('sensor-gauge', 25);
updateGauge('memory-gauge', 50);



// Simulate data for now
function simulateGaugeData() {
    const inRangePercentage = 80; // Example value
    const memoryUsage = 50; // Placeholder for memory usage gauge

    updateGauge('sensor-gauge', inRangePercentage);
    updateGauge('memory-gauge', memoryUsage);
}

window.onload = function() {
    // Fetch alerts and update gauges after the page loads
    loadAlerts();
    simulateGaugeData(); // Initial gauge values
    setInterval(loadAlerts, 5000); // Refresh alerts every 5 seconds
    setInterval(simulateGaugeData, 5000); // Update gauges every 5 seconds
};

setInterval(() => {
    // Fetch data from your API or calculate values here
    const sensorPercentage = calculateSensorPercentage(); // Function to get the current sensor percentage
    const memoryPercentage = calculateMemoryPercentage(); // Function to get the current memory percentage

    // Update the gauges
    updateGauge('sensor-gauge', sensorPercentage);
    updateGauge('memory-gauge', memoryPercentage);
}, 5000);

