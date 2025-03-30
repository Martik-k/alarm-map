document.addEventListener("DOMContentLoaded", () => {
    const openBtn = document.getElementById("open-selector");
    const closeBtn = document.getElementById("close-selector");
    const selector = document.getElementById("selector");

    if (!openBtn || !closeBtn || !selector) {
        console.error("Помилка: один із елементів не знайдено!");
        return;
    }

    openBtn.addEventListener("click", () => {
        selector.classList.add("open");
        openBtn.style.display = "none"; // Ховаємо кнопку
    });

    closeBtn.addEventListener("click", () => {
        selector.classList.remove("open");
        openBtn.style.display = "block"; // Повертаємо кнопку
    });
});
