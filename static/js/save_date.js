document.addEventListener("DOMContentLoaded", function () {
    const dateInput = document.getElementById("id_expected_at");
    const localStorageKey = "expected_at_date";

    // Restaura a data salva anteriormente, se houver
    const savedDate = localStorage.getItem(localStorageKey);
    if (savedDate && !dateInput.value) {
        dateInput.value = savedDate;
    }

    // Atualiza o localStorage sempre que o usuário mudar a data
    dateInput.addEventListener("change", function () {
        console.log(dateInput.value)
        localStorage.setItem(localStorageKey, dateInput.value);
    });
});