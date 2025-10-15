# DataLens — Intelligent Data Dashboard Web App 💡

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **full-stack intelligent data dashboard** that automates dataset analysis, visualization, and insight generation with secure authentication and cloud deployment.

---

## 🎯 **Project Overview**

**DataLens** is an enterprise-grade web application that allows users to:
- 📤 **Upload datasets** (CSV, Excel, JSON)
- 🔍 **Automatically analyze** data with statistical insights
- 📊 **Visualize** data with interactive charts and graphs
- 🤖 **Generate AI-powered insights** and predictions
- 🔐 **Secure authentication** with JWT-based user management
- ☁️ **Cloud deployment** ready for production

---

## 🛠️ **Tech Stack**

### **Backend**
- **FastAPI** — Modern, fast Python web framework
- **Pandas & NumPy** — Data processing and analysis
- **SQLAlchemy** — ORM for database operations
- **PostgreSQL** — Primary database
- **JWT** — Authentication & authorization
- **Pytest** — Testing framework

### **Frontend**
- **React 18** — UI library
- **Vite** — Build tool
- **TailwindCSS** — Styling framework
- **shadcn/ui** — Component library
- **Chart.js / Plotly** — Data visualization
- **Axios** — HTTP client

### **DevOps**
- **Docker** — Containerization
- **Render / Railway** — Backend hosting
- **Vercel** — Frontend hosting
- **GitHub Actions** — CI/CD pipeline

---

## 📁 **Project Structure**

```
DataLens/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   ├── auth.py
│   │   │   ├── datasets.py
│   │   │   └── analysis.py
│   │   ├── core/              # Core configurations
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/            # Database models
│   │   │   ├── user.py
│   │   │   └── dataset.py
│   │   ├── services/          # Business logic
│   │   │   ├── data_processor.py
│   │   │   ├── analyzer.py
│   │   │   └── visualizer.py
│   │   ├── schemas/           # Pydantic schemas
│   │   └── main.py            # Application entry point
│   ├── tests/                 # Unit tests
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── DataUpload.jsx
│   │   │   ├── Charts.jsx
│   │   │   └── Auth/
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   ├── hooks/             # Custom hooks
│   │   ├── utils/             # Utility functions
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── docs/                       # Documentation
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── DEPLOYMENT.md
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── .gitignore
├── docker-compose.yml
├── PROJECT_PLAN.md
└── README.md
```

---

## 🚀 **Features**

### **Phase 1: Core Features** ✅
- [x] User authentication (Register, Login, JWT)
- [x] File upload (CSV, Excel, JSON)
- [x] Data preview and validation
- [x] Basic statistical analysis
- [x] Data visualization (charts, graphs)

### **Phase 2: Advanced Features** 🔄
- [ ] Advanced analytics (correlation, trends)
- [ ] Custom query builder
- [ ] Export reports (PDF, Excel)
- [ ] Real-time collaboration
- [ ] Data filtering and search

### **Phase 3: AI/ML Features** 🤖
- [ ] Predictive analytics
- [ ] Anomaly detection
- [ ] Natural language queries
- [ ] Automated insights generation

---

## 📚 **Skills You'll Learn**

| Category | Skills |
|----------|--------|
| **Backend Development** | FastAPI, REST APIs, Async Python |
| **Data Engineering** | Pandas, NumPy, Data Cleaning, ETL |
| **Database** | PostgreSQL, SQLAlchemy, Query Optimization |
| **Authentication** | JWT, OAuth2, Security Best Practices |
| **Frontend** | React, State Management, Component Design |
| **Visualization** | Chart.js, Plotly, Data Storytelling |
| **Testing** | Pytest, Jest, Integration Testing |
| **DevOps** | Docker, CI/CD, Cloud Deployment |

---

## 🏃 **Getting Started**

### **Prerequisites**
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Git

### **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

### **Database Setup**
```bash
# Create PostgreSQL database
createdb datalens

# Run migrations
alembic upgrade head
```

---

## 📖 **Documentation**

- [Project Plan](PROJECT_PLAN.md) — Detailed development roadmap
- [Architecture](docs/ARCHITECTURE.md) — System design and architecture
- [API Documentation](docs/API.md) — API endpoints and usage
- [Deployment Guide](docs/DEPLOYMENT.md) — Production deployment steps

---

## 🧪 **Testing**

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

---

## 🚢 **Deployment**

### **Backend (Render/Railway)**
```bash
# Build Docker image
docker build -t datalens-backend ./backend

# Deploy to Render
# (Connect GitHub repo to Render)
```

### **Frontend (Vercel)**
```bash
cd frontend
npm run build
vercel --prod
```

---

## 🤝 **Contributing**

This is a learning project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 **Author**

**Akash** — [GitHub Profile](https://github.com/22CB006)

Built as a portfolio project to demonstrate full-stack development, data engineering, and cloud deployment skills.

---

## 🙏 **Acknowledgments**

- FastAPI documentation and community
- React and Vite teams
- Open-source contributors

---

## 📧 **Contact**

For questions or feedback, please open an issue on GitHub.

---

**⭐ Star this repository if you find it helpful!**
