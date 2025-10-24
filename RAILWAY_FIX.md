# 🔧 Railway Deployment Fix

## Problem
Railway can't detect how to build because the repo has both `backend/` and `frontend/` folders.

## Solution 1: Configure in Railway Dashboard (EASIEST)

### Step 1: Set Root Directory
1. Go to your Railway project
2. Click on the **DataLens service** (not the database)
3. Click **Settings** tab
4. Scroll to **Root Directory**
5. Enter: `backend`
6. Click **Save**

### Step 2: Set Start Command
1. Still in Settings
2. Scroll to **Custom Start Command**
3. Enter: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Click **Save**

### Step 3: Set Python Version
1. Still in Settings
2. Scroll to **Environment Variables**
3. Add new variable:
   - **Name:** `NIXPACKS_PYTHON_VERSION`
   - **Value:** `3.11`
4. Click **Add**

### Step 4: Redeploy
1. Click **Deployments** tab
2. Click **Deploy** button (top right)
3. Wait 2-3 minutes
4. Check logs for success!

---

## Solution 2: Use Configuration Files (AUTOMATIC)

I've created two config files for you:

### Files Created:
- `railway.json` - Railway configuration
- `nixpacks.toml` - Build configuration

### Push to GitHub:
```bash
git add railway.json nixpacks.toml
git commit -m "fix: add Railway configuration files"
git push origin main
```

Railway will auto-detect these files and deploy correctly!

---

## Solution 3: Separate Services (ADVANCED)

Deploy backend and frontend as separate Railway services:

### Backend Service:
1. Create new service from GitHub
2. Root Directory: `backend`
3. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend Service:
1. Create another service from same repo
2. Root Directory: `frontend`
3. Build Command: `npm install && npm run build`
4. Start Command: `npx serve -s dist -l $PORT`

---

## Verify Environment Variables

Make sure these are set in Railway:

```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=<your-generated-secret>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=production
DEBUG=False
NIXPACKS_PYTHON_VERSION=3.11
```

---

## Expected Build Output

When it works, you should see:
```
✓ Installing Python 3.11
✓ Installing dependencies from requirements.txt
✓ Starting uvicorn server
✓ Application running on port $PORT
```

---

## Test After Deployment

1. Visit: `https://your-app.up.railway.app/docs`
2. You should see FastAPI Swagger UI
3. Try the `/health` endpoint

---

## Common Issues

### "Module not found"
- Check `requirements.txt` is complete
- Verify Python version is 3.11

### "Port already in use"
- Make sure start command uses `$PORT` variable
- Railway assigns port dynamically

### "Database connection failed"
- Verify `DATABASE_URL` is set
- Check PostgreSQL service is running
- Ensure both services are in same project

---

## Quick Commands

### View Logs
```bash
# In Railway dashboard
Deployments → Latest → Deploy Logs
```

### Force Redeploy
```bash
# In Railway dashboard
Deployments → Click ⋮ → Redeploy
```

### Check Variables
```bash
# In Railway dashboard
Service → Variables tab
```

---

## 🎯 Recommended Approach

**Use Solution 1** (Dashboard configuration) - It's the fastest!

1. Set Root Directory to `backend`
2. Set Start Command
3. Add Python version variable
4. Redeploy

**Total time: 2 minutes**

---

## Need Help?

If it still fails:
1. Share the **Deploy Logs** (full output)
2. Share your **Environment Variables** (hide secrets)
3. I'll help debug!

---

**Your app will be live soon!** 🚀
