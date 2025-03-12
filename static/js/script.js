function setSteps() {
    var steps = document.getElementById("steps_per_revolution").value;
    if(steps >= 0){
        fetch('/set_steps', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `steps_per_revolution=${steps}`
        }).then(response => response.json())
        .then(data => alert(`Кількість кроків на оберт: ${data.steps_per_revolution}`));
    }
    else{
        alert("Помилка: кількість кроків не може бути від'ємною!");
        return;
    }
}

function calibrate(direction) {
    var steps = document.getElementById("calibration_steps").value;
    if(steps >= 0){
        var delay = 500; // Затримка у мікросекундах
        fetch('/calibrate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            body: `direction=${direction}&steps=${steps}&delay=${delay}`
        }).then(response => response.json())
        .then(data => alert('Калібрування виконано'));
    }
    else{
        alert("Помилка: кількість кроків не може бути від'ємною!");
        return;
    }
}
