function updateFormFields() {
            const repeat = document.getElementById("repeat").value;
            const timeField = document.getElementById("time_field");
            const weekdayField = document.getElementById("weekday_field");
            const dateField = document.getElementById("date_field");

            // Скидаємо всі додаткові поля
            timeField.classList.remove("hidden");
            weekdayField.classList.add("hidden");
            dateField.classList.add("hidden");

            // Показуємо потрібні поля залежно від вибраного варіанту
            if (repeat === "daily") {
                timeField.classList.remove("hidden");
            } else if (repeat === "weekly") {
                weekdayField.classList.remove("hidden");
                timeField.classList.remove("hidden");
            } else if (repeat === "one-time") {
                dateField.classList.remove("hidden");
                timeField.classList.remove("hidden");
            }
        }
        document.addEventListener("DOMContentLoaded", updateFormFields);
});