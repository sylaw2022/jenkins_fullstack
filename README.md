# Jenkins Fullstack Application

A simple fullstack application with Jenkins CI/CD and Render.com deployment support.

## 🏗️ Architecture

- **Backend**: Node.js/Express API server
- **Frontend**: React application
- **CI/CD**: Jenkins pipeline
- **Deployment**: Render.com

## 📁 Project Structure

```
jenkins_fullstack/
├── backend/           # Node.js/Express API
│   ├── server.js     # Main server file
│   └── package.json  # Backend dependencies
├── frontend/         # React application
│   ├── src/          # React source files
│   ├── public/       # Public assets
│   └── package.json  # Frontend dependencies
├── postman/          # Postman collection and environments
│   ├── Jenkins_Fullstack_API.postman_collection.json
│   ├── Local.postman_environment.json
│   └── Production.postman_environment.json
├── Jenkinsfile       # Jenkins CI/CD pipeline
├── render.yaml       # Render.com configuration
└── README.md         # This file
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Jenkins (for CI/CD)
- Render.com account (for deployment)

### Local Development

#### Backend Setup

```bash
cd backend
npm install
cp .env.example .env
npm start
```

The backend will run on `http://localhost:5000`

#### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env and set REACT_APP_API_URL=http://localhost:5000
npm start
```

The frontend will run on `http://localhost:3000`

## 📦 Git Repository

This project is configured to use a local Git repository at:
```
/home/sylaw/git/repositories/jenkins_fullstack.git
```

### Repository Setup

The repository has been initialized and configured:
- **Local Repository**: `/home/sylaw/jenkins_fullstack`
- **Bare Repository**: `/home/sylaw/git/repositories/jenkins_fullstack.git`
- **Remote**: `origin` points to the local bare repository

### Working with the Repository

```bash
# Check repository status
git status

# Make changes and commit
git add .
git commit -m "Your commit message"
git push origin main

# Pull latest changes
git pull origin main
```

## 🔄 Jenkins CI/CD Setup

### 1. Create Jenkins Pipeline Job

1. Open Jenkins dashboard
2. Click "New Item"
3. Select "Pipeline"
4. Configure the pipeline:
   - **Pipeline Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: `/home/sylaw/git/repositories/jenkins_fullstack.git` (for local Jenkins)
   - **Script Path**: `Jenkinsfile`

### 2. Pipeline Stages

The Jenkins pipeline includes:
- **Checkout**: Clones the repository
- **Install Dependencies**: Installs npm packages for both backend and frontend
- **Test**: Runs tests (if available)
- **Build**: Builds the frontend application
- **Archive Artifacts**: Saves build artifacts

### 3. Run Pipeline

- Click "Build Now" to trigger the pipeline
- View progress in the "Build History"

## 🌐 Render.com Deployment

### Option 1: Using render.yaml (Recommended)

1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)
2. Connect your repository to Render.com
3. Render will automatically detect `render.yaml` and create services

### Option 2: Manual Setup

#### Backend Service

1. Create a new **Web Service** on Render
2. Connect your repository
3. Configure:
   - **Build Command**: `cd backend && npm install`
   - **Start Command**: `cd backend && npm start`
   - **Environment**: Node
   - **Environment Variables**:
     - `NODE_ENV=production`
     - `PORT=5000`

#### Frontend Service

1. Create a new **Static Site** on Render
2. Connect your repository
3. Configure:
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/build`
   - **Environment Variables**:
     - `REACT_APP_API_URL=https://your-backend-service.onrender.com`

### Environment Variables

Make sure to set `REACT_APP_API_URL` in the frontend service to point to your backend service URL.

## 📡 API Endpoints

### Backend API

- `GET /api/health` - Health check endpoint
- `GET /api/message` - Get a message from the backend
- `POST /api/data` - Submit data to the backend
  - Body: `{ "name": "string", "message": "string" }`

## 🧪 Testing with Postman

### Import Postman Collection

A Postman collection is included in the `postman/` directory for easy API testing.

#### Steps to Import:

1. **Open Postman** (Desktop app or web version)

2. **Import Collection**:
   - Click "Import" button
   - Select `postman/Jenkins_Fullstack_API.postman_collection.json`
   - The collection will be imported with all API endpoints

3. **Import Environments** (Optional but recommended):
   - Import `postman/Local.postman_environment.json` for local testing
   - Import `postman/Production.postman_environment.json` for production testing
   - Select the appropriate environment from the environment dropdown

4. **Start Backend Server**:
   ```bash
   cd backend
   npm start
   ```

5. **Run Requests**:
   - Select the "Local" environment (or update `base_url` variable)
   - Run any request from the collection
   - View responses and test results

### Postman Collection Contents

The collection includes:
- ✅ **Health Check** - Tests `/api/health` endpoint with assertions
- ✅ **Get Message** - Tests `/api/message` endpoint
- ✅ **Submit Data** - Tests `/api/data` POST endpoint with sample data
- ✅ **Submit Data (Minimal)** - Tests `/api/data` with empty body (default values)

All requests include automated tests that verify:
- HTTP status codes
- Response structure
- Required fields
- Data validation

### Environment Variables

- **Local**: `base_url = http://localhost:5000`
- **Production**: `base_url = https://jenkins-fullstack-backend.onrender.com`

You can create custom environments or modify the existing ones to match your deployment URLs.

## 🧪 Testing

### Backend Tests

```bash
cd backend
npm test
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📝 Environment Variables

### Backend (.env)

```
PORT=5000
NODE_ENV=production
```

### Frontend (.env)

```
REACT_APP_API_URL=http://localhost:5000
```

For production, set `REACT_APP_API_URL` to your Render.com backend URL.

## 🔧 Troubleshooting

### Jenkins Issues

- Ensure Node.js is installed on Jenkins server
- Check Jenkins workspace permissions
- Verify Git credentials are configured

### Render.com Issues

- Check build logs in Render dashboard
- Verify environment variables are set correctly
- Ensure `render.yaml` syntax is correct
- Check that backend service is running before deploying frontend

## 📄 License

ISC

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

Built with ❤️ for Jenkins CI/CD and Render.com deployment

