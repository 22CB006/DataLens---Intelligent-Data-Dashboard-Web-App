# Phase 3 Testing Checklist

## ✅ Pre-Testing Setup

### 1. Install Dependencies
```bash
cd backend
pip install scipy==1.11.4 openpyxl==3.1.2 aiofiles==23.2.1
```

### 2. Start Server
```bash
uvicorn app.main:app --reload
```

### 3. Check Console Output
Look for:
```
🚀 DataLens API v1.0.0 starting up...
📁 Upload directory ready: ...
```

---

## 🧪 Testing Sequence

### Step 1: Get JWT Token

1. Go to http://localhost:8000/docs
2. Find `POST /api/v1/auth/login`
3. Login with your credentials
4. Copy the `access_token`
5. Click **Authorize** button (top right)
6. Paste token
7. Click **Authorize**

---

### Step 2: Upload Dataset

**Endpoint:** `POST /api/v1/datasets/upload`

1. Click "Try it out"
2. Choose a CSV file (or create one)
3. Execute

**Sample CSV to test:**
```csv
date,product,sales,quantity,region
2024-01-01,Widget A,1250.50,10,North
2024-01-02,Widget B,980.00,8,South
2024-01-03,Widget A,1450.00,12,East
2024-01-04,Widget C,2100.00,15,West
2024-01-05,Widget B,1200.00,9,North
```

**Expected:** 201 Created with dataset metadata

---

### Step 3: List Datasets

**Endpoint:** `GET /api/v1/datasets/?skip=0&limit=10`

**Expected:** Array of your datasets

---

### Step 4: Preview Dataset

**Endpoint:** `GET /api/v1/datasets/{dataset_id}/preview?rows=5`

Replace `{dataset_id}` with ID from upload response

**Expected:** First 5 rows of data

---

### Step 5: Get Dataset Info

**Endpoint:** `GET /api/v1/datasets/{dataset_id}/info`

**Expected:** Detailed metadata with column types

---

### Step 6: Get Statistics

**Endpoint:** `GET /api/v1/analysis/{dataset_id}/statistics`

**Expected:** Statistics for numeric columns (sales, quantity)

---

### Step 7: Correlation Analysis

**Endpoint:** `GET /api/v1/analysis/{dataset_id}/correlation?method=pearson`

**Expected:** Correlation matrix

---

### Step 8: Outlier Detection

**Endpoint:** `GET /api/v1/analysis/{dataset_id}/outliers?method=iqr&threshold=1.5`

**Expected:** Outliers for each numeric column

---

### Step 9: Generate Bar Chart

**Endpoint:** `POST /api/v1/analysis/{dataset_id}/visualize/bar`

**Parameters:**
- x_column: region
- y_column: sales
- aggregation: sum
- limit: 10

**Expected:** Chart data with labels and values

---

### Step 10: Generate Histogram

**Endpoint:** `POST /api/v1/analysis/{dataset_id}/visualize/histogram`

**Parameters:**
- column: sales
- bins: 10

**Expected:** Histogram data with bin ranges

---

### Step 11: Chart Suggestion

**Endpoint:** `GET /api/v1/analysis/{dataset_id}/visualize/suggest`

**Parameters:**
- x_column: date
- y_column: sales

**Expected:** Suggested chart type (probably "line")

---

### Step 12: Delete Dataset

**Endpoint:** `DELETE /api/v1/datasets/{dataset_id}`

**Expected:** 204 No Content

---

## ✅ Success Criteria

- [ ] All endpoints return 200/201/204 (not 500)
- [ ] Upload creates file in uploads/ directory
- [ ] Preview shows correct data
- [ ] Statistics calculated correctly
- [ ] Correlation matrix is symmetric
- [ ] Outliers detected
- [ ] Chart data is JSON-serializable
- [ ] Delete removes file and database record

---

## 🐛 Troubleshooting

### Error: "scipy not found"
```bash
pip install scipy==1.11.4
```

### Error: "openpyxl not found"
```bash
pip install openpyxl==3.1.2
```

### Error: "No such file or directory: uploads"
- Restart server (it creates automatically)
- Or manually: `mkdir uploads`

### Error: "Dataset not found"
- Check dataset_id is correct
- Verify you own the dataset

### Error: "Not authorized"
- Re-authorize with fresh token
- Check token hasn't expired

---

## 📊 All Endpoints Summary

**Total: 18 new endpoints**

### Datasets (6)
- ✅ POST /upload
- ✅ GET /
- ✅ GET /{id}
- ✅ DELETE /{id}
- ✅ GET /{id}/preview
- ✅ GET /{id}/info

### Analysis (5)
- ✅ GET /{id}/statistics
- ✅ GET /{id}/correlation
- ✅ GET /{id}/outliers
- ✅ GET /{id}/trends
- ✅ GET /{id}/summary

### Visualization (7)
- ✅ POST /{id}/visualize/bar
- ✅ POST /{id}/visualize/line
- ✅ POST /{id}/visualize/pie
- ✅ POST /{id}/visualize/scatter
- ✅ GET /{id}/visualize/heatmap
- ✅ POST /{id}/visualize/histogram
- ✅ GET /{id}/visualize/suggest

---

## 🎉 If All Tests Pass

**You're ready for Phase 4: Frontend Development!**

Commit your code:
```bash
git add .
git commit -m "feat: complete Phase 3 - data processing and analysis"
git push origin main
```

---

**Happy Testing!** 🚀
