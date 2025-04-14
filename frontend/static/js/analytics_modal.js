// DOM Elements
const openModalButtons = document.querySelectorAll(".openModal");
const closeModalButton = document.getElementById("closeModal");
const modal = document.getElementById("modal");
const regionNameElement = document.getElementById("regionName");
const buttonContainer = document.querySelector('.popup-buttons');
const avgDurationElement = document.getElementById('avgDuration');
const alertCountElement = document.getElementById('alertCount');
const alertPercentageElement = document.getElementById('alertPercentage');
const lastAlertElement = document.getElementById('lastAlert');
const chartImageElement = document.getElementById('chartImage');
const loadingElement = document.getElementById('loading');

// Region name mapping
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

// Store the currently active listener function
let currentPeriodButtonListener = null;
// Store the AbortController for fetch requests
let currentFetchController = null;

// Function to show loading state
function showLoading() {
  loadingElement.classList.add('active');
}

// Function to hide loading state
function hideLoading() {
  loadingElement.classList.remove('active');
}

// Function to clear modal data
function clearModalData() {
  avgDurationElement.textContent = '';
  alertCountElement.textContent = '';
  alertPercentageElement.textContent = '';
  lastAlertElement.textContent = '';
  // Set a transparent pixel or placeholder
  chartImageElement.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
}

// Function to fetch and update data
async function fetchAndUpdateData(region, period) {
  // Abort any previous ongoing fetch for this modal
  if (currentFetchController) {
    currentFetchController.abort();
  }
  // Create a new controller for the new fetch
  currentFetchController = new AbortController();
  const signal = currentFetchController.signal;

  // Clear previous data immediately before fetching
  clearModalData();
  // Show loading indicator
  showLoading();

  try {
    const response = await fetch(`/api/alert-data?region=${encodeURIComponent(region)}_область&range=${period}`, { signal });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log(`Data fetched for ${region}, period ${period}:`, data);

    // Update UI only if the fetch wasn't aborted
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
      console.log('Fetch aborted');
    } else {
      console.error('API error:', error);
      // Display error message to the user in the modal
      lastAlertElement.textContent = 'Помилка завантаження даних.';
      // Clear other fields or show error state
      avgDurationElement.textContent = '-';
      alertCountElement.textContent = '-';
      alertPercentageElement.textContent = '-';
      chartImageElement.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
    }
  } finally {
    hideLoading();
  }
}

// Event listener for opening the modal
openModalButtons.forEach(button => {
  button.addEventListener("click", async (event) => {
    const name = event.target.getAttribute('name');
    const translatedName = regionNameMap[name] || name || 'Невідомий регіон';
    let currentPeriod = "year"; // Default period when opening

    // Prepare display name
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

    // Clear old data and listener
    clearModalData();
    if (buttonContainer && currentPeriodButtonListener) {
      buttonContainer.removeEventListener('click', currentPeriodButtonListener);
      currentPeriodButtonListener = null;
    }
    
    // Abort any fetch that might be ongoing from a previously closed modal
    if (currentFetchController) {
      currentFetchController.abort();
      currentFetchController = null;
    }

    if (buttonContainer) {
      // Set initial active button
      buttonContainer.querySelectorAll('button[data-period]').forEach(btn => {
        btn.classList.remove('active');
      });
      const initialActiveButton = buttonContainer.querySelector(`button[data-period="${currentPeriod}"]`);
      if (initialActiveButton) {
        initialActiveButton.classList.add('active');
      }

      // Define the new listener function for THIS modal instance
      currentPeriodButtonListener = async (e) => {
        const clickedButton = e.target.closest('button[data-period]');
        if (clickedButton && !clickedButton.classList.contains('active')) {
          const newPeriod = clickedButton.dataset.period;
          currentPeriod = newPeriod;

          // Update active button state
          buttonContainer.querySelectorAll('button[data-period]').forEach(btn => {
            btn.classList.remove('active');
          });
          clickedButton.classList.add('active');

          // Fetch data for the new period
          fetchAndUpdateData(translatedName, newPeriod);
        }
      };

      // Add the new listener
      buttonContainer.addEventListener('click', currentPeriodButtonListener);

      // Fetch initial data for the default period
      fetchAndUpdateData(translatedName, currentPeriod);
    } else {
      console.error("Error: Could not find the element with class 'popup-buttons'.");
      lastAlertElement.textContent = 'Помилка інтерфейсу: кнопки періоду не знайдено.';
    }

    // Show Modal
    modal.classList.add("active");
    document.body.classList.add("modal-open");
  });
});

// Event listener for closing the modal
closeModalButton.addEventListener("click", () => {
  modal.classList.remove("active");
  document.body.classList.remove("modal-open");

  // Clean up when modal closes
  clearModalData();
  if (buttonContainer && currentPeriodButtonListener) {
    buttonContainer.removeEventListener('click', currentPeriodButtonListener);
    currentPeriodButtonListener = null;
  }
  
  // Abort any ongoing fetch when closing the modal
  if (currentFetchController) {
    currentFetchController.abort();
    currentFetchController = null;
  }
});

// Close modal when clicking outside the content
modal.addEventListener("click", (e) => {
  if (e.target === modal) {
    closeModalButton.click();
  }
});

// Close modal with Escape key
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && modal.classList.contains("active")) {
    closeModalButton.click();
  }
});