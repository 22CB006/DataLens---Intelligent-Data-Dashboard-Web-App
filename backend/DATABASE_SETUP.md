# Database Setup Guide 🗄️

This guide will help you set up PostgreSQL and create the database for DataLens.

---

## 📋 **Prerequisites**

- PostgreSQL 14+ installed
- Backend virtual environment activated
- Dependencies installed (`pip install -r requirements.txt`)

---

## 🔧 **Step 1: Install PostgreSQL**

### **Windows**

1. **Download PostgreSQL**
   - Visit: https://www.postgresql.org/download/windows/
   - Download the installer (PostgreSQL 14 or higher)

2. **Run Installer**
   - Run the downloaded `.exe` file
   - Follow the installation wizard
   - **Remember the password you set for the `postgres` user!**
   - Default port: 5432 (keep this)
   - Install pgAdmin 4 (recommended)

3. **Verify Installation**
   ```bash
   psql --version
   # Should show: psql (PostgreSQL) 14.x or higher
   ```

### **Mac**

```bash
# Using Homebrew
brew install postgresql@14

# Start PostgreSQL
brew services start postgresql@14

# Verify
psql --version
```

### **Linux (Ubuntu/Debian)**

```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify
psql --version
```

---

## 🗄️ **Step 2: Create Database**

### **Option 1: Using psql (Command Line)**

```bash
# Connect to PostgreSQL
psql -U postgres

# You'll be prompted for the password you set during installation

# Create database
CREATE DATABASE datalens;

# Verify
\l

# You should see 'datalens' in the list

# Exit
\q
```

### **Option 2: Using pgAdmin 4 (GUI)**

1. Open pgAdmin 4
2. Connect to PostgreSQL server (enter your password)
3. Right-click on "Databases"
4. Select "Create" → "Database"
5. Name: `datalens`
6. Click "Save"

---

## ⚙️ **Step 3: Configure Database URL**

Update your `.env` file in the `backend` directory:

```bash
# backend/.env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/datalens
```

**Replace:**
- `YOUR_PASSWORD` with the password you set during PostgreSQL installation
- `localhost` with your database host (usually localhost for local development)
- `5432` with your PostgreSQL port (usually 5432)
- `datalens` with your database name

**Example:**
```bash
DATABASE_URL=postgresql://postgres:mypassword123@localhost:5432/datalens
```

---

## 🔄 **Step 4: Install New Dependencies**

We added `asyncpg` for async PostgreSQL support:

```bash
# Make sure virtual environment is activated
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install new dependency
pip install asyncpg==0.29.0

# Or reinstall all
pip install -r requirements.txt
```

---

## 🚀 **Step 5: Create Initial Migration**

Alembic will create the database tables based on our models:

```bash
# Make sure you're in the backend directory with venv activated
cd backend

# Create initial migration
alembic revision --autogenerate -m "Initial migration: users and datasets tables"

# This creates a migration file in alembic/versions/
```

**What this does:**
- Scans your models (User, Dataset)
- Compares with current database schema
- Generates migration script with SQL commands

---

## 📤 **Step 6: Apply Migration**

```bash
# Apply the migration to create tables
alembic upgrade head

# You should see output like:
# INFO  [alembic.runtime.migration] Running upgrade -> abc123, Initial migration
```

**What this does:**
- Executes the migration script
- Creates `users` and `datasets` tables
- Creates indexes and constraints

---

## ✅ **Step 7: Verify Database**

### **Using psql:**

```bash
psql -U postgres -d datalens

# List tables
\dt

# You should see:
# - users
# - datasets
# - alembic_version (tracks migrations)

# Describe users table
\d users

# Exit
\q
```

### **Using pgAdmin 4:**

1. Open pgAdmin 4
2. Navigate to: Servers → PostgreSQL → Databases → datalens → Schemas → public → Tables
3. You should see `users` and `datasets` tables

---

## 🧪 **Step 8: Test Database Connection**

Create a test script to verify connection:

```python
# test_db.py
import asyncio
from app.core.database import engine
from sqlalchemy import text

async def test_connection():
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        print(f"Result: {result.scalar()}")

if __name__ == "__main__":
    asyncio.run(test_connection())
```

Run it:
```bash
python test_db.py
```

---

## 📚 **Understanding Database Models**

### **User Model**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### **Dataset Model**
```sql
CREATE TABLE datasets (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) UNIQUE NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size INTEGER NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    row_count INTEGER,
    column_count INTEGER,
    columns_info JSONB,
    status VARCHAR(50) DEFAULT 'uploaded',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 🔄 **Common Alembic Commands**

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current

# Rollback to specific version
alembic downgrade <revision_id>
```

---

## 🐛 **Troubleshooting**

### **Issue: "psql: command not found"**
**Solution:** Add PostgreSQL to your PATH or use full path:
```bash
# Windows
C:\Program Files\PostgreSQL\14\bin\psql -U postgres
```

### **Issue: "password authentication failed"**
**Solution:** 
- Check your password
- Reset password if needed:
  ```bash
  # As postgres user
  ALTER USER postgres PASSWORD 'newpassword';
  ```

### **Issue: "database 'datalens' does not exist"**
**Solution:** Create the database first (Step 2)

### **Issue: "could not connect to server"**
**Solution:** 
- Check if PostgreSQL is running:
  ```bash
  # Windows (Services)
  # Mac
  brew services list
  # Linux
  sudo systemctl status postgresql
  ```

### **Issue: Alembic can't find models**
**Solution:** Make sure all models are imported in `alembic/env.py`

### **Issue: "asyncpg not installed"**
**Solution:**
```bash
pip install asyncpg==0.29.0
```

---

## 📊 **What We've Built**

✅ **Database Models:**
- User model with authentication fields
- Dataset model with file metadata
- Relationships (User → Datasets)
- UUID primary keys
- Automatic timestamps

✅ **Database Features:**
- Foreign key constraints
- Cascade deletes
- Unique constraints
- Indexes for performance
- JSONB for flexible data

✅ **Migration System:**
- Alembic configuration
- Async support
- Version control for schema

---

## 🎯 **Next Steps**

After completing database setup:
1. ✅ Database created
2. ✅ Tables created
3. ✅ Connection verified
4. ➡️ **Next: Implement Authentication (Milestone 2.2)**

---

## 📝 **Quick Reference**

```bash
# Create database
psql -U postgres -c "CREATE DATABASE datalens;"

# Create migration
alembic revision --autogenerate -m "message"

# Apply migration
alembic upgrade head

# Test connection
python test_db.py
```

---

**You're now ready to implement authentication! 🎉**

See the next section for JWT authentication implementation.
