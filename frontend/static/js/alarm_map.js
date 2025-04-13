document.addEventListener('DOMContentLoaded', () => {
    const openModalButtons = document.querySelectorAll(".openModal");
    const closeModalButton = document.getElementById("closeModal");
    const modal = document.getElementById("modal");
    const regionNameH3 = document.getElementById("regionName"); 
    const newsItemDivs = [
        document.getElementById("n1"),
        document.getElementById("n2"),
        document.getElementById("n3"),
        document.getElementById("n4"),
        document.getElementById("n5")
    ];

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

    openModalButtons.forEach(buttonPath => {
        buttonPath.addEventListener("click", (event) => {
            const targetPath = event.target;
            const regionNameAttribute = targetPath.getAttribute('name');
            const contentString = targetPath.dataset.content || '';
            let displayRegionName = regionNameMap[regionNameAttribute] || regionNameAttribute || 'Невідомий регіон';
            let finalDisplayName = displayRegionName;
            if (displayRegionName &&
                !displayRegionName.includes('область') &&
                !displayRegionName.startsWith('м.') &&
                !displayRegionName.startsWith('А.Р.') &&
                displayRegionName !== 'Закарпаття' &&
                displayRegionName !== 'Севастополь'
               ) {
                finalDisplayName += " область";
            }
            regionNameH3.textContent = finalDisplayName;
            const newsEntries = contentString.split('///');
            newsItemDivs.forEach((newsDiv, index) => {
                const headlineSpan = newsDiv.querySelector('.news-headline');
                const linkAnchor = newsDiv.querySelector('.news-link');

                if (headlineSpan && linkAnchor) {
                    if (newsEntries[index]) {
                        const parts = newsEntries[index].split('::');
                        const headline = parts[0] ? parts[0].trim() : 'Немає заголовку';
                        const url = parts[1] ? parts[1].trim() : '#';

                        headlineSpan.textContent = headline;
                        linkAnchor.href = url;
                        newsDiv.style.display = 'flex';
                    } else {
                        newsDiv.style.display = 'none';
                        headlineSpan.textContent = '';
                        linkAnchor.href = '#';
                    }
                }
            });
            modal.classList.add("active");
            document.body.classList.add("modal-open");
        });
    });

    closeModalButton.addEventListener("click", () => {
        modal.classList.remove("active");
        document.body.classList.remove("modal-open");
    });

    modal.addEventListener('click', (event) => {
       if (event.target === modal) {
           modal.classList.remove("active");
           document.body.classList.remove("modal-open");
       }
    });

});
