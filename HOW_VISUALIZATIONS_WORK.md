# How DataLens Visualizations Work

## 🎯 Overview
All visualizations in DataLens are **100% dynamic** - they're generated from your actual CSV data using statistical analysis on the backend. Nothing is hardcoded!

---

## 📊 Data Flow Architecture

```
Your CSV File
    ↓
Backend Analysis (Python/Pandas)
    ↓
Statistical Calculations
    ↓
REST API Endpoints
    ↓
Frontend (React)
    ↓
Chart.js Visualizations
```

---

## 🔍 How Each Tab Works

### 1. **Overview Tab** 📈

**What You See:**
- Mean vs Median Comparison (Bar Chart)
- Standard Deviation by Column (Bar Chart)
- Min-Max Range by Column (Bar Chart)
- Data Count Distribution (Pie Chart)
- Distribution Histograms

**How It Works:**
1. **Backend**: When you upload a CSV, the backend reads it using Pandas
2. **Calculation**: For each numeric column, it calculates:
   - `mean` = average value
   - `median` = middle value
   - `std` = standard deviation (data spread)
   - `min/max` = smallest/largest values
   - `count` = number of data points
   - `quartiles` (Q25, Q50, Q75)
   - `skewness` = data asymmetry
   - `kurtosis` = tail heaviness

3. **API Endpoint**: `GET /api/v1/analysis/{dataset_id}/statistics`
4. **Response Format**:
```json
{
  "statistics": {
    "column_name": {
      "mean": 104.5,
      "median": 104.5,
      "std": 2.45,
      "min": 101.0,
      "max": 108.0,
      ...
    }
  },
  "distributions": {
    "column_name": {
      "labels": ["101.88", "103.62", ...],
      "values": [2, 2, 2, 2],
      "bins": 4
    }
  }
}
```

5. **Frontend**: React components use Chart.js to render the data

**Example from Your Data:**
- Your CSV has columns: `user_id`, `sessions`, `avg_session_time_min`, etc.
- Backend calculates: sessions mean = 28.25, median = 26.0
- Frontend displays these in bar charts

---

### 2. **Correlation Tab** 🔗

**What You See:**
- Correlation Heatmap (Color-coded matrix)
- Strong Correlations Table
- Correlation Strength Bar Chart

**How It Works:**
1. **Backend**: Uses Pandas `.corr()` method
2. **Calculation**: Pearson correlation coefficient between every pair of columns
   - Values range from -1 to 1
   - +1 = perfect positive correlation
   - -1 = perfect negative correlation
   - 0 = no correlation

3. **API Endpoint**: `GET /api/v1/analysis/{dataset_id}/correlation`
4. **Response Format**:
```json
{
  "matrix": {
    "sessions": {
      "sessions": 1.0,
      "pages_visited": 0.995,
      "conversion_rate": 0.967
    },
    "pages_visited": {
      "sessions": 0.995,
      "pages_visited": 1.0,
      ...
    }
  },
  "columns": ["sessions", "pages_visited", ...],
  "strong_correlations": [
    {
      "column1": "sessions",
      "column2": "pages_visited",
      "correlation": 0.995,
      "strength": "strong positive"
    }
  ]
}
```

5. **Frontend**: 
   - Heatmap component converts object matrix to 2D array
   - Colors cells based on correlation value
   - Blue = positive, Red = negative

**Example from Your Data:**
- `sessions` and `pages_visited` have 0.995 correlation
- This means: when sessions increase, pages visited also increase (almost perfectly)

---

### 3. **Outliers Tab** ⚠️

**What You See:**
- Outliers by Column (Bar Chart)
- Outlier Distribution (Pie Chart)
- Outlier Detection Details

**How It Works:**
1. **Backend**: Uses IQR (Interquartile Range) method
2. **Calculation**:
   ```python
   Q1 = 25th percentile
   Q3 = 75th percentile
   IQR = Q3 - Q1
   Lower Bound = Q1 - 1.5 * IQR
   Upper Bound = Q3 + 1.5 * IQR
   Outliers = values < Lower Bound OR values > Upper Bound
   ```

3. **API Endpoint**: `GET /api/v1/analysis/{dataset_id}/outliers`
4. **Response Format**:
```json
{
  "column_name": {
    "count": 0,
    "percentage": 0.0,
    "method": "iqr",
    "lower_bound": 10.0,
    "upper_bound": 54.0,
    "values": []
  }
}
```

5. **Frontend**: Displays outlier counts and details

**Example from Your Data:**
- Your data has no outliers (all values within normal range)
- If you had a session count of 500 when others are 10-54, it would be flagged

---

### 4. **Trends Tab** 📈 (NEW!)

**What You See:**
- Trend Direction (increasing/decreasing/stable)
- Slope and R² values
- Trend Line Charts

**How It Works:**
1. **Backend**: Uses linear regression to find trends
2. **Calculation**:
   - Fits a line through data points
   - Calculates slope (rate of change)
   - Calculates R² (how well the line fits)

3. **API Endpoint**: `GET /api/v1/analysis/{dataset_id}/trends`
4. **Response Format**:
```json
{
  "column_name": {
    "trend": {
      "direction": "increasing",
      "slope": 0.5,
      "r_squared": 0.85
    },
    "values": [10, 15, 20, 25, 30]
  }
}
```

5. **Frontend**: Line charts show the trend over time

**Note**: Trends work best with time-series data (data collected over time)

---

### 5. **Data Preview Tab** 👁️

**What You See:**
- Raw data table (first 10 rows)
- Column names and values

**How It Works:**
1. **Backend**: Reads CSV and returns first N rows
2. **API Endpoint**: `GET /api/v1/datasets/{dataset_id}/preview?rows=10`
3. **Response Format**:
```json
{
  "columns": ["user_id", "sessions", ...],
  "data": [
    {"user_id": 101, "sessions": 10, ...},
    {"user_id": 102, "sessions": 15, ...}
  ],
  "total_rows": 8,
  "preview_rows": 8
}
```

4. **Frontend**: HTML table displays the data

---

## 🎨 Chart Libraries Used

### Frontend (React):
- **Chart.js** - For bar charts, line charts, pie charts
- **HTML Canvas** - For custom heatmap rendering

### Backend (Python):
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical calculations
- **SciPy** - Statistical functions

---

## 🔄 Real-Time Updates

When you upload a new CSV:
1. File is saved to `backend/uploads/`
2. Metadata stored in PostgreSQL database
3. Analysis is computed on-demand when you click "Analyze"
4. Results are cached for performance
5. Frontend fetches and displays the results

---

## 💡 Key Insights

### Your Current Dataset:
- **8 rows × 10 columns**
- **Numeric columns**: user_id, sessions, avg_session_time_min, pages_visited, conversion_rate, feedback_score
- **Text columns**: username, email, signup_date, subscription_type

### Strong Correlations Found:
- Sessions ↔ Pages Visited (0.995) - Almost perfect!
- Sessions ↔ Conversion Rate (0.967) - Very strong
- Avg Session Time ↔ Feedback Score (0.923) - Strong

### What This Means:
- Users who have more sessions visit more pages
- More sessions lead to higher conversion rates
- Longer session times correlate with better feedback scores

---

## 🚀 Performance Optimizations

1. **Caching**: Analysis results are cached to avoid recalculation
2. **Lazy Loading**: Charts only render when tab is active
3. **Pagination**: Data preview shows limited rows
4. **Async Loading**: All API calls happen in parallel

---

## 📚 Learn More

- **Correlation**: https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
- **Outliers (IQR)**: https://en.wikipedia.org/wiki/Interquartile_range
- **Trend Analysis**: https://en.wikipedia.org/wiki/Linear_regression
- **Chart.js Docs**: https://www.chartjs.org/docs/

---

## 🎯 Summary

**Everything is dynamic!** The visualizations adapt to YOUR data:
- Different CSV = Different charts
- More columns = More visualizations
- Different values = Different insights

No hardcoding - pure data-driven analysis! 🚀
