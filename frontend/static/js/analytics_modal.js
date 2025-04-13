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

        fetch(`/api/alert-data?region=${encodeURIComponent(translatedName)}_область&month=3&year=2025`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                // Example: Display it in the modal
                document.getElementById('avgDuration').textContent = data.average_duration;
                document.getElementById('alertCount').textContent = data.alert_count;
                document.getElementById('alertPercentage').textContent = `${data.alert_percentage}%`;
                document.getElementById('lastAlert').textContent = data.last_alert;
            })
            .catch(error => console.error('API error:', error));


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
