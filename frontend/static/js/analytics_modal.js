/* Елементи DOM */
const openModalButtons = document.querySelectorAll(".openModal");
const closeModal = document.getElementById("closeModal");
const modal = document.getElementById("modal");
const regionNameElement = document.getElementById("regionName");
const buttonContainer = document.querySelector('.popup-buttons');
const avgDurationElement = document.getElementById('avgDuration');
const alertCountElement = document.getElementById('alertCount');
const alertPercentageElement = document.getElementById('alertPercentage');
const lastAlertElement = document.getElementById('lastAlert');
const chartImageElement = document.getElementById('chartImage');
const loadingElement = document.getElementById('loading');

/* Відображення назв регіонів */
const regionNameMap = {
  "Avtonomna Respublika Krym": "А.Р. Крим",
  "Vinnytska": "Вінницька",
  "Volynska": "Волинська",
  "Dnipropetrovska": "Дніпропетровська",
  "Donetska": "Донецька",
  "Zhytomyrska": "Житомирська",
  "Zakarpatska": "Закарпатська",
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

/* Зберігає поточну активну функцію слухача */
let currentPeriodButtonListener = null;
/* Зберігає AbortController для запитів fetch */
let currentFetchController = null;

/* Функція для відображення стану завантаження */
function showLoading() {
  loadingElement.classList.add('active');
}

/* Функція для приховання стану завантаження */
function hideLoading() {
  loadingElement.classList.remove('active');
}

/* Функція для очищення даних модального вікна */
function clearModalData() {
  avgDurationElement.textContent = '';
  alertCountElement.textContent = '';
  alertPercentageElement.textContent = '';
  lastAlertElement.textContent = '';
  /* Встановлення прозорого пікселя або заповнювача */
  chartImageElement.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
}

/* Функція для отримання та оновлення даних */
async function fetchAndUpdateData(region, period) {
  /* Перервати будь-який попередній триваючий запит fetch для цього модального вікна */
  if (currentFetchController) {
    currentFetchController.abort();
  }
  /* Створити новий контролер для нового запиту fetch */
  currentFetchController = new AbortController();
  const signal = currentFetchController.signal;

  /* Очистити попередні дані безпосередньо перед отриманням */
  clearModalData();
  /* Показати індикатор завантаження */
  showLoading();

  let currentRegion = region;

  switch (currentRegion) {
    case "А.Р. Крим":
      currentRegion = "Автономна Республіка Крим"
      break;
    default:
      currentRegion = currentRegion + " область"
      break;
  }
  try {
    const response = await fetch(`/api/alert-data?region=${encodeURIComponent(currentRegion)}&range=${period}`, { signal });
    if (!response.ok) {
      throw new Error(`HTTP помилка! статус: ${response.status}`);
    }
    const data = await response.json();
    console.log(`Дані отримано для ${region}, період ${period}:`, data);

    /* Оновити інтерфейс користувача лише якщо запит fetch не було перервано */
    avgDurationElement.textContent = data.average_duration ?? 'N/A';
    alertCountElement.textContent = data.alert_count ?? 'N/A';
    alertPercentageElement.textContent = data.alert_percentage !== undefined ? `${data.alert_percentage}%` : 'N/A';
    lastAlertElement.textContent = data.last_alert ?? 'Немає даних';

    if (data.imageBase64) {
      chartImageElement.src = `data:image/png;base64,${data.imageBase64}`;
    } else {
      chartImageElement.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
    }

  } catch (error) {
    if (error.name === 'AbortError') {
      console.log('Запит fetch перервано');
    } else {
      console.error('Помилка API:', error);
      /* Відобразити повідомлення про помилку користувачеві в модальному вікні */
      lastAlertElement.textContent = 'Помилка завантаження даних.';
      /* Очистити інші поля або показати стан помилки */
      avgDurationElement.textContent = '-';
      alertCountElement.textContent = '-';
      alertPercentageElement.textContent = '-';
      chartImageElement.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
    }
  } finally {
    hideLoading();
  }
}

/* Слухач подій для відкриття модального вікна */
openModalButtons.forEach(button => {
  button.addEventListener("click", async (event) => {
    const name = event.target.getAttribute('name');
    let translatedName = regionNameMap[name] || name || 'Невідомий регіон';
    let currentPeriod = "year"; /* Період за замовчуванням при відкритті */

    /* Підготовка назви для відображення */
    let displayName = translatedName;
    if (
      translatedName &&
      !translatedName.includes('область') &&
      !translatedName.startsWith('м.') &&
      !translatedName.startsWith('А.Р.') &&
      translatedName !== 'Закарпаття' &&
      translatedName !== 'Севастополь'
    ) {
      displayName = translatedName + " область";
    }
    regionNameElement.textContent = displayName;

    /* Очистити старі дані та слухача */
    clearModalData();
    if (buttonContainer && currentPeriodButtonListener) {
      buttonContainer.removeEventListener('click', currentPeriodButtonListener);
      currentPeriodButtonListener = null;
    }

    /* Перервати будь-який запит fetch, який може тривати з попередньо закритого модального вікна */
    if (currentFetchController) {
      currentFetchController.abort();
      currentFetchController = null;
    }

    if (buttonContainer) {
      /* Встановити початкову активну кнопку */
      buttonContainer.querySelectorAll('button[data-period]').forEach(btn => {
        btn.classList.remove('active');
      });
      const initialActiveButton = buttonContainer.querySelector(`button[data-period="${currentPeriod}"]`);
      if (initialActiveButton) {
        initialActiveButton.classList.add('active');
      }

      /* Визначити нову функцію слухача для ЦЬОГО екземпляра модального вікна */
      currentPeriodButtonListener = async (e) => {
        const clickedButton = e.target.closest('button[data-period]');
        if (clickedButton && !clickedButton.classList.contains('active')) {
          const newPeriod = clickedButton.dataset.period;
          currentPeriod = newPeriod;

       
          buttonContainer.querySelectorAll('button[data-period]').forEach(btn => {
            btn.classList.remove('active');
          });
          clickedButton.classList.add('active');

        
          fetchAndUpdateData(translatedName, newPeriod);
        }
      };

    
      buttonContainer.addEventListener('click', currentPeriodButtonListener);

      fetchAndUpdateData(translatedName, currentPeriod);
    } else {
      console.error("Помилка: Не вдалося знайти елемент з класом 'popup-buttons'.");
      lastAlertElement.textContent = 'Помилка інтерфейсу: кнопки періоду не знайдено.';
    }

    
    modal.classList.add("active");
    document.body.classList.add("modal-open");
  });
});


closeModal.addEventListener("click", () => {
  modal.classList.remove("active");
  document.body.classList.remove("modal-open");

 
  clearModalData();
  if (buttonContainer && currentPeriodButtonListener) {
    buttonContainer.removeEventListener('click', currentPeriodButtonListener);
    currentPeriodButtonListener = null;
  }

  
  if (currentFetchController) {
    currentFetchController.abort();
    currentFetchController = null;
  }
});


modal.addEventListener("click", (e) => {
  if (e.target === modal) {
    closeModal.click();
  }
});


document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && modal.classList.contains("active")) {
    closeModal.click();
  }
});