const apiKey = 'a0b2332cbf1ac4e8bc2432f99c12866e'; 

document.getElementById('weatherForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const location = document.getElementById('location').value.trim();

    if (location) {
        fetchWeather(location);
    } else {
        alert("Please enter a city name.");
    }
});

async function fetchWeather(location) {
    // Use backticks for template literals
    const apiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${location}&appid=${apiKey}&units=metric`;

    try {
        const response = await fetch(apiUrl);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Weather data not found');
        }

        // Extract rainfall data correctly
        let rainfall = 0;
        if (data.rain) {
            rainfall = data.rain['1h'] || data.rain['3h'] || 0;
        }

        const reqBody = {
            'humidity': data.main.humidity,
            'temperature': data.main.temp,
            'rainfall': rainfall,
            'risk_factor': data.wind.speed,
            'altitude': data.main.sea_level || 0  // Fallback in case sea_level is not available
        };

        // Call the flood prediction API and wait for the result
        const floodPrediction = await predictFlood(reqBody);

        if (floodPrediction) {
            // Store data in sessionStorage
            sessionStorage.setItem('city', data.name);
            sessionStorage.setItem('temperature', data.main.temp);
            sessionStorage.setItem('humidity', data.main.humidity);
            sessionStorage.setItem('windSpeed', data.wind.speed);
            sessionStorage.setItem('floodRisk', (data.wind.speed / 2).toFixed(2));
            sessionStorage.setItem('noFloodProb', floodPrediction['Probability of No Flood']);
            sessionStorage.setItem('floodProb', floodPrediction['Probability of Flood']);

            // Redirect to result page
            window.location.href = 'result.html'; // Ensure this path is correct
        } else {
            alert("Flood prediction failed. Please try again.");
        }
        
    } catch (error) {
        console.error("Error fetching weather data:", error);
        alert(`Could not retrieve weather data: ${error.message}`);
    }
}

const predictFlood = async (input) => {
    const url = "http://127.0.0.1:8000/predict"; // Ensure your backend is running and accessible

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(input), // Convert input object to JSON
        });

        // Check if the response is successful
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
        }

        // Parse the JSON response from the server
        const data = await response.json();

        // Validate response data
        if ('Probability of No Flood' in data && 'Probability of Flood' in data) {
            return data;
        } else {
            throw new Error('Invalid prediction data received.');
        }

    } catch (error) {
        console.error("Error during flood prediction:", error);
        alert(`Flood prediction failed: ${error.message}`);
        return null;
    }
};
