# DataLens — Quick Reference Guide 📝

Quick commands and references for common tasks during development.

---

## 🚀 **Quick Start Commands**

### **Start Development Servers**
```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate  # Windows
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### **Access Applications**
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

---

## 🐍 **Backend Commands**

### **Virtual Environment**
```bash
# Create
python -m venv venv

# Activate
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Deactivate
deactivate
```

### **Dependencies**
```bash
# Install all
pip install -r requirements.txt

# Add new package
pip install package-name
pip freeze > requirements.txt

# Update all packages
pip install --upgrade -r requirements.txt
```

### **Database Migrations**
```bash
# Create migration
alembic revision -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

### **Testing**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_register_user

# Verbose output
pytest -v
```

### **Code Quality**
```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

---

## ⚛️ **Frontend Commands**

### **Development**
```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### **Dependencies**
```bash
# Install all
npm install

# Add new package
npm install package-name

# Add dev dependency
npm install -D package-name

# Update packages
npm update

# Remove package
npm uninstall package-name
```

### **Testing**
```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

### **Linting**
```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint -- --fix
```

---

## 🗄️ **Database Commands**

### **PostgreSQL**
```bash
# Connect to database
psql -U postgres -d datalens

# List databases
\l

# Connect to database
\c datalens

# List tables
\dt

# Describe table
\d table_name

# Run SQL file
\i path/to/file.sql

# Exit
\q
```

### **Common SQL Queries**
```sql
-- View all users
SELECT * FROM users;

-- Count records
SELECT COUNT(*) FROM datasets;

-- Delete all data (careful!)
TRUNCATE TABLE table_name CASCADE;

-- Drop database (careful!)
DROP DATABASE datalens;

-- Create database
CREATE DATABASE datalens;
```

---

## 🔧 **Git Commands**

### **Basic Workflow**
```bash
# Check status
git status

# Add files
git add .
git add specific-file.py

# Commit
git commit -m "feat: add feature"

# Push
git push origin main

# Pull latest
git pull
```

### **Branching**
```bash
# Create new branch
git checkout -b feature/feature-name

# Switch branch
git checkout branch-name

# List branches
git branch

# Delete branch
git branch -d branch-name

# Merge branch
git checkout main
git merge feature/feature-name
```

### **Undo Changes**
```bash
# Discard changes in file
git checkout -- filename

# Unstage file
git reset HEAD filename

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

### **View History**
```bash
# View commit history
git log

# View compact history
git log --oneline

# View changes
git diff
```

---

## 📦 **Docker Commands**

### **Build & Run**
```bash
# Build image
docker build -t datalens-backend ./backend

# Run container
docker run -p 8000:8000 datalens-backend

# Run with environment file
docker run --env-file .env -p 8000:8000 datalens-backend
```

### **Docker Compose**
```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# Rebuild images
docker-compose build
```

### **Container Management**
```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop container-id

# Remove container
docker rm container-id

# View logs
docker logs container-id
```

---

## 🧪 **Testing Endpoints**

### **Using curl**
```bash
# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","username":"testuser"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Get profile (with token)
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### **Using Python requests**
```python
import requests

# Register
response = requests.post(
    "http://localhost:8000/api/v1/auth/register",
    json={
        "email": "test@example.com",
        "password": "password123",
        "username": "testuser"
    }
)
print(response.json())

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "email": "test@example.com",
        "password": "password123"
    }
)
token = response.json()["access_token"]

# Get profile
response = requests.get(
    "http://localhost:8000/api/v1/auth/me",
    headers={"Authorization": f"Bearer {token}"}
)
print(response.json())
```

---

## 🐛 **Debugging**

### **Backend Debugging**
```python
# Add print statements
print(f"Variable value: {variable}")

# Use debugger
import pdb; pdb.set_trace()

# Logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
```

### **Frontend Debugging**
```javascript
// Console logging
console.log('Variable:', variable);
console.error('Error:', error);
console.table(arrayOfObjects);

// Debugger
debugger;

// React DevTools
// Install React DevTools browser extension
```

---

## 📊 **Useful Python Snippets**

### **Pandas Quick Reference**
```python
import pandas as pd

# Read data
df = pd.read_csv('file.csv')
df = pd.read_excel('file.xlsx')
df = pd.read_json('file.json')

# Basic info
df.head()           # First 5 rows
df.tail()           # Last 5 rows
df.info()           # Column info
df.describe()       # Statistics
df.shape            # (rows, columns)

# Selection
df['column']        # Single column
df[['col1', 'col2']]  # Multiple columns
df[df['age'] > 25]  # Filter rows

# Operations
df.mean()           # Average
df.sum()            # Sum
df.groupby('col').sum()  # Group by
df.sort_values('col')    # Sort
```

### **FastAPI Quick Reference**
```python
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

# GET endpoint
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# POST endpoint
@app.post("/items")
async def create_item(item: Item):
    return item

# With dependency
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Error handling
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

---

## ⚛️ **React Quick Reference**

### **Component Basics**
```jsx
import { useState, useEffect } from 'react';

function MyComponent() {
    // State
    const [count, setCount] = useState(0);
    
    // Effect
    useEffect(() => {
        // Runs after render
        console.log('Component mounted');
        
        return () => {
            // Cleanup
            console.log('Component unmounted');
        };
    }, []); // Dependencies
    
    // Event handler
    const handleClick = () => {
        setCount(count + 1);
    };
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={handleClick}>Increment</button>
        </div>
    );
}
```

### **API Calls**
```javascript
import axios from 'axios';

// GET request
const fetchData = async () => {
    try {
        const response = await axios.get('/api/data');
        console.log(response.data);
    } catch (error) {
        console.error('Error:', error);
    }
};

// POST request
const createData = async (data) => {
    try {
        const response = await axios.post('/api/data', data);
        console.log(response.data);
    } catch (error) {
        console.error('Error:', error);
    }
};
```

---

## 🔐 **Environment Variables**

### **Backend (.env)**
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/datalens
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=["http://localhost:3000"]
MAX_FILE_SIZE=52428800
```

### **Frontend (.env)**
```bash
VITE_API_URL=http://localhost:8000
VITE_MAX_FILE_SIZE=52428800
```

---

## 📝 **Commit Message Convention**

```bash
feat: add new feature
fix: fix bug
docs: update documentation
style: format code (no code change)
refactor: refactor code
test: add or update tests
chore: update dependencies
perf: improve performance
ci: update CI/CD
build: update build system
```

**Examples:**
```bash
git commit -m "feat: add user authentication"
git commit -m "fix: resolve file upload error"
git commit -m "docs: update API documentation"
git commit -m "test: add unit tests for auth service"
```

---

## 🆘 **Common Issues & Solutions**

### **Port Already in Use**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### **Module Not Found**
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### **Database Connection Error**
```bash
# Check PostgreSQL is running
# Windows: Services → PostgreSQL
# Mac: brew services list
# Linux: sudo systemctl status postgresql

# Check connection string in .env
DATABASE_URL=postgresql://postgres:password@localhost:5432/datalens
```

### **CORS Error**
```python
# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📚 **Useful Links**

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **Pandas Docs**: https://pandas.pydata.org/docs/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **TailwindCSS Docs**: https://tailwindcss.com/docs
- **Axios Docs**: https://axios-http.com/docs/intro

---

**Keep this file handy for quick reference during development! 🚀**
