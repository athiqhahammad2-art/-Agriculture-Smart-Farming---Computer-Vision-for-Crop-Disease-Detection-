# 🚀 Setup Guide - Smart Farming Crop Disease Detection

## Complete Step-by-Step Setup Instructions

### Part 1: Prerequisites

1. **Install Python 3.8+**
   - Download from: https://www.python.org/downloads/
   - Verify installation: `python --version`

2. **Install Git**
   - Download from: https://git-scm.com/
   - Verify: `git --version`

3. **Optional: Docker**
   - Download from: https://www.docker.com/products/docker-desktop
   - Verify: `docker --version`

### Part 2: Local Setup

#### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/agriculture-smart-farming.git
cd agriculture-smart-farming
```

#### Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**This will install:**
- Flask (web framework)
- TensorFlow & Keras (ML framework)
- OpenCV (image processing)
- SQLAlchemy (database ORM)
- And more...

#### Step 4: Create Directories
```bash
mkdir -p data/dataset models temp
```

#### Step 5: Configure Environment
```bash
cp .env.example .env
```

Edit `.env` if needed (default settings work fine).

#### Step 6: Run Application
```bash
python backend/app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

#### Step 7: Access Web Interface
Open browser and go to: `http://localhost:5000`

### Part 3: Docker Setup (Alternative)

#### Step 1: Build Docker Image
```bash
docker-compose build
```

#### Step 2: Run Containers
```bash
docker-compose up
```

#### Step 3: Access Application
- Frontend: `http://localhost`
- Backend API: `http://localhost:5000/api`

#### Step 4: Stop Containers
```bash
docker-compose down
```

### Part 4: Training with Your Dataset

#### Step 1: Prepare Dataset
Organize images in this structure:
```
data/dataset/
├── Early Blight/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Late Blight/
│   ├── image1.jpg
│   └── ...
├── Septoria/
├── Powdery Mildew/
└── Healthy/
```

**Recommended:**
- 100+ images per disease class
- Various angles and lighting conditions
- Mix of training and validation data

#### Step 2: Train Model
```bash
python training/train_model.py
```

**The script will:**
- Load your dataset
- Split into train/validation
- Train the model for 50 epochs
- Save best model to `models/disease_model.h5`

#### Step 3: Use Trained Model
The backend automatically loads the trained model. Just upload images and it will use your custom model.

### Part 5: Cloud Deployment

#### AWS Deployment

1. **Install AWS CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize:**
   ```bash
   eb init -p python-3.9 smart-farming
   ```

3. **Create environment:**
   ```bash
   eb create smart-farming-env
   ```

4. **Deploy:**
   ```bash
   eb deploy
   ```

#### Heroku Deployment

1. **Install Heroku CLI:**
   - Download from: https://devcenter.heroku.com/articles/heroku-cli

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create app:**
   ```bash
   heroku create smart-farming-app
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

#### DigitalOcean Deployment

1. **Create Droplet** (Ubuntu 20.04)

2. **SSH into server:**
   ```bash
   ssh root@your_server_ip
   ```

3. **Install Docker:**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

4. **Clone repository and deploy:**
   ```bash
   git clone your_repo
   cd agriculture-smart-farming
   docker-compose up -d
   ```

### Part 6: Troubleshooting

#### Issue: "ModuleNotFoundError: No module named 'tensorflow'"
**Solution:**
```bash
pip install --upgrade tensorflow
```

#### Issue: Port 5000 already in use
**Solution:**
```bash
python backend/app.py --port 8000
```

#### Issue: Images not processing
**Check:**
- Image format is JPG/PNG
- Image file size < 10MB
- Check console for error messages

#### Issue: GPU not recognized
**Solution (TensorFlow GPU):**
```bash
pip install tensorflow[and-cuda]
```

### Part 7: Performance Optimization

#### Enable GPU Support
```bash
pip install tensorflow[and-cuda]
```

#### Use Production Server
Replace `flask run` with gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 backend.app
```

#### Enable Caching
Edit `backend/app.py` and add:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

### Part 8: Monitoring

#### View Logs
**Docker:**
```bash
docker-compose logs -f
```

**Local:**
Logs appear in console when running `python backend/app.py`

#### Monitor Performance
```bash
# Check CPU/Memory usage
ps aux | grep python

# Docker stats
docker stats
```

### Next Steps

1. ✅ Test the application with sample images
2. ✅ Train with your own dataset
3. ✅ Deploy to cloud platform
4. ✅ Set up monitoring and logging
5. ✅ Share with farmers in your region

### Support

For issues:
1. Check console for error messages
2. Review logs in `data/` directory
3. Visit: https://github.com/issues
4. Contact support team

---

**Happy Farming! 🌾**