# Getting Started with DataLens 🚀

This guide will help you set up your development environment and start building DataLens.

---

## 📋 **Prerequisites**

Before starting, ensure you have the following installed:

### **Required Software**
- ✅ **Python 3.11+** - [Download](https://www.python.org/downloads/)
- ✅ **Node.js 18+** - [Download](https://nodejs.org/)
- ✅ **PostgreSQL 14+** - [Download](https://www.postgresql.org/download/)
- ✅ **Git** - [Download](https://git-scm.com/downloads)
- ✅ **VS Code** (recommended) - [Download](https://code.visualstudio.com/)

### **Verify Installation**
```bash
# Check Python version
python --version  # Should be 3.11 or higher

# Check Node.js version
node --version    # Should be 18 or higher

# Check PostgreSQL
psql --version    # Should be 14 or higher

# Check Git
git --version
```

---

## 🔧 **Initial Setup**

### **Step 1: Clone Repository**
```bash
# If you haven't already
git clone https://github.com/22CB006/DataLens_Intelligent-Data-Dashboard-Web-App.git
cd DataLens_Intelligent-Data-Dashboard-Web-App
```

### **Step 2: Configure Git (First Time Only)**
```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify
git config --list
```

### **Step 3: GitHub Authentication**

**Option 1: Personal Access Token (Recommended)**
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `workflow`
4. Copy the token
5. When pushing, use token as password

**Option 2: SSH Key**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub → Settings → SSH and GPG keys
```

---

## 🐍 **Backend Setup (Phase 1)**

### **Step 1: Create Backend Structure**
```bash
# Create directories
mkdir -p backend/app/api
mkdir -p backend/app/core
mkdir -p backend/app/models
mkdir -p backend/app/schemas
mkdir -p backend/app/services
mkdir -p backend/tests
```

### **Step 2: Create Virtual Environment**
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# You should see (venv) in your terminal
```

### **Step 3: Create requirements.txt**
Create `backend/requirements.txt`:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pandas==2.1.3
numpy==1.26.2
python-dotenv==1.0.0
alembic==1.13.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

### **Step 4: Install Dependencies**
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt

# Verify installation
pip list
```

### **Step 5: Create .env File**
Create `backend/.env`:
```bash
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/datalens

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# File Upload
MAX_FILE_SIZE=52428800
UPLOAD_DIR=./uploads
```

### **Step 6: Setup PostgreSQL Database**
```bash
# Open PostgreSQL command line
psql -U postgres

# Create database
CREATE DATABASE datalens;

# Verify
\l

# Exit
\q
```

---

## ⚛️ **Frontend Setup (Phase 2)**

### **Step 1: Create React App**
```bash
# From project root
npm create vite@latest frontend -- --template react

cd frontend
```

### **Step 2: Install Dependencies**
```bash
# Core dependencies
npm install

# Additional packages
npm install react-router-dom axios
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### **Step 3: Configure TailwindCSS**
Update `frontend/tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Update `frontend/src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### **Step 4: Create .env File**
Create `frontend/.env`:
```bash
VITE_API_URL=http://localhost:8000
VITE_MAX_FILE_SIZE=52428800
```

---

## 🚀 **Running the Application**

### **Backend**
```bash
cd backend

# Activate virtual environment (if not already)
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run server
uvicorn app.main:app --reload

# Server will start at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### **Frontend**
```bash
cd frontend

# Run development server
npm run dev

# Server will start at http://localhost:5173
```

---

## 📁 **Project Structure Overview**

```
DataLens/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   ├── core/              # Core configs
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   └── main.py            # App entry point
│   ├── tests/                 # Backend tests
│   ├── uploads/               # Uploaded files
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   └── venv/                  # Virtual environment
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   ├── App.jsx            # Main app component
│   │   └── main.jsx           # Entry point
│   ├── package.json           # Node dependencies
│   └── .env                   # Environment variables
│
├── docs/                       # Documentation
├── .gitignore                 # Git ignore rules
├── README.md                  # Project overview
├── PROJECT_PLAN.md            # Development roadmap
├── ARCHITECTURE.md            # System architecture
└── LEARNING_GUIDE.md          # Learning resources
```

---

## 🧪 **Testing Your Setup**

### **Backend Health Check**
1. Start backend server
2. Open browser: http://localhost:8000/docs
3. You should see FastAPI Swagger UI

### **Frontend Check**
1. Start frontend server
2. Open browser: http://localhost:5173
3. You should see React app

---

## 🔍 **Troubleshooting**

### **Python Issues**
```bash
# If python command not found, try:
python3 --version

# If pip not working:
python -m pip install --upgrade pip
```

### **PostgreSQL Connection Issues**
```bash
# Check if PostgreSQL is running
# Windows:
# Open Services → PostgreSQL should be running

# Mac:
brew services list

# Linux:
sudo systemctl status postgresql
```

### **Port Already in Use**
```bash
# Backend (8000)
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Frontend (5173)
# Change port in vite.config.js or kill process
```

### **Module Not Found Errors**
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

---

## 📚 **Next Steps**

Now that your environment is set up, follow the development plan:

1. ✅ **Read** [PROJECT_PLAN.md](PROJECT_PLAN.md) for detailed roadmap
2. ✅ **Study** [LEARNING_GUIDE.md](LEARNING_GUIDE.md) for concepts
3. ✅ **Review** [ARCHITECTURE.md](ARCHITECTURE.md) for system design
4. ✅ **Start** with Phase 1, Milestone 1.2: Backend Setup

---

## 🎯 **Development Workflow**

### **Daily Workflow**
1. Pull latest changes: `git pull`
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes and test
4. Commit: `git commit -m "feat: your feature"`
5. Push: `git push origin feature/your-feature`
6. Create Pull Request on GitHub

### **Commit Message Format**
```bash
feat: add new feature
fix: fix bug
docs: update documentation
test: add tests
refactor: refactor code
style: format code
perf: improve performance
```

---

## 💡 **Tips for Success**

1. **Read documentation first** before coding
2. **Test frequently** as you build
3. **Commit often** with meaningful messages
4. **Ask questions** when stuck (Google, Stack Overflow, ChatGPT)
5. **Take breaks** to avoid burnout
6. **Document your learning** in comments

---

## 🆘 **Getting Help**

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **Stack Overflow**: Search for specific errors
- **GitHub Issues**: Report bugs or ask questions

---

## ✅ **Checklist Before Starting**

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] PostgreSQL 14+ installed
- [ ] Git configured
- [ ] GitHub authentication setup
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] PostgreSQL database created
- [ ] Frontend dependencies installed
- [ ] Both servers can start successfully

---

**You're all set! Let's start building! 🚀**

**Next:** Open [PROJECT_PLAN.md](PROJECT_PLAN.md) and begin with **Phase 1, Milestone 1.2: Backend Setup**
