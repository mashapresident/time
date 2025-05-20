//перевірка введених даних
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("set_steps").addEventListener("submit", function (event) {
        let stepsInput = document.getElementById("steps_per_revolution");
        let stepsValue = parseInt(stepsInput.value, 10);

        if (isNaN(stepsValue) || stepsValue <= 0) {
            alert("Кількість кроків на оберт повинна бути додатнім числом!");
            event.preventDefault();
        }
    });
});

//перевірка введених даних
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("set_period").addEventListener("submit", function (event) {
        let periodInput = document.getElementById("period_per_revolution");
        let periodValue = parseInt(periodInput.value, 10);

        if (isNaN(periodValue) || periodValue <= 0) {
            alert("Час проходу на хвилину повинен бути додатнім числом!");
            event.preventDefault();
        }
    });
});


//перевірка введених даних та оновлення інтерфейсу
document.addEventListener("DOMContentLoaded", function () {
    const melodyFileInput = document.getElementById("melodyFile");
    const knockFileInput = document.getElementById("knockSoundFile");
    const audioUploads1 = document.querySelector(".audio-uploads1");
    const audioUploads2 = document.querySelector(".audio-uploads2");
    const addMelodyButton = document.getElementById("add_melody");
    const addKnockButton = document.getElementById("add_knock");

    melodyFileInput.addEventListener("change", function () {
        if (this.files.length > 0) {
            audioUploads1.style.border = "2px solid blue";
            audioUploads1.style.backgroundColor = "#005bd1";
            audioUploads1.style.borderRadius = "8px";
            addMelodyButton.textContent = "Замінити файл";
            addMelodyButton.style.backgroundColor = "transparent";
        }
    })
    knockFileInput.addEventListener("change", function () {
        if (this.files.length > 0) {
            audioUploads2.style.border = "2px solid blue";
            audioUploads2.style.backgroundColor = "#005bd1";
            audioUploads2.style.borderRadius = "8px";
            addKnockButton.textContent = "Замінити файл";
            addKnockButton.style.backgroundColor = "transparent";
        }
    });
});

