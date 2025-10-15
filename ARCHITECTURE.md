# DataLens — System Architecture 🏗️

This document describes the technical architecture, design decisions, and system components of DataLens.

---

## 📐 **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           React Frontend (Vite + TailwindCSS)        │   │
│  │  - Dashboard UI    - Data Visualization             │   │
│  │  - File Upload     - Authentication                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTPS/REST API
┌─────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              FastAPI Backend Server                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │   │
│  │  │ Auth Service │  │ Data Service │  │ Analysis │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────┘  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │   │
│  │  │  JWT Auth    │  │ File Handler │  │Visualizer│  │   │
│  │  └──────────────┘  └──────────────┘  └──────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ SQLAlchemy ORM
┌─────────────────────────────────────────────────────────────┐
│                        DATA LAYER                            │
│  ┌──────────────────┐  ┌──────────────────────────────┐    │
│  │   PostgreSQL     │  │    File Storage              │    │
│  │   - Users        │  │    - Uploaded Datasets       │    │
│  │   - Datasets     │  │    - Temporary Files         │    │
│  │   - Analysis     │  │                              │    │
│  └──────────────────┘  └──────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 **Technology Stack**

### **Frontend**
| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **React 18** | UI Framework | Component-based, large ecosystem, industry standard |
| **Vite** | Build Tool | Fast HMR, optimized builds, modern tooling |
| **TailwindCSS** | Styling | Utility-first, rapid development, consistent design |
| **shadcn/ui** | Components | Accessible, customizable, modern design |
| **Chart.js** | Visualization | Lightweight, flexible, good documentation |
| **Axios** | HTTP Client | Interceptors, better error handling than fetch |
| **React Router** | Routing | Standard routing solution for React |

### **Backend**
| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **FastAPI** | Web Framework | High performance, async support, auto-docs |
| **Python 3.11+** | Language | Rich data science ecosystem, readable |
| **Pandas** | Data Processing | Industry standard for data manipulation |
| **NumPy** | Numerical Computing | Fast array operations, scientific computing |
| **SQLAlchemy** | ORM | Powerful, flexible, async support |
| **PostgreSQL** | Database | Reliable, feature-rich, JSON support |
| **JWT** | Authentication | Stateless, scalable, standard |
| **Pydantic** | Validation | Type safety, automatic validation |

### **DevOps**
| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **Docker** | Containerization | Consistent environments, easy deployment |
| **GitHub Actions** | CI/CD | Integrated with GitHub, free for public repos |
| **Render/Railway** | Backend Hosting | Easy deployment, free tier, PostgreSQL included |
| **Vercel** | Frontend Hosting | Optimized for React, automatic deployments |

---

## 🗂️ **Database Schema**

### **Users Table**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Datasets Table**
```sql
CREATE TABLE datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size INTEGER NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    row_count INTEGER,
    column_count INTEGER,
    columns_info JSONB,
    status VARCHAR(50) DEFAULT 'uploaded',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Analysis Results Table**
```sql
CREATE TABLE analysis_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id UUID REFERENCES datasets(id) ON DELETE CASCADE,
    analysis_type VARCHAR(100) NOT NULL,
    results JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Relationships**
- One User → Many Datasets (One-to-Many)
- One Dataset → Many Analysis Results (One-to-Many)

---

## 🔐 **Authentication Flow**

```
┌──────────┐                                    ┌──────────┐
│  Client  │                                    │  Server  │
└────┬─────┘                                    └────┬─────┘
     │                                                │
     │  1. POST /auth/register                       │
     │  { email, password, username }                │
     ├──────────────────────────────────────────────>│
     │                                                │
     │                                    2. Hash password
     │                                    3. Create user in DB
     │                                                │
     │  4. Return user data                          │
     │<──────────────────────────────────────────────┤
     │                                                │
     │  5. POST /auth/login                          │
     │  { email, password }                          │
     ├──────────────────────────────────────────────>│
     │                                                │
     │                                    6. Verify password
     │                                    7. Generate JWT
     │                                                │
     │  8. Return { access_token, token_type }       │
     │<──────────────────────────────────────────────┤
     │                                                │
     │  9. Store token in localStorage                │
     │                                                │
     │  10. GET /datasets (with Authorization header)│
     │  Authorization: Bearer <token>                │
     ├──────────────────────────────────────────────>│
     │                                                │
     │                                    11. Verify JWT
     │                                    12. Get user from token
     │                                    13. Fetch user's datasets
     │                                                │
     │  14. Return datasets                          │
     │<──────────────────────────────────────────────┤
     │                                                │
```

### **JWT Token Structure**
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

---

## 📊 **Data Processing Pipeline**

```
┌─────────────────────────────────────────────────────────────┐
│                    File Upload Flow                          │
└─────────────────────────────────────────────────────────────┘

1. User uploads file (CSV/Excel/JSON)
                ↓
2. Validate file type and size
                ↓
3. Generate unique filename (UUID)
                ↓
4. Save file to storage
                ↓
5. Create dataset metadata in DB
                ↓
6. Return dataset ID to client

┌─────────────────────────────────────────────────────────────┐
│                  Data Processing Flow                        │
└─────────────────────────────────────────────────────────────┘

1. Read file into Pandas DataFrame
                ↓
2. Detect column types (numeric, categorical, datetime)
                ↓
3. Validate data integrity
                ↓
4. Clean data (handle missing values, outliers)
                ↓
5. Store processed data info in DB
                ↓
6. Return data preview and metadata

┌─────────────────────────────────────────────────────────────┐
│                   Analysis Flow                              │
└─────────────────────────────────────────────────────────────┘

1. Fetch dataset from storage
                ↓
2. Load into Pandas DataFrame
                ↓
3. Perform requested analysis:
   - Descriptive statistics (mean, median, std)
   - Correlation analysis
   - Outlier detection
   - Trend analysis
                ↓
4. Format results for API response
                ↓
5. Cache results in DB
                ↓
6. Return analysis results
```

---

## 🔄 **API Design Patterns**

### **RESTful Endpoints**

```
Authentication:
POST   /api/v1/auth/register      - Register new user
POST   /api/v1/auth/login         - Login user
GET    /api/v1/auth/me            - Get current user

Datasets:
POST   /api/v1/datasets/upload    - Upload dataset
GET    /api/v1/datasets/          - List user's datasets
GET    /api/v1/datasets/{id}      - Get dataset details
DELETE /api/v1/datasets/{id}      - Delete dataset
GET    /api/v1/datasets/{id}/preview - Preview data

Analysis:
GET    /api/v1/analysis/{id}/statistics  - Get statistics
GET    /api/v1/analysis/{id}/correlation - Get correlations
GET    /api/v1/analysis/{id}/outliers    - Detect outliers
GET    /api/v1/analysis/{id}/trends      - Analyze trends

Visualization:
GET    /api/v1/visualization/{id}/chart-data - Get chart data
POST   /api/v1/visualization/{id}/custom     - Custom chart
```

### **Request/Response Format**

**Success Response:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid file format",
    "details": { ... }
  }
}
```

---

## 🛡️ **Security Measures**

### **Authentication & Authorization**
- JWT tokens with expiration (24 hours)
- Password hashing with bcrypt (12 rounds)
- HTTPS only in production
- CORS configuration for allowed origins
- Rate limiting on auth endpoints

### **Data Security**
- Input validation with Pydantic
- SQL injection prevention (SQLAlchemy ORM)
- File type validation (whitelist)
- File size limits (50MB max)
- Secure file storage (UUID filenames)
- User data isolation (row-level security)

### **API Security**
- Authentication required for all protected endpoints
- Request validation
- Error message sanitization
- CSRF protection
- Security headers (HSTS, X-Frame-Options, etc.)

---

## ⚡ **Performance Optimizations**

### **Backend**
- Async/await for I/O operations
- Database connection pooling
- Query optimization with indexes
- Pagination for large datasets
- Caching of analysis results
- Lazy loading of data

### **Frontend**
- Code splitting (React.lazy)
- Image optimization
- Bundle size optimization
- Memoization (useMemo, useCallback)
- Virtual scrolling for large lists
- Debouncing for search/filter

### **Database**
- Indexes on frequently queried columns
- JSONB for flexible data storage
- Partial indexes for filtered queries
- Connection pooling

---

## 📈 **Scalability Considerations**

### **Current Architecture (MVP)**
- Single server deployment
- File storage on server filesystem
- PostgreSQL on same server
- Suitable for: 100-1000 users

### **Future Scaling Options**

**Horizontal Scaling:**
- Load balancer (Nginx/AWS ALB)
- Multiple backend instances
- Session storage in Redis
- Distributed file storage (S3/MinIO)

**Database Scaling:**
- Read replicas for analytics
- Connection pooling
- Query caching
- Partitioning for large tables

**Caching Layer:**
- Redis for session storage
- Cache analysis results
- Cache frequently accessed datasets

---

## 🔍 **Monitoring & Logging**

### **Application Logging**
```python
# Structured logging format
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "backend",
  "endpoint": "/api/v1/datasets/upload",
  "user_id": "uuid",
  "duration_ms": 150,
  "status": 200
}
```

### **Metrics to Track**
- Request rate and latency
- Error rate by endpoint
- Database query performance
- File upload success rate
- User authentication attempts
- Active users count

### **Health Checks**
```
GET /health
Response:
{
  "status": "healthy",
  "database": "connected",
  "storage": "available",
  "version": "1.0.0"
}
```

---

## 🧪 **Testing Strategy**

### **Backend Testing**
- **Unit Tests:** Service layer functions
- **Integration Tests:** API endpoints
- **Database Tests:** Model operations
- **Security Tests:** Authentication flow

### **Frontend Testing**
- **Unit Tests:** Utility functions
- **Component Tests:** React components
- **Integration Tests:** User flows
- **E2E Tests:** Critical paths (optional)

### **Test Coverage Goals**
- Backend: 80%+ coverage
- Frontend: 70%+ coverage
- Critical paths: 100% coverage

---

## 🚀 **Deployment Architecture**

### **Production Setup**

```
┌─────────────────────────────────────────────────────────┐
│                    Vercel CDN                            │
│              (Frontend Hosting)                          │
│         https://datalens.vercel.app                      │
└─────────────────────────────────────────────────────────┘
                        ↕ HTTPS
┌─────────────────────────────────────────────────────────┐
│                  Render/Railway                          │
│              (Backend Hosting)                           │
│         https://api.datalens.com                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │         FastAPI Application                      │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────────┐
│              Managed PostgreSQL                          │
│         (Render/Railway Database)                        │
└─────────────────────────────────────────────────────────┘
```

### **Environment Variables**

**Backend (.env):**
```bash
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=["https://datalens.vercel.app"]
MAX_FILE_SIZE=52428800  # 50MB
```

**Frontend (.env):**
```bash
VITE_API_URL=https://api.datalens.com
VITE_MAX_FILE_SIZE=52428800
```

---

## 🔄 **CI/CD Pipeline**

```
┌─────────────────────────────────────────────────────────┐
│                  GitHub Push                             │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│              GitHub Actions Triggered                    │
└─────────────────────────────────────────────────────────┘
                        ↓
        ┌───────────────────────────────┐
        │                               │
        ↓                               ↓
┌──────────────┐              ┌──────────────┐
│   Backend    │              │   Frontend   │
│   Pipeline   │              │   Pipeline   │
└──────────────┘              └──────────────┘
        │                               │
        ↓                               ↓
  1. Lint code                    1. Lint code
  2. Run tests                    2. Run tests
  3. Build Docker                 3. Build app
  4. Push to registry             4. Deploy to Vercel
  5. Deploy to Render
```

---

## 📚 **Design Decisions**

### **Why FastAPI over Flask?**
- Built-in async support
- Automatic API documentation
- Type hints and validation
- Better performance
- Modern Python features

### **Why PostgreSQL over MongoDB?**
- Structured data (users, datasets)
- ACID compliance
- Better for relational data
- JSONB for flexibility
- Mature ecosystem

### **Why React over Vue/Angular?**
- Largest ecosystem
- More job opportunities
- Better for learning
- Rich component libraries
- Industry standard

### **Why Vite over Create React App?**
- Faster development server
- Optimized builds
- Modern tooling
- Better developer experience
- Active maintenance

---

## 🎯 **Future Enhancements**

### **Phase 2 Features**
- Real-time collaboration
- Advanced ML predictions
- Natural language queries
- Scheduled reports
- Data export to multiple formats

### **Technical Improvements**
- WebSocket for real-time updates
- Redis caching layer
- S3 for file storage
- Elasticsearch for search
- GraphQL API option

---

## 📞 **Support & Maintenance**

### **Monitoring Tools**
- Application logs (structured JSON)
- Error tracking (Sentry - optional)
- Performance monitoring
- Database query analysis

### **Backup Strategy**
- Daily database backups
- File storage backups
- Configuration backups
- Disaster recovery plan

---

This architecture is designed to be:
- ✅ **Scalable** - Can grow with user base
- ✅ **Maintainable** - Clean code structure
- ✅ **Secure** - Industry-standard security
- ✅ **Performant** - Optimized for speed
- ✅ **Testable** - Comprehensive test coverage

**Ready to build! 🚀**
