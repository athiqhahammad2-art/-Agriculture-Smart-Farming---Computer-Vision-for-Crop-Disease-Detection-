const API_BASE_URL = 'http://localhost:5000/api';
let selectedImageFile = null;

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const resultImage = document.getElementById('resultImage');
const diseaseName = document.getElementById('diseaseName');
const confidenceFill = document.getElementById('confidenceFill');
const confidenceText = document.getElementById('confidenceText');
const predictions = document.getElementById('predictions');
const recommendations = document.getElementById('recommendations');
const historyContainer = document.getElementById('historyContainer');
const statsContainer = document.getElementById('statsContainer');

// Upload handlers
uploadArea.addEventListener('click', () => imageInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

imageInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

function handleFiles(files) {
    if (files.length > 0) {
        selectedImageFile = files[0];
        displayPreview(selectedImageFile);
        analyzeBtn.disabled = false;
    }
}

function displayPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        resultImage.src = e.target.result;
        uploadArea.innerHTML = `<p>✓ Image selected: ${file.name}</p>`;
    };
    reader.readAsDataURL(file);
}

analyzeBtn.addEventListener('click', analyzeImage);

async function analyzeImage() {
    if (!selectedImageFile) return;

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = 'Analyzing...';

    try {
        const formData = new FormData();
        formData.append('image', selectedImageFile);

        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Analysis failed');

        const result = await response.json();
        displayResults(result);
        loadHistory();
        loadStatistics();

    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = 'Analyze Image';
    }
}

function displayResults(result) {
    resultsSection.style.display = 'block';
    
    // Disease name and confidence
    diseaseName.textContent = result.disease;
    const confidence = (result.confidence * 100).toFixed(1);
    confidenceFill.style.width = confidence + '%';
    confidenceText.textContent = confidence + '%';

    // All predictions
    predictions.innerHTML = '<strong>All Predictions:</strong>';
    for (const [disease, prob] of Object.entries(result.all_predictions)) {
        const prob_percent = (prob * 100).toFixed(1);
        predictions.innerHTML += `<div>${disease}: ${prob_percent}%</div>`;
    }

    // Recommendations
    if (result.recommendations) {
        const rec = result.recommendations;
        recommendations.innerHTML = `
            <h3>🎯 Treatment & Prevention</h3>
            <strong>Severity:</strong> ${rec.severity}<br><br>
            <strong>Recommended Treatments:</strong>
            <ul>${rec.treatments.map(t => `<li>${t}</li>`).join('')}</ul>
            <strong>Prevention Measures:</strong>
            <ul>${rec.prevention.map(p => `<li>${p}</li>`).join('')}</ul>
        `;
    }

    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/history?limit=6`);
        const data = await response.json();

        historyContainer.innerHTML = '';
        data.history.forEach(item => {
            const time = new Date(item.timestamp).toLocaleDateString();
            const card = document.createElement('div');
            card.className = 'history-item';
            card.innerHTML = `
                <div class="disease">${item.disease}</div>
                <div class="confidence">Confidence: ${(item.confidence * 100).toFixed(1)}%</div>
                <div class="time">${time}</div>
            `;
            historyContainer.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/statistics`);
        const stats = await response.json();

        statsContainer.innerHTML = `
            <div class="stat-card">
                <div class="label">Total Predictions</div>
                <div class="value">${stats.total_predictions}</div>
            </div>
            <div class="stat-card">
                <div class="label">Average Confidence</div>
                <div class="value">${(stats.average_confidence * 100).toFixed(1)}%</div>
            </div>
        `;

        // Disease distribution
        for (const [disease, count] of Object.entries(stats.disease_distribution)) {
            statsContainer.innerHTML += `
                <div class="stat-card">
                    <div class="label">${disease}</div>
                    <div class="value">${count}</div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Load initial data
loadHistory();
loadStatistics();