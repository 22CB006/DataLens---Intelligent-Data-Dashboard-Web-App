# DataLens — Intelligent Data Dashboard Web App 💡

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)

A **personal learning project** - building a full-stack intelligent data dashboard to showcase my skills in backend development, data engineering, and modern web technologies.

---

## 🎯 **About This Project**

**DataLens** is a web application I built to learn and demonstrate full-stack development skills. The application allows users to:
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

## 📚 **Skills I Learned**

Through building this project, I gained hands-on experience with:

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

## 💡 **Learning & Usage**

This is a personal skill development project built to showcase my abilities for job applications. However, if you're learning full-stack development, feel free to:
- Explore the code structure
- Learn from the implementation
- Use it as a reference for your own projects

---

## 👩‍💻 **Developer**

**Arya Lakshmi M**  
GitHub: [https://github.com/22CB006](https://github.com/22CB006)  
Email: aryalakshmi.m2022csbs@sece.ac.in

*Built as a portfolio project to demonstrate full-stack development, data engineering, and modern web development skills.*

---

## 🎯 **Project Purpose**

This project was created to:
- Learn modern full-stack development practices
- Build a portfolio piece for job applications
- Demonstrate proficiency in Python, FastAPI, React, and data engineering
- Practice building production-ready applications

---

## 📧 **Contact**

For questions about the project or collaboration opportunities, feel free to reach out via GitHub or email.

---

**⭐ If you find this project helpful for learning, consider starring it!**
