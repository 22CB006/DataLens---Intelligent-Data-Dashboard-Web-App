# 🚀 DataLens Deployment Guide

## Quick Deploy (15-20 minutes to live!)

---

## 📋 Prerequisites

- ✅ GitHub account (you have this)
- ✅ Code pushed to GitHub (you did this)
- ⏳ Railway account (we'll create)
- ⏳ Vercel account (we'll create)

---

## 🎯 Step 1: Deploy Backend + Database (Railway)

### 1.1 Create Railway Account

1. Go to https://railway.app
2. Click "Login with GitHub"
3. Authorize Railway

### 1.2 Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository: `DataLens---Intelligent-Data-Dashboard-Web-App`
4. Railway will auto-detect it's a Python app

### 1.3 Add PostgreSQL Database

1. In your project, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway will provision a database automatically
4. Note: Database credentials are auto-generated

### 1.4 Configure Backend Service

1. Click on your backend service
2. Go to "Settings" tab
3. Set **Root Directory:** `backend`
4. Set **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 1.5 Add Environment Variables

Click "Variables" tab and add:

```bash
# Database (Railway auto-fills these)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# App Settings
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (add your Vercel domain later)
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app

# Environment
ENVIRONMENT=production
DEBUG=False
```

**Generate SECRET_KEY:**
```python
# Run this in Python
import secrets
print(secrets.token_urlsafe(32))
```

### 1.6 Deploy

1. Click "Deploy"
2. Railway will:
   - Install dependencies
   - Run migrations (if configured)
   - Start your app
3. Wait 2-3 minutes
4. You'll get a URL like: `https://your-app.up.railway.app`

### 1.7 Test Backend

Visit: `https://your-app.up.railway.app/docs`

You should see FastAPI Swagger documentation!

---
 
## 🎨 Step 2: Deploy Frontend (Vercel)

### 2.1 Create Vercel Account

1. Go to https://vercel.com
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Vercel

### 2.2 Import Project

1. Click "Add New..." → "Project"
2. Import your GitHub repository
3. Vercel auto-detects it's a Vite/React app

### 2.3 Configure Build Settings

**Framework Preset:** Vite
**Root Directory:** `frontend`
**Build Command:** `npm run build`
**Output Directory:** `dist`

### 2.4 Add Environment Variables

Click "Environment Variables" and add:

```bash
VITE_API_URL=https://your-backend.up.railway.app
```

Replace with your actual Railway backend URL!

### 2.5 Deploy

1. Click "Deploy"
2. Vercel will:
   - Install dependencies
   - Build your React app
   - Deploy to CDN
3. Wait 1-2 minutes
4. You'll get a URL like: `https://your-app.vercel.app`

### 2.6 Update Backend CORS

Go back to Railway:
1. Update `CORS_ORIGINS` to include your Vercel URL
2. Redeploy backend

---

## ✅ Step 3: Test Your Live App!

### 3.1 Visit Your App

Open: `https://your-app.vercel.app`

### 3.2 Test Features

1. ✅ Register a new user
2. ✅ Login
3. ✅ Upload a CSV file
4. ✅ View dataset
5. ✅ Run analysis

### 3.3 Share Your Link! 🎉

Your app is now live! Share:
- **Frontend:** `https://your-app.vercel.app`
- **API Docs:** `https://your-backend.up.railway.app/docs`

---

## 🐳 Optional: Docker Setup (For Later)

### Create Dockerfile for Backend

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create Dockerfile for Frontend

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Build app
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: datalens
      POSTGRES_PASSWORD: datalens123
      POSTGRES_DB: datalens
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://datalens:datalens123@postgres:5432/datalens
      SECRET_KEY: your-secret-key
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### Run with Docker

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 🔄 CI/CD Setup (GitHub Actions)

### Create Backend CI Workflow

```yaml
# .github/workflows/backend-ci.yml
name: Backend CI

on:
  push:
    branches: [ main ]
    paths:
      - 'backend/**'
  pull_request:
    branches: [ main ]
    paths:
      - 'backend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      working-directory: ./backend
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests
      working-directory: ./backend
      run: pytest
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./backend/coverage.xml
```

### Create Frontend CI Workflow

```yaml
# .github/workflows/frontend-ci.yml
name: Frontend CI

on:
  push:
    branches: [ main ]
    paths:
      - 'frontend/**'
  pull_request:
    branches: [ main ]
    paths:
      - 'frontend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      working-directory: ./frontend
      run: npm ci
    
    - name: Run linter
      working-directory: ./frontend
      run: npm run lint
    
    - name: Build
      working-directory: ./frontend
      run: npm run build
```

---

## 🎯 Custom Domain (Optional)

### For Vercel (Frontend)

1. Go to your project settings
2. Click "Domains"
3. Add your custom domain
4. Update DNS records as instructed

### For Railway (Backend)

1. Go to your service settings
2. Click "Settings" → "Domains"
3. Add custom domain
4. Update DNS records

---

## 📊 Monitoring & Logs

### Railway Logs

1. Click on your service
2. Go to "Deployments" tab
3. Click on latest deployment
4. View real-time logs

### Vercel Logs

1. Go to your project
2. Click "Deployments"
3. Click on latest deployment
4. View build and runtime logs

---

## 🔒 Security Checklist

Before going live:

- [ ] Change SECRET_KEY to a strong random value
- [ ] Set DEBUG=False in production
- [ ] Configure proper CORS origins
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS (automatic on Railway/Vercel)
- [ ] Set up database backups (Railway provides this)
- [ ] Review API rate limiting
- [ ] Add monitoring/alerting

---

## 💰 Cost Estimates

### Free Tier Limits

**Railway:**
- $5 free credit per month
- ~500 hours of runtime
- PostgreSQL included
- Perfect for hobby projects

**Vercel:**
- 100 GB bandwidth/month
- Unlimited deployments
- Free SSL
- Perfect for frontend

**Total Cost:** $0-5/month for hobby use

### Upgrade When Needed

- More users → Upgrade Railway ($5-20/month)
- More bandwidth → Upgrade Vercel ($20/month)
- Custom domains → $10-15/year

---

## 🎉 You're Live!

After deployment, you'll have:

✅ Live backend API with database
✅ Live frontend application
✅ Shareable URLs
✅ Automatic HTTPS
✅ Auto-deploy on git push
✅ Professional hosting

**Share your app with the world!** 🌟

---

## 🆘 Troubleshooting

### Backend won't start

- Check Railway logs
- Verify DATABASE_URL is set
- Check Python version (3.11)
- Verify requirements.txt is complete

### Frontend can't connect to backend

- Check VITE_API_URL is correct
- Verify CORS_ORIGINS includes Vercel URL
- Check backend is running

### Database connection errors

- Verify DATABASE_URL format
- Check PostgreSQL is running
- Verify network access

---

## 📚 Next Steps

1. ✅ Deploy to Railway + Vercel
2. ⏳ Add custom domain
3. ⏳ Set up CI/CD
4. ⏳ Add monitoring
5. ⏳ Configure backups
6. ⏳ Add analytics

---

**Your DataLens app is ready for production!** 🚀
