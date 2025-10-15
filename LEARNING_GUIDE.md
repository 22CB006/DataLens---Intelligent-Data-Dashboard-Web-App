# DataLens — Learning Guide 🎓

This guide explains **what you'll learn** at each step and **why we're doing it**. Use this as your reference while building the project.

---

## 📚 **Table of Contents**

1. [Backend Development Concepts](#backend-development-concepts)
2. [Frontend Development Concepts](#frontend-development-concepts)
3. [Database & Data Modeling](#database--data-modeling)
4. [Data Processing & Analysis](#data-processing--analysis)
5. [Authentication & Security](#authentication--security)
6. [Testing & Quality Assurance](#testing--quality-assurance)
7. [Deployment & DevOps](#deployment--devops)
8. [Best Practices](#best-practices)

---

## 🔧 **Backend Development Concepts**

### **What is FastAPI?**
FastAPI is a modern Python web framework for building APIs. It's:
- **Fast**: Built on Starlette and Pydantic (high performance)
- **Type-safe**: Uses Python type hints for validation
- **Auto-documented**: Generates interactive API docs automatically
- **Async**: Supports async/await for concurrent operations

**Why FastAPI over Flask?**
- Better performance (comparable to Node.js)
- Built-in data validation
- Automatic API documentation (Swagger UI)
- Modern Python features (type hints, async)
- Better for data-heavy applications

### **REST API Principles**
REST (Representational State Transfer) is an architectural style for APIs:

**HTTP Methods:**
- `GET`: Retrieve data (read-only)
- `POST`: Create new resource
- `PUT/PATCH`: Update existing resource
- `DELETE`: Remove resource

**Status Codes:**
- `200`: Success
- `201`: Created
- `400`: Bad request (client error)
- `401`: Unauthorized
- `404`: Not found
- `500`: Server error

**Example:**
```python
@app.get("/api/v1/datasets/{dataset_id}")
async def get_dataset(dataset_id: str):
    # GET request to retrieve a specific dataset
    return {"id": dataset_id, "name": "Sales Data"}
```

### **Async/Await in Python**
Async programming allows handling multiple operations concurrently:

```python
# Synchronous (blocking)
def process_file():
    data = read_file()  # Waits here
    result = analyze_data(data)  # Then waits here
    return result

# Asynchronous (non-blocking)
async def process_file():
    data = await read_file()  # Can do other things while waiting
    result = await analyze_data(data)
    return result
```

**When to use async:**
- Database queries
- File I/O operations
- External API calls
- Multiple concurrent requests

### **Dependency Injection**
FastAPI's dependency injection system provides reusable components:

```python
# Define a dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validate token and return user
    return user

# Use in endpoint
@app.get("/api/v1/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    # current_user is automatically injected
    return current_user
```

**Benefits:**
- Code reusability
- Easier testing (can mock dependencies)
- Cleaner code structure
- Automatic validation

### **Pydantic Models**
Pydantic provides data validation using Python type hints:

```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr  # Validates email format
    password: str
    age: int  # Must be integer
    
# FastAPI automatically validates incoming data
@app.post("/users")
async def create_user(user: UserCreate):
    # user is guaranteed to be valid
    return user
```

---

## 🎨 **Frontend Development Concepts**

### **React Fundamentals**

**Components:**
React apps are built from reusable components:

```jsx
// Functional Component
function Button({ text, onClick }) {
    return <button onClick={onClick}>{text}</button>;
}

// Usage
<Button text="Click me" onClick={handleClick} />
```

**State Management:**
State is data that changes over time:

```jsx
import { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>
                Increment
            </button>
        </div>
    );
}
```

**Effects:**
Side effects (API calls, subscriptions) use `useEffect`:

```jsx
import { useEffect, useState } from 'react';

function UserProfile() {
    const [user, setUser] = useState(null);
    
    useEffect(() => {
        // Runs after component mounts
        fetchUser().then(data => setUser(data));
    }, []); // Empty array = run once
    
    return <div>{user?.name}</div>;
}
```

### **Component Lifecycle**

```
Mount → Update → Unmount

1. Mount: Component is created and added to DOM
   - Constructor runs
   - Render happens
   - useEffect runs

2. Update: State or props change
   - Re-render happens
   - useEffect runs (if dependencies changed)

3. Unmount: Component is removed
   - Cleanup functions run
```

### **Props vs State**

**Props (Properties):**
- Data passed from parent to child
- Read-only (immutable)
- Used for configuration

```jsx
<UserCard name="John" age={30} />
```

**State:**
- Internal component data
- Can be changed (mutable)
- Triggers re-render when updated

```jsx
const [name, setName] = useState("John");
```

### **React Hooks**

**Common Hooks:**

```jsx
// useState - manage state
const [count, setCount] = useState(0);

// useEffect - side effects
useEffect(() => {
    // Code here
}, [dependencies]);

// useContext - access context
const theme = useContext(ThemeContext);

// useMemo - memoize expensive calculations
const result = useMemo(() => expensiveCalc(data), [data]);

// useCallback - memoize functions
const handleClick = useCallback(() => {
    // Handler code
}, [dependencies]);
```

### **TailwindCSS**
Utility-first CSS framework:

```jsx
// Traditional CSS
<div className="card">
    <h1 className="title">Hello</h1>
</div>

// TailwindCSS
<div className="bg-white rounded-lg shadow-md p-4">
    <h1 className="text-2xl font-bold text-gray-800">Hello</h1>
</div>
```

**Benefits:**
- No need to write custom CSS
- Consistent design system
- Responsive design built-in
- Smaller bundle size (purges unused styles)

---

## 🗄️ **Database & Data Modeling**

### **Relational Database Concepts**

**Tables:**
Structured data storage with rows and columns:

```
Users Table:
+------+------------------+----------+
| id   | email            | username |
+------+------------------+----------+
| 1    | john@email.com   | john123  |
| 2    | jane@email.com   | jane456  |
+------+------------------+----------+
```

**Relationships:**

**One-to-Many:**
One user can have many datasets:
```
User (1) ──→ (Many) Datasets
```

**Many-to-Many:**
Many users can collaborate on many datasets:
```
Users (Many) ←→ (Many) Datasets
(Requires junction table)
```

### **SQL vs ORM**

**Raw SQL:**
```sql
SELECT * FROM users WHERE email = 'john@email.com';
```

**SQLAlchemy ORM:**
```python
user = db.query(User).filter(User.email == 'john@email.com').first()
```

**Benefits of ORM:**
- Type safety
- Database agnostic
- Prevents SQL injection
- Easier to maintain
- Python-native syntax

### **Database Migrations**
Track database schema changes over time:

```bash
# Create migration
alembic revision -m "add users table"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

**Why migrations?**
- Version control for database
- Team collaboration
- Safe schema updates
- Rollback capability

---

## 📊 **Data Processing & Analysis**

### **Pandas Fundamentals**

**DataFrame:**
2D labeled data structure (like Excel spreadsheet):

```python
import pandas as pd

# Create DataFrame
df = pd.DataFrame({
    'name': ['John', 'Jane', 'Bob'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000]
})

# Basic operations
df.head()           # First 5 rows
df.describe()       # Statistics
df['age'].mean()    # Average age
df[df['age'] > 25]  # Filter rows
```

**Common Operations:**

```python
# Reading data
df = pd.read_csv('data.csv')
df = pd.read_excel('data.xlsx')
df = pd.read_json('data.json')

# Data cleaning
df.dropna()                    # Remove missing values
df.fillna(0)                   # Fill missing with 0
df.drop_duplicates()           # Remove duplicates

# Data transformation
df['new_col'] = df['col1'] + df['col2']  # Create column
df.groupby('category').sum()              # Group and aggregate
df.sort_values('age', ascending=False)    # Sort

# Data analysis
df.corr()                      # Correlation matrix
df['col'].value_counts()       # Count unique values
df.pivot_table(...)            # Pivot table
```

### **NumPy Basics**

NumPy provides fast numerical operations:

```python
import numpy as np

# Arrays
arr = np.array([1, 2, 3, 4, 5])

# Operations
arr.mean()          # Average
arr.std()           # Standard deviation
arr.max()           # Maximum value
np.percentile(arr, 75)  # 75th percentile

# Mathematical operations
np.sqrt(arr)        # Square root
np.log(arr)         # Logarithm
arr ** 2            # Square
```

### **Statistical Analysis**

**Descriptive Statistics:**
```python
# Central tendency
mean = df['column'].mean()
median = df['column'].median()
mode = df['column'].mode()

# Dispersion
std = df['column'].std()
variance = df['column'].var()
range = df['column'].max() - df['column'].min()

# Distribution
quartiles = df['column'].quantile([0.25, 0.5, 0.75])
```

**Correlation Analysis:**
```python
# Pearson correlation (-1 to 1)
correlation = df.corr()

# Interpretation:
# 1.0: Perfect positive correlation
# 0.0: No correlation
# -1.0: Perfect negative correlation
```

**Outlier Detection:**
```python
# Z-score method
from scipy import stats
z_scores = np.abs(stats.zscore(df['column']))
outliers = df[z_scores > 3]  # Values > 3 std deviations

# IQR method
Q1 = df['column'].quantile(0.25)
Q3 = df['column'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['column'] < Q1 - 1.5*IQR) | 
              (df['column'] > Q3 + 1.5*IQR)]
```

---

## 🔐 **Authentication & Security**

### **JWT (JSON Web Tokens)**

**Structure:**
```
header.payload.signature

Example:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIn0.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

**How it works:**

1. **User logs in** with credentials
2. **Server validates** and creates JWT
3. **Client stores** JWT (localStorage/cookie)
4. **Client sends** JWT with each request
5. **Server verifies** JWT and grants access

**Benefits:**
- Stateless (no session storage needed)
- Scalable (works across multiple servers)
- Secure (signed and optionally encrypted)
- Self-contained (contains user info)

### **Password Hashing**

**Never store plain passwords!**

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed = pwd_context.hash("mypassword123")
# Result: $2b$12$KIXxLV...

# Verify password
is_valid = pwd_context.verify("mypassword123", hashed)
```

**Why bcrypt?**
- Slow by design (prevents brute force)
- Salted (unique hash for same password)
- Adaptive (can increase rounds over time)

### **CORS (Cross-Origin Resource Sharing)**

Allows frontend (different domain) to access backend:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Without CORS:**
```
Frontend (localhost:3000) → Backend (localhost:8000)
❌ Blocked by browser
```

**With CORS:**
```
Frontend (localhost:3000) → Backend (localhost:8000)
✅ Allowed
```

---

## 🧪 **Testing & Quality Assurance**

### **Types of Tests**

**Unit Tests:**
Test individual functions in isolation:

```python
def test_add_numbers():
    result = add(2, 3)
    assert result == 5
```

**Integration Tests:**
Test multiple components together:

```python
def test_user_registration():
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert "id" in response.json()
```

**End-to-End Tests:**
Test complete user flows:

```python
def test_complete_workflow():
    # 1. Register user
    # 2. Login
    # 3. Upload dataset
    # 4. Analyze data
    # 5. View results
```

### **Pytest Basics**

```python
import pytest

# Simple test
def test_example():
    assert 1 + 1 == 2

# Test with fixture
@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

def test_with_fixture(sample_data):
    assert len(sample_data) == 5

# Parametrized test
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert input ** 2 == expected
```

### **Test-Driven Development (TDD)**

1. **Write test first** (it fails)
2. **Write minimal code** to pass test
3. **Refactor** code
4. **Repeat**

**Benefits:**
- Better code design
- Fewer bugs
- Living documentation
- Confidence in changes

---

## 🚀 **Deployment & DevOps**

### **Docker Basics**

**Dockerfile:**
Instructions to build a container image:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

**Docker Compose:**
Define multi-container applications:

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - db
  
  db:
    image: postgres:14
    environment:
      POSTGRES_PASSWORD: password
```

**Benefits:**
- Consistent environments
- Easy deployment
- Isolation
- Reproducibility

### **CI/CD Pipeline**

**Continuous Integration:**
Automatically test code on every commit:

```yaml
# .github/workflows/test.yml
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest
```

**Continuous Deployment:**
Automatically deploy passing code:

```yaml
deploy:
  needs: test
  runs-on: ubuntu-latest
  steps:
    - name: Deploy to production
      run: ./deploy.sh
```

### **Environment Variables**

Never hardcode secrets!

```python
# ❌ Bad
DATABASE_URL = "postgresql://user:pass@localhost/db"

# ✅ Good
import os
DATABASE_URL = os.getenv("DATABASE_URL")
```

**`.env` file:**
```bash
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
DEBUG=False
```

---

## 💡 **Best Practices**

### **Code Organization**

**Separation of Concerns:**
```
app/
├── api/          # Routes (HTTP layer)
├── services/     # Business logic
├── models/       # Database models
├── schemas/      # Data validation
└── core/         # Configuration
```

**Single Responsibility:**
Each function/class should do one thing:

```python
# ❌ Bad - does too much
def process_user(data):
    validate_data(data)
    hash_password(data)
    save_to_db(data)
    send_email(data)

# ✅ Good - separate functions
def validate_user_data(data): ...
def hash_user_password(password): ...
def create_user(data): ...
def send_welcome_email(user): ...
```

### **Error Handling**

```python
# ❌ Bad - generic error
raise Exception("Something went wrong")

# ✅ Good - specific error
raise HTTPException(
    status_code=400,
    detail="Invalid email format"
)
```

### **Code Documentation**

```python
def calculate_statistics(data: pd.DataFrame) -> dict:
    """
    Calculate descriptive statistics for a dataset.
    
    Args:
        data: Pandas DataFrame containing numerical data
        
    Returns:
        Dictionary with mean, median, std, etc.
        
    Raises:
        ValueError: If DataFrame is empty
    """
    if data.empty:
        raise ValueError("DataFrame cannot be empty")
    
    return {
        "mean": data.mean(),
        "median": data.median(),
        "std": data.std()
    }
```

### **Git Commit Messages**

```bash
# ❌ Bad
git commit -m "fixed stuff"

# ✅ Good
git commit -m "feat: add user authentication with JWT"
git commit -m "fix: resolve file upload validation error"
git commit -m "docs: update API documentation"
```

**Commit Prefixes:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `style:` Formatting
- `perf:` Performance improvement

---

## 📖 **Learning Resources**

### **Official Documentation**
- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **Pandas**: https://pandas.pydata.org/docs/
- **PostgreSQL**: https://www.postgresql.org/docs/

### **Interactive Tutorials**
- **Python**: https://www.learnpython.org/
- **React**: https://react.dev/learn
- **SQL**: https://www.sqlzoo.net/

### **Video Courses**
- **FastAPI**: Search "FastAPI tutorial" on YouTube
- **React**: freeCodeCamp React course
- **Data Analysis**: Kaggle Learn courses

---

## 🎯 **Key Takeaways**

After completing this project, you'll understand:

✅ **Backend Development**
- REST API design
- Database modeling
- Authentication & security
- Async programming

✅ **Frontend Development**
- React component architecture
- State management
- API integration
- Modern UI/UX

✅ **Data Engineering**
- Data processing pipelines
- Statistical analysis
- Data visualization
- ETL processes

✅ **DevOps**
- Docker containerization
- CI/CD pipelines
- Cloud deployment
- Environment management

✅ **Software Engineering**
- Clean code principles
- Testing strategies
- Version control
- Documentation

---

**Remember:** Learning by building is the best way to master these concepts. Don't worry if you don't understand everything at first—it will make sense as you build! 🚀

**Next Step:** Start with [PROJECT_PLAN.md](PROJECT_PLAN.md) Phase 1, Milestone 1.2!
