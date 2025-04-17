document.addEventListener('DOMContentLoaded', function() {
  const team1Select = document.getElementById('team1');
  const team2Select = document.getElementById('team2');
  const venueSelect = document.getElementById('venue');
  const form = document.getElementById('predictionForm');
  const resultBox = document.getElementById('result');
  const analyzeBtn = document.getElementById('analyzeBtn');
  const analysisBox = document.getElementById('analysis');

  function updateVenues() {
      const team1 = team1Select.value;
      const team2 = team2Select.value;
      const validVenues = [...new Set([...(teamVenues[team1] || []), ...(teamVenues[team2] || [])])];
      const currentVenue = venueSelect.value;
      venueSelect.innerHTML = '';
      validVenues.forEach(venue => {
          const option = document.createElement('option');
          option.value = venue;
          option.textContent = venue;
          if (venue === currentVenue) option.selected = true;
          venueSelect.appendChild(option);
      });
      if (validVenues.length > 0 && !validVenues.includes(currentVenue)) {
          venueSelect.value = validVenues[0];
      }
  }
  team1Select.addEventListener('change', updateVenues);
  team2Select.addEventListener('change', updateVenues);
  updateVenues();

  form.addEventListener('submit', function(e) {
      e.preventDefault();
      resultBox.textContent = "Calculating...";
      fetch("/predict", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
              team1: team1Select.value,
              team2: team2Select.value,
              venue: venueSelect.value
          })
      })
      .then(res => res.json())
      .then(data => {
          resultBox.textContent = data.result;
      });
  });

  analyzeBtn.addEventListener('click', function() {
      analysisBox.innerHTML = "Analyzing...";
      fetch("/analysis", {method: "POST"})
      .then(res => res.text())
      .then(html => {
          analysisBox.innerHTML = html;
      });
  });
});
