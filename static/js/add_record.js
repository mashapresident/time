//перевірка введених даних та оновлення інтерфейсу
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("add_event_form");
    const eventName = document.getElementById("event_name");
    const repeatSelect = document.getElementById("repeat");
    const eventTime = document.getElementById("event_time");
    const eventDate = document.getElementById("event_date");
    const weekdayField = document.getElementById("weekday_field");
    const dateField = document.getElementById("date_field");
    const weekday = document.getElementById("weekday");
    const soundFileInput = document.getElementById("soundFile");
    const audioUploads = document.querySelector(".audio-uploads");
    const uploadButton = document.getElementById("add_sound");

    // Функція оновлення видимості полів залежно від вибору повторення
    function updateVisibility() {
        const selectedValue = repeatSelect.value;
        weekdayField.style.display = (selectedValue === "weekly") ? "block" : "none";
        dateField.style.display = (selectedValue === "one-time") ? "block" : "none";
    }

    repeatSelect.addEventListener("change", updateVisibility);
    updateVisibility();

    soundFileInput.addEventListener("change", function () {
        if (this.files.length > 0) {
            audioUploads.style.border = "2px solid blue";
            audioUploads.style.backgroundColor = "#005bd1";
            audioUploads.style.borderRadius = "8px";
            uploadButton.textContent = "Замінити файл";
            uploadButton.style.backgroundColor = "transparent";
        }
    });

    // Перевірка валідності введених даних перед відправкою форми
    form.addEventListener("submit", function (event) {
        let isValid = true;

        if (eventName.value.trim() === "") {
            alert("Назва події не може бути порожньою!");
            isValid = false;
        }

        if (repeatSelect.value === "weekly" && weekday.value === "") {
            alert("Будь ласка, виберіть день тижня!");
            isValid = false;
        } else if (repeatSelect.value === "one-time" && eventDate.value === "") {
            alert("Будь ласка, виберіть дату!");
            isValid = false;
        }

        if (!eventTime.value) {
            alert("Будь ласка, введіть час події!");
            isValid = false;
        }

        if (soundFileInput.files.length > 0) {
            const file = soundFileInput.files[0];
            if (!file.type.startsWith("audio/")) {
                alert("Будь ласка, виберіть коректний аудіофайл!");
                isValid = false;
            }
        }

        if (!isValid) {
            event.preventDefault();
        }
    });
});



