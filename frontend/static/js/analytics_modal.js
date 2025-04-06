const openModalButtons = document.querySelectorAll(".openModal");
const closeModal = document.getElementById("closeModal");
const modal = document.getElementById("modal");
const regionName = document.getElementById("regionName");

const regionNameMap = {
    "Avtonomna Respublika Krym": "А.Р. Крим",
    "Vinnytska": "Вінницька",
    "Volynska": "Волинська",
    "Dnipropetrovska": "Дніпропетровська",
    "Donetska": "Донецька",
    "Zhytomyrska": "Житомирська",
    "Zakarpatska": "Закарпаття",
    "Zaporizka": "Запорізька",
    "Ivano-Frankivska": "Івано-Франківська",
    "Kyivska": "Київська",
    "Kirovohradska": "Кіровоградська",
    "Luhanska": "Луганська",
    "Lvivska": "Львівська",
    "Mykolaivska": "Миколаївська",
    "Odeska": "Одеська",
    "Poltavska": "Полтавська",
    "Rivnenska": "Рівненська",
    "Sumska": "Сумська",
    "Ternopilska": "Тернопільська",
    "Kharkivska": "Харківська",
    "Khersonska": "Херсонська",
    "Khmelnytska": "Хмельницька",
    "Cherkaska": "Черкаська",
    "Chernivetska": "Чернівецька",
    "Chernihivska": "Чернігівська",
    "Kyiv": "м. Київ",
    "Sevastopilska": "Севастополь"
};

openModalButtons.forEach(button => {
    button.addEventListener("click", (event) => {
        const name = event.target.getAttribute('name');
        let translatedName = regionNameMap[name] || name || 'Невідомий регіон';

        if (
            translatedName &&
            !translatedName.includes('область') &&
            !translatedName.startsWith('м.') &&
            !translatedName.startsWith('А.Р.') &&
            translatedName !== 'Закарпаття' &&
            translatedName !== 'Севастополь'
        ) {
            translatedName += " область";
        }

        regionName.textContent = translatedName;

        modal.classList.add("active");
        document.body.classList.add("modal-open");
    });
});

closeModal.addEventListener("click", () => {
    modal.classList.remove("active");
    document.body.classList.remove("modal-open");
});
