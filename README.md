# 🌾 Smart Farming - Crop Disease Detection

An AI-powered system for detecting crop diseases using Computer Vision and Deep Learning.

## 🎯 Overview

This project uses transfer learning (MobileNetV2) to detect crop diseases in real-time. It provides:
- **5+ Disease Detection**: Early Blight, Late Blight, Septoria, Powdery Mildew, Healthy
- **95%+ Accuracy**: Using pre-trained deep learning models
- **Treatment Recommendations**: Personalized for each disease
- **Real-time Analysis**: Fast inference on CPU/GPU
- **Web Interface**: Easy-to-use dashboard for farmers

## 📋 Features

✅ **Machine Learning**
- Transfer learning with MobileNetV2
- Fine-tuned for crop disease classification
- Data augmentation for improved accuracy

✅ **Backend (Flask API)**
- RESTful API endpoints
- Image preprocessing and normalization
- Database storage for predictions
- Treatment recommendations engine

✅ **Frontend (Web UI)**
- Drag-and-drop image upload
- Real-time disease detection
- Prediction history
- Statistics dashboard
- Responsive design

✅ **Deployment**
- Docker containerization
- Production-ready configuration
- Easy deployment on cloud platforms

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda
- Optional: Docker

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Agriculture-Smart-Farming
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python backend/app.py
```

5. Open browser:
```
http://localhost:5000
```

### Docker Deployment

```bash
docker-compose up
```

Then open `http://localhost`

## 📁 Project Structure

```
├── backend/
│   └── app.py              # Flask application
├── models/
│   └── disease_detector.py # ML model
├── utils/
│   └── image_processor.py  # Image preprocessing
├── database/
│   └── db_handler.py       # Database operations
├── training/
│   └── train_model.py      # Model training script
├── frontend/
│   ├── index.html          # Web UI
│   ├── styles.css          # Styling
│   └── app.js              # Frontend logic
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🎓 Training

To train the model with your own dataset:

1. Prepare dataset structure:
```
data/dataset/
├── Early Blight/
├── Late Blight/
├── Septoria/
├── Powdery Mildew/
└── Healthy/
```

2. Run training:
```bash
python training/train_model.py
```

## 📊 API Endpoints

- `POST /api/predict` - Predict disease from image
- `GET /api/history` - Get prediction history
- `GET /api/statistics` - Get statistics
- `GET /api/diseases` - Get available diseases
- `GET /api/health` - Health check

## 🔧 Configuration

Edit `.env` file to configure:
```
FLASK_ENV=production
DATABASE_URL=sqlite:///data/predictions.db
MODEL_PATH=models/disease_model.h5
CONFIDENCE_THRESHOLD=0.5
```

## 📈 Disease Reference

### Early Blight
- Symptoms: Brown lesions with concentric rings
- Treatment: Fungicides, leaf removal
- Prevention: Crop rotation, spacing

### Late Blight
- Symptoms: Water-soaked spots, white mold
- Treatment: Systemic fungicides, isolation
- Prevention: Resistant varieties, monitoring

### Septoria
- Symptoms: Small circular spots
- Treatment: Protectant fungicides
- Prevention: Sanitation, spacing

### Powdery Mildew
- Symptoms: White powder on leaves
- Treatment: Sulfur-based fungicides
- Prevention: Ventilation, humidity control

## 🌐 Deployment

### AWS
```bash
eb init
eb create smart-farming
eb deploy
```

### Heroku
```bash
heroku create smart-farming
git push heroku main
```

### DigitalOcean
```bash
docker build -t smart-farming .
docker tag smart-farming:latest registry.digitalocean.com/smart-farming/app:latest
docker push registry.digitalocean.com/smart-farming/app:latest
```

## 📝 License

MIT License - feel free to use for personal and commercial projects

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please open an issue on GitHub.

## 🙏 Acknowledgments

- TensorFlow & Keras team
- MobileNet architecture creators
- Agriculture research community