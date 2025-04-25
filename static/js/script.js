document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("set_steps").addEventListener("submit", function (event) {
        let stepsInput = document.getElementById("steps_per_revolution");
        let stepsValue = parseInt(stepsInput.value, 10);

        if (isNaN(stepsValue) || stepsValue < 0) {
            alert("Кількість кроків на оберт повинна бути додатнім числом!");
            event.preventDefault();
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("set_period").addEventListener("submit", function (event) {
        let periodInput = document.getElementById("period_per_revolution");
        let periodValue = parseInt(periodInput.value, 10);

        if (isNaN(periodValue) || periodValue < 0) {
            alert("Час проходу на хвилину повинен бути додатнім числом!");
            event.preventDefault();
        }
    });
});
    fetch('../config.json')
    .then(function (response) {
        if (!response.ok) {
            throw new Error("Failed to fetch JSON file");
        }
        return response.json();
    })
    .then(function (data) {
        const stepsPerRevolution = get_rev(data);
        const periodPerRevolution = get_period(data);

        console.log("Steps per revolution:", stepsPerRevolution);
        console.log("Period per revolution:", periodPerRevolution);

        document.getElementById('steps_per_revolution').placeholder = stepsPerRevolution || "Немає даних";
        document.getElementById('period_per_revolution').placeholder = periodPerRevolution || "Немає даних";
    })
    .catch(function (err) {
        console.error('Error fetching or processing data:', err);
    });




