document.addEventListener('DOMContentLoaded', () => {
  const danger_data_1 = JSON.parse(document.getElementById('danger-data-1').textContent);
  const danger_data_2 = JSON.parse(document.getElementById('danger-data-2').textContent);
  let danger_data = danger_data_1; 

  function updateMap(data) {
    for (const region in data) {
      const path = document.querySelector(`path[name="${region}"]`);
      if (path) {
        path.style.fill = data[region]; 
      }
    }
  }


  updateMap(danger_data);

  document.querySelectorAll('input[name="danger-level"]').forEach(radio => {
    radio.addEventListener('change', () => {
      danger_data = (radio.value === 'all') ? danger_data_1 : danger_data_2;
      updateMap(danger_data);
    });
  });
});
