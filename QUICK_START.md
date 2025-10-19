# DataLens - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### **Step 1: Install Dependencies** (1 min)

```bash
cd backend
pip install scipy==1.11.4 openpyxl==3.1.2 aiofiles==23.2.1
```

### **Step 2: Start Server** (30 sec)

```bash
uvicorn app.main:app --reload
```

### **Step 3: Open API Docs** (10 sec)

Visit: **http://localhost:8000/docs**

### **Step 4: Register & Login** (1 min)

1. Find `POST /api/v1/auth/register`
2. Register a new user
3. Find `POST /api/v1/auth/login`
4. Login and copy the `access_token`
5. Click **Authorize** button (🔒 top right)
6. Paste token and click **Authorize**

### **Step 5: Upload Dataset** (1 min)

1. Find `POST /api/v1/datasets/upload`
2. Click "Try it out"
3. Upload `sample_data.csv`
4. Copy the `id` from response

### **Step 6: Analyze Data** (1 min)

1. Find `GET /api/v1/analysis/{dataset_id}/statistics`
2. Paste your dataset ID
3. Execute
4. See statistics! 📊

---

## 🎯 Common Tasks

### **Upload a CSV File**
```
POST /api/v1/datasets/upload
File: sample_data.csv
```

### **Get Statistics**
```
GET /api/v1/analysis/{id}/statistics
```

### **Generate Bar Chart**
```
POST /api/v1/analysis/{id}/visualize/bar
  ?x_column=region
  &y_column=sales
  &aggregation=sum
```

### **Detect Outliers**
```
GET /api/v1/analysis/{id}/outliers
  ?method=iqr
  &threshold=1.5
```

---

## 📊 All Endpoints (27 Total)

### **Auth (3)**
- `POST /auth/register` - Register
- `POST /auth/login` - Login
- `GET /auth/me` - Profile

### **Users (6)**
- `GET /users/` - List (admin)
- `GET /users/me` - My profile
- `PUT /users/me` - Update
- `DELETE /users/me` - Delete
- `GET /users/{id}` - Get user
- `DELETE /users/{id}` - Delete (admin)

### **Datasets (6)**
- `POST /datasets/upload` - Upload
- `GET /datasets/` - List
- `GET /datasets/{id}` - Get
- `DELETE /datasets/{id}` - Delete
- `GET /datasets/{id}/preview` - Preview
- `GET /datasets/{id}/info` - Info

### **Analysis (5)**
- `GET /analysis/{id}/statistics` - Stats
- `GET /analysis/{id}/correlation` - Correlation
- `GET /analysis/{id}/outliers` - Outliers
- `GET /analysis/{id}/trends` - Trends
- `GET /analysis/{id}/summary` - Summary

### **Visualization (7)**
- `POST /analysis/{id}/visualize/bar` - Bar
- `POST /analysis/{id}/visualize/line` - Line
- `POST /analysis/{id}/visualize/pie` - Pie
- `POST /analysis/{id}/visualize/scatter` - Scatter
- `GET /analysis/{id}/visualize/heatmap` - Heatmap
- `POST /analysis/{id}/visualize/histogram` - Histogram
- `GET /analysis/{id}/visualize/suggest` - Suggest

---

## 🔑 Environment Variables

Create `.env` in `backend/`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/datalens

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# App
APP_NAME=DataLens API
APP_VERSION=1.0.0
DEBUG=True
```

---

## 🐛 Troubleshooting

### **Server won't start**
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <PID> /F
```

### **Database connection error**
```bash
# Check PostgreSQL is running
# Verify DATABASE_URL in .env
# Test connection:
psql -U postgres -d datalens
```

### **Import errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### **Upload fails**
```bash
# Check uploads/ directory exists
# Server creates it automatically
# Or manually: mkdir uploads
```

---

## 📝 Sample Data

Use `sample_data.csv` for testing:
- 30 rows
- 6 columns (date, product, sales, quantity, region, customer_satisfaction)
- Perfect for all analysis types

---

## 🎯 Testing Checklist

- [ ] Server starts without errors
- [ ] Can register new user
- [ ] Can login and get token
- [ ] Can upload CSV file
- [ ] Can list datasets
- [ ] Can preview data
- [ ] Can get statistics
- [ ] Can generate charts
- [ ] Can delete dataset

---

## 🚀 Next: Phase 4

**Frontend Development**
- React + TypeScript
- TailwindCSS
- Interactive charts
- File upload UI
- Real-time dashboards

---

## 📚 Documentation

- **API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Complete Guide:** `PHASE_3_COMPLETE.md`
- **Testing:** `TEST_PHASE_3.md`

---

## 🎉 You're Ready!

**27 endpoints. 60% complete. Let's go!** 🚀
