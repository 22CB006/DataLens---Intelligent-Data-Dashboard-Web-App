# Debugging Guide - Analysis Page Issue

## Issue
The Analysis page shows "Dataset not found" even though the backend is responding correctly.

## Debugging Logs Added

### 1. API Service (`frontend/src/services/api.js`)
- ✅ Request logging: Shows all outgoing API requests
- ✅ Response logging: Shows all successful API responses
- ✅ Error logging: Shows all API errors with status codes

### 2. Analysis Page (`frontend/src/pages/Analysis.jsx`)
- ✅ Dataset ID logging
- ✅ All API response data logging (stats, correlation, outliers, dataset, preview)
- ✅ State setting confirmation logs
- ✅ Current dataset state before render
- ✅ Loading state tracking

## How to Debug

### Step 1: Open Browser Console
1. Open the application in your browser
2. Press `F12` or right-click → "Inspect" → "Console" tab
3. Navigate to the Analysis page

### Step 2: Check Console Logs
Look for these log messages in order:

```
🔍 Loading data for dataset: [dataset-id]
🌐 API Request: GET /datasets/[id]
🌐 API Request: GET /analysis/[id]/statistics
🌐 API Request: GET /analysis/[id]/correlation
... (more requests)
✅ API Response: GET /datasets/[id] 200
✅ API Response: GET /analysis/[id]/statistics 200
... (more responses)
📊 Stats Data: {...}
📁 Dataset Data: {...}
👁️ Preview Data: {...}
✅ All data loaded successfully
Dataset state will be: {...}
🔎 Current dataset state: {...}
🔎 Loading state: false
```

### Step 3: Identify the Problem

#### If you see "Dataset not found":
- Check if `📁 Dataset Data:` shows `null` or `undefined`
- Check if there's an `❌ API Error` for the dataset endpoint
- Check the dataset response structure

#### If API calls are failing:
- Look for `❌ API Error` messages
- Check the HTTP status code
- Verify the backend is running
- Check CORS settings

#### If data loads but doesn't display:
- Check `🔎 Current dataset state:` - it should have data
- Verify field names match (row_count, column_count, etc.)
- Check if loading state is stuck on `true`

## Common Issues & Solutions

### Issue 1: Dataset is null
**Symptoms:** `📁 Dataset Data: null`
**Solution:** Check if the dataset ID in the URL is correct

### Issue 2: API 404 Error
**Symptoms:** `❌ API Error: GET /datasets/[id] 404`
**Solution:** Dataset doesn't exist in database, verify dataset ID

### Issue 3: API 401 Error
**Symptoms:** `❌ API Error: GET /datasets/[id] 401`
**Solution:** Authentication token expired, log in again

### Issue 4: Field name mismatch
**Symptoms:** Data loads but shows 0 rows/columns
**Solution:** Check if using `row_count`/`column_count` instead of `rows`/`columns`

### Issue 5: CORS Error
**Symptoms:** Network errors in console
**Solution:** Verify backend CORS settings allow frontend origin

## Next Steps

1. **Refresh the page** and check the browser console
2. **Copy all console logs** related to the Analysis page
3. **Look for error patterns** in the logs
4. **Share the logs** if you need help debugging

## Field Name Reference

Backend API returns these fields:
- `row_count` (not `rows`)
- `column_count` (not `columns`)
- `original_filename` (preferred over `filename`)
- `file_size`
- `created_at`
- `updated_at`

## Test Checklist

- [ ] Backend is running on http://localhost:8000
- [ ] Frontend is running on http://localhost:5173
- [ ] User is logged in (token in localStorage)
- [ ] Dataset exists in database
- [ ] Browser console is open
- [ ] No CORS errors in console
- [ ] API requests return 200 status
- [ ] Dataset data is not null
