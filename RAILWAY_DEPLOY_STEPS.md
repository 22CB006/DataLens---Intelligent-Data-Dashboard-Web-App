# 🚀 Railway Deployment - Step by Step

## ✅ Issue Fixed!

I've updated the configuration files. Now follow these steps:

---

## Step 1: Push Updated Config (Do This Now)

```bash
git add .
git commit -m "fix: update Railway configuration for proper deployment"
git push origin main
```

---

## Step 2: Configure Railway Dashboard

### 2.1 Go to Your Service Settings

1. In Railway, click on **DataLens---Intelligent-Data-Dashboard-Web-App** service
2. Click **Settings** tab

### 2.2 Set Root Directory

1. Scroll to **Root Directory**
2. Enter: `backend`
3. Click outside to save

### 2.3 Set Start Command

1. Scroll to **Custom Start Command**
2. Enter: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Click outside to save

### 2.4 Add Environment Variables

Click **Variables** tab and add these:

**Required Variables:**
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=<generate-below>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
DEBUG=False
NIXPACKS_PYTHON_VERSION=3.11
```

**Generate SECRET_KEY:**
```bash
# Run in terminal
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**CORS Origins (add after you get Vercel URL):**
```bash
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

---

## Step 3: Deploy

### 3.1 Trigger Deployment

1. Go to **Deployments** tab
2. Click **Deploy** button (top right)
3. Or click ⋮ on latest deployment → **Redeploy**

### 3.2 Watch Logs

You should see:
```
✓ Installing Python 3.11
✓ Installing dependencies
✓ Starting uvicorn
✓ Application running on port 8000
```

### 3.3 Get Your URL

After successful deployment:
1. Go to **Settings** tab
2. Under **Domains**, you'll see your Railway URL
3. Example: `https://datalens-production.up.railway.app`

---

## Step 4: Test Backend

### 4.1 Visit API Docs

Open: `https://your-app.up.railway.app/docs`

You should see the FastAPI Swagger UI!

### 4.2 Test Health Endpoint

Try: `https://your-app.up.railway.app/health`

Should return: `{"status": "healthy"}`

---

## Step 5: Deploy Frontend (Vercel)

### 5.1 Go to Vercel

1. Visit: https://vercel.com
2. Sign up with GitHub
3. Click "Add New..." → "Project"

### 5.2 Import Repository

1. Select your GitHub repo
2. Vercel auto-detects Vite

### 5.3 Configure Build

- **Framework Preset:** Vite
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`

### 5.4 Add Environment Variable

Add this variable:
```bash
VITE_API_URL=https://your-railway-url.up.railway.app
```

Replace with your actual Railway URL!

### 5.5 Deploy

1. Click **Deploy**
2. Wait 1-2 minutes
3. Get your Vercel URL: `https://your-app.vercel.app`

---

## Step 6: Connect Frontend & Backend

### 6.1 Update CORS in Railway

1. Go back to Railway
2. Go to **Variables** tab
3. Update `CORS_ORIGINS`:
```bash
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```
4. Save and redeploy

### 6.2 Test Full App

1. Visit your Vercel URL
2. Register a new user
3. Login
4. Upload a CSV file
5. View your data

---

## 🎉 Success Checklist

- [ ] Backend deployed on Railway
- [ ] Database connected
- [ ] API docs accessible
- [ ] Frontend deployed on Vercel
- [ ] CORS configured
- [ ] Can register/login
- [ ] Can upload files
- [ ] Full app working

---

## 🐛 Troubleshooting

### Build Still Fails?

**Check these in Railway Settings:**
- ✅ Root Directory = `backend`
- ✅ Start Command = `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- ✅ Python Version = `3.11` (in Variables)

### Database Connection Error?

**Verify:**
- ✅ PostgreSQL service is running
- ✅ `DATABASE_URL` variable is set
- ✅ Format: `postgresql://user:pass@host:port/db`

### Frontend Can't Connect?

**Check:**
- ✅ `VITE_API_URL` points to Railway URL
- ✅ `CORS_ORIGINS` includes Vercel URL
- ✅ Both URLs use HTTPS

---

## 📊 Expected Timeline

- **Backend Setup:** 5 minutes
- **Backend Deploy:** 3 minutes
- **Frontend Setup:** 3 minutes
- **Frontend Deploy:** 2 minutes
- **Testing:** 2 minutes

**Total: ~15 minutes** ⏱️

---

## 🎯 Quick Commands

### Push Changes
```bash
git add .
git commit -m "fix: Railway configuration"
git push origin main
```

### Generate Secret Key
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Check Deployment
- Railway: Click service → Deployments → View logs
- Vercel: Click project → Deployments → View logs

---

## ✅ Final Result

After completion, you'll have:

**Backend API:**
- URL: `https://your-app.up.railway.app`
- Docs: `https://your-app.up.railway.app/docs`
- Database: PostgreSQL on Railway

**Frontend App:**
- URL: `https://your-app.vercel.app`
- CDN: Global edge network
- Auto-deploy: On every push

**Share these URLs with anyone!** 🌟

---

## 💡 Pro Tips

1. **Custom Domain:** Add in Railway/Vercel settings
2. **Monitoring:** Use Railway's built-in metrics
3. **Logs:** Check Railway logs for errors
4. **Backups:** Railway auto-backs up PostgreSQL
5. **Scaling:** Upgrade plan when needed

---

**Your DataLens app is ready to go live!** 🚀

Follow these steps and you'll be deployed in 15 minutes!
