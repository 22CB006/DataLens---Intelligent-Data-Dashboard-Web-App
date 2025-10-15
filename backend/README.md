# DataLens Backend 🔧

FastAPI-based backend for the DataLens application.

---

## 📁 **Project Structure**

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/                 # API route handlers
│   │   └── __init__.py
│   ├── core/                # Core configuration
│   │   ├── __init__.py
│   │   └── config.py        # Application settings
│   ├── models/              # Database models (SQLAlchemy)
│   │   └── __init__.py
│   ├── schemas/             # Pydantic schemas (request/response)
│   │   └── __init__.py
│   └── services/            # Business logic
│       └── __init__.py
├── tests/                   # Unit and integration tests
│   └── __init__.py
├── uploads/                 # Uploaded files storage
│   └── .gitkeep
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
└── .gitignore              # Git ignore rules
```

---

## 🚀 **Setup Instructions**

### **1. Create Virtual Environment**
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Configure Environment Variables**
```bash
# Copy example env file
cp .env.example .env

# Edit .env file with your settings
# IMPORTANT: Change SECRET_KEY in production!
```

### **4. Setup Database**
```bash
# Create PostgreSQL database
createdb datalens

# Or using psql:
psql -U postgres
CREATE DATABASE datalens;
\q
```

### **5. Run the Application**
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📚 **What We've Built So Far**

### **✅ Milestone 1.2: Backend Setup - COMPLETED**

#### **Files Created:**
1. **`requirements.txt`** - Python dependencies
2. **`.env.example`** - Environment variable template
3. **`app/core/config.py`** - Configuration management
4. **`app/main.py`** - FastAPI application

#### **What You Learned:**

**1. Pydantic Settings (`config.py`)**
- Environment variable management
- Type-safe configuration
- Automatic validation
- Default values

```python
from app.core.config import settings
print(settings.DATABASE_URL)  # Loaded from .env
```

**2. FastAPI Application (`main.py`)**
- FastAPI initialization
- CORS middleware for frontend access
- Basic endpoints (/, /health)
- Startup/shutdown events
- Auto-generated API documentation

**3. Project Structure**
- Modular folder organization
- Separation of concerns
- Scalable architecture

**4. Virtual Environment**
- Isolated Python environment
- Dependency management
- Reproducible setup

---

## 🧪 **Testing the Setup**

### **Test 1: Check if server starts**
```bash
uvicorn app.main:app --reload
```

Expected output:
```
🚀 DataLens v1.0.0 starting up...
📚 API Documentation: http://localhost:8000/docs
🔧 Debug mode: True
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### **Test 2: Access root endpoint**
Open browser: http://localhost:8000

Expected response:
```json
{
  "message": "Welcome to DataLens API",
  "status": "online",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### **Test 3: View API documentation**
Open browser: http://localhost:8000/docs

You should see:
- Interactive Swagger UI
- List of available endpoints
- Ability to test endpoints

### **Test 4: Health check**
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "app_name": "DataLens",
  "version": "1.0.0"
}
```

---

## 🔍 **Understanding the Code**

### **Configuration Management (`config.py`)**

```python
class Settings(BaseSettings):
    DATABASE_URL: str  # Required field
    SECRET_KEY: str    # Required field
    DEBUG: bool = True # Optional with default
```

**How it works:**
1. Pydantic reads `.env` file
2. Validates each field type
3. Raises error if required field missing
4. Provides defaults for optional fields

**Benefits:**
- Type safety (catches errors early)
- Centralized configuration
- Easy to test (can override settings)
- Auto-completion in IDE

### **FastAPI Application (`main.py`)**

```python
app = FastAPI(
    title="DataLens",
    version="1.0.0",
    docs_url="/docs"
)
```

**What this does:**
- Creates FastAPI instance
- Configures metadata
- Enables auto-documentation
- Sets up OpenAPI schema

**CORS Middleware:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Why we need CORS:**
- Frontend runs on different port (e.g., 3000)
- Browser blocks cross-origin requests by default
- CORS middleware allows specific origins
- Required for API access from frontend

---

## 📖 **Key Concepts Explained**

### **1. Async/Await**
```python
@app.get("/")
async def root():
    return {"message": "Hello"}
```

- `async def` = asynchronous function
- Can handle multiple requests concurrently
- Better performance for I/O operations
- Use `await` for async operations

### **2. Dependency Injection**
```python
@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    # db is automatically injected
    return db.query(User).all()
```

- FastAPI automatically provides dependencies
- Reusable across endpoints
- Easy to test (mock dependencies)
- Clean code structure

### **3. Type Hints**
```python
def process_data(data: dict) -> dict:
    return data
```

- Specifies expected types
- FastAPI uses for validation
- Better IDE support
- Self-documenting code

---

## 🎯 **Next Steps**

### **Milestone 1.3: API Router Structure**

We'll create:
1. `app/api/deps.py` - Shared dependencies
2. `app/api/auth.py` - Authentication routes
3. `app/api/datasets.py` - Dataset routes
4. `app/api/analysis.py` - Analysis routes

This will give us:
- Modular route organization
- API versioning (/api/v1/)
- Cleaner code structure
- Easier maintenance

---

## 🐛 **Troubleshooting**

### **Issue: Module not found**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### **Issue: Port already in use**
```bash
# Solution: Use different port
uvicorn app.main:app --reload --port 8001

# Or kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### **Issue: .env file not loaded**
```bash
# Solution: Check file name (should be .env, not .env.txt)
# Check it's in backend/ directory
# Verify python-dotenv is installed
```

### **Issue: Import errors**
```bash
# Solution: Make sure you're in backend/ directory
cd backend

# And virtual environment is activated
venv\Scripts\activate
```

---

## 📝 **Development Tips**

1. **Always activate virtual environment** before working
2. **Use `--reload` flag** during development (auto-restarts on changes)
3. **Check API docs** at /docs to test endpoints
4. **Read error messages** carefully - FastAPI gives helpful errors
5. **Use type hints** - helps catch bugs early

---

## 🎓 **Learning Resources**

- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **Pydantic Docs**: https://docs.pydantic.dev/
- **Python Async**: https://realpython.com/async-io-python/

---

**Great job! You've completed Milestone 1.2! 🎉**

**Next:** Continue to Milestone 1.3 - API Router Structure
