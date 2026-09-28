# fullstack_developer_capstone

## Project Name

fullstack_developer_capstone

## Project Description

Cars Dealership is a full-stack web application developed as part of the Full-stack Developer Capstone project...

> Full-stack web application for a national car retailer in the United States, providing dealer listings, state-based filtering, customer reviews with AI sentiment analysis, user authentication, and multi-cloud deployment configurations.

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Technologies Used](#-technologies-used)
3. [Architecture](#-architecture)
4. [Backend Setup](#-backend-setup)
5. [Frontend Setup](#-frontend-setup)
6. [Database Setup](#-database-setup)
7. [API Endpoints](#-api-endpoints)
8. [Authentication](#-authentication)
9. [Review System & Sentiment Analysis](#-review-system--sentiment-analysis)
10. [Docker Configuration](#-docker-configuration)
11. [Kubernetes Deployment](#-kubernetes-deployment)
12. [GitHub Actions CI/CD](#-github-actions-cicd)
13. [IBM Cloud Code Engine Deployment](#-ibm-cloud-code-engine-deployment)
14. [Testing Instructions](#-testing-instructions)
15. [Evidence Generation Guide](#-evidence-generation-guide)

---

## 🚗 Project Overview

**Cars Dealership** is a national automotive retail platform built to empower customers with transparent dealership information, customer reviews, and vehicle catalogs. 

### Key Features
- **National Dealer Directory:** Browse dealers across multiple U.S. states.
- **State Filtering:** Dynamically filter dealers by state (e.g. Kansas, Texas, California, New York).
- **Individual Dealer Details:** View detailed dealership info, phone numbers, and addresses.
- **Customer Review System:** Authenticated users can post detailed reviews, star ratings, and vehicle purchase details.
- **AI Sentiment Analysis:** Automated sentiment classification (positive, neutral, negative) for incoming customer reviews using VADER Sentiment analysis.
- **Car Catalog:** Structured car makes and model catalog (Toyota, Ford, Honda, Chevy, BMW, etc.).
- **User Authentication:** Registration, Login, Logout, and Django Admin panel.

---

## 🛠 Technologies Used

- **Backend Framework:** Python 3.11, Django 4.2, Django REST Framework (DRF)
- **Frontend Framework:** React 18, JSX, JavaScript, Bootstrap 5, Vite
- **Database:** SQLite (local development), PostgreSQL-ready for production
- **Microservices & Sentiment:** Flask 3.0, VADER Sentiment Analysis (`vaderSentiment`)
- **Containerization & Cloud Orchestration:** Docker, Docker Compose, Kubernetes
- **CI/CD Automation:** GitHub Actions
- **Deployment Platform:** IBM Cloud Code Engine / Red Hat OpenShift

---

## 🏗 Architecture

```
                                +---------------------------+
                                |      React Frontend       |
                                | (SPA / Static Components) |
                                +-------------+-------------+
                                              |
                                       HTTP / REST API
                                              |
                                              v
                                +-------------+-------------+
                                |      Django Backend       |
                                |  (REST Framework / Auth)  |
                                +-------+-------------+-----+
                                        |             |
                                        v             v
                           +------------+----+   +----+------------------+
                           |  SQLite DB      |   | Flask Microservice    |
                           | (Dealers, Cars, |   |  (Sentiment Analysis) |
                           |    Reviews)     |   +-----------------------+
                           +-----------------+
```

---

## ⚙️ Backend Setup

### Prerequisites
- Python 3.11+
- Virtual Environment tool (`venv`)

### Step-by-Step Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sanskarbhor28/Car-Dealership.git
   cd Car-Dealership
   ```

2. **Create and activate Python Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations & Populate Data:**
   ```bash
   python server/djangoapp/manage.py makemigrations djangoapp
   python server/djangoapp/manage.py migrate
   python server/djangoapp/manage.py populate_data
   ```

5. **Start Django Development Server:**
   ```bash
   python server/djangoapp/manage.py runserver 8000
   ```
   The backend server will run at `http://127.0.0.1:8000/`.

---

## 🎨 Frontend Setup

1. **Navigate to Frontend Directory:**
   ```bash
   cd server/djangoapp/frontend
   ```

2. **Install Node Dependencies:**
   ```bash
   npm install
   ```

3. **Build Frontend Production Bundle:**
   ```bash
   npm run build
   ```

4. **Run Vite Development Server (Optional):**
   ```bash
   npm run dev
   ```
   The Vite dev server will run at `http://localhost:3000/` and proxy API calls to port 8000.

---

## 🗄 Database Setup

The project uses SQLite for local development with predefined models:
- **`CarMake`**: Vehicle manufacturer name, description, country.
- **`CarModel`**: Vehicle model name, body type (Sedan, SUV, etc.), manufacturing year.
- **`Dealer`**: Dealership ID, full name, city, state, address, zip code, phone.
- **`Review`**: Reviewer name, review text, purchase status, purchase date, car make/model, star rating, sentiment.

### Populate Database Management Command
To populate initial sample data (including Kansas dealers):
```bash
python server/djangoapp/manage.py populate_data
```

### Admin User Creation
```bash
python server/djangoapp/manage.py createsuperuser
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/login/` | Authenticate user credentials |
| `POST` | `/api/logout/` | Log out authenticated user |
| `POST` | `/api/register/` | Register new user account |
| `GET` | `/api/dealers/` | List all dealerships |
| `GET` | `/api/dealers?state=Kansas` | Filter dealerships by state |
| `GET` | `/api/dealers/<dealer_id>/` | Get dealer details by ID |
| `GET` | `/api/dealers/<dealer_id>/reviews/` | Get reviews for a specific dealer |
| `GET` | `/api/carmakes/` | List all car makes and models |
| `POST` | `/api/analyze-review/` | Analyze sentiment of review text |
| `POST` | `/api/reviews/` | Post a new dealer review |

---

## 🔐 Authentication

Authentication is handled securely via Django session authentication and JSON endpoints:
- User registration requires `username`, `firstName`, `lastName`, `email`, and `password`.
- Login creates an authenticated user session and returns `{"status": "Authenticated", "userName": "..."}`.
- Logout invalidates the active session and returns `{"status": "Logged out"}`.

---

## 🤖 Review System & Sentiment Analysis

Review texts are evaluated automatically upon submission or query using **VADER Sentiment Analysis**:
- Compound score `≥ 0.05` ➔ **Positive Sentiment** (Green badge)
- Compound score `≤ -0.05` ➔ **Negative Sentiment** (Red badge)
- Otherwise ➔ **Neutral Sentiment** (Yellow badge)

Example API test:
```bash
curl -X POST http://127.0.0.1:8000/api/analyze-review/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Fantastic services"}'
```
Response:
```json
{
  "text": "Fantastic services",
  "sentiment": "positive"
}
```

---

## 🐳 Docker Configuration

### Building the Docker Image Locally
```bash
docker build -t car-dealership:latest .
```

### Running with Docker Container
```bash
docker run -d -p 8000:8000 --name car_dealership_app car-dealership:latest
```

### Running with Docker Compose
```bash
docker-compose up --build -d
```

---

## ☸️ Kubernetes Deployment

Kubernetes manifests are located in `kubernetes/`:
- `deployment.yaml`: Deployment spec with replica set & health probes.
- `service.yaml`: LoadBalancer service routing HTTP traffic to port 8000.
- `configmap.yaml`: Application configuration variables.
- `secret.yaml`: Production secret key template.

### Deploying to Kubernetes:
```bash
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

---

## 🔄 GitHub Actions CI/CD

Workflow configuration is stored in `.github/workflows/cicd.yml`.

### CI/CD Pipeline Steps:
1. Checkout repository code.
2. Set up Python 3.11 environment.
3. Install backend dependencies.
4. Run Django checks (`python manage.py check`).
5. Execute unit tests (`python manage.py test djangoapp`).
6. Set up Node.js environment.
7. Install frontend dependencies and build React assets (`npm run build`).
8. Validate Docker image build.

---

## ☁️ IBM Cloud Code Engine Deployment

### Deployment Steps:
1. **Login to IBM Cloud CLI:**
   ```bash
   ibmcloud login --apikey <YOUR_IBM_CLOUD_API_KEY> -r us-south
   ibmcloud target -g Default
   ```

2. **Log in to IBM Container Registry (ICR):**
   ```bash
   ibmcloud cr region-set us-south
   ibmcloud cr login
   ```

3. **Build & Push Docker Image:**
   ```bash
   docker build -t us.icr.io/<YOUR_NAMESPACE>/car-dealership:latest .
   docker push us.icr.io/<YOUR_NAMESPACE>/car-dealership:latest
   ```

4. **Deploy Application to Code Engine:**
   ```bash
   ibmcloud ce application create --name car-dealership-app \
     --image us.icr.io/<YOUR_NAMESPACE>/car-dealership:latest \
     --registry-secret icr-secret \
     --port 8000 \
     --min-scale 1 --max-scale 3
   ```

5. **Retrieve Public Deployment URL:**
   ```bash
   ibmcloud ce application get --name car-dealership-app --output url
   ```

---

## 🧪 Testing Instructions

Run all Django unit tests:
```bash
python server/djangoapp/manage.py test djangoapp
```

---

## 📝 Evidence Generation Guide

Execute the following cURL commands on your running local server (`http://127.0.0.1:8000`) and save the output text to the requested evidence files:

1. **`django_server`**: Real output terminal text when running `python server/djangoapp/manage.py runserver`.
2. **`loginuser`**: `curl -X POST http://127.0.0.1:8000/api/login/ -H "Content-Type: application/json" -d '{"userName":"john_doe","password":"Password123!"}'`
3. **`logoutuser`**: `curl -X POST http://127.0.0.1:8000/api/logout/`
4. **`getdealerreviews`**: `curl -X GET http://127.0.0.1:8000/api/dealers/1/reviews/`
5. **`getalldealers`**: `curl -X GET http://127.0.0.1:8000/api/dealers/`
6. **`getdealerbyid`**: `curl -X GET http://127.0.0.1:8000/api/dealers/1/`
7. **`getdealersbyState`**: `curl -X GET "http://127.0.0.1:8000/api/dealers/?state=Kansas"`
8. **`getallcarmakes`**: `curl -X GET http://127.0.0.1:8000/api/carmakes/`
9. **`analyzereview`**: `curl -X POST http://127.0.0.1:8000/api/analyze-review/ -H "Content-Type: application/json" -d '{"text":"Fantastic services"}'`

---

## 📄 License
This project is part of the IBM Full-Stack Software Developer Capstone Project.
