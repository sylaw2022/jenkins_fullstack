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
├── scripts/          # Utility scripts
│   └── sonar-scanner.sh  # SonarQube analysis script
├── Jenkinsfile       # Jenkins CI/CD pipeline
├── render.yaml       # Render.com configuration
├── sonar-project.properties  # SonarQube configuration
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
- **SonarQube Analysis**: Analyzes code quality and security (optional)
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

## 🔍 SonarQube Code Quality Analysis

SonarQube is integrated to analyze code quality, security vulnerabilities, and code smells.

### Prerequisites

1. **SonarQube Server**: Install and run SonarQube server
   - Download from: https://www.sonarqube.org/downloads/
   - Default URL: `http://localhost:9000`
   - Default credentials: `admin/admin` (change on first login)

2. **SonarQube Scanner**: Install the scanner
   ```bash
   # Option 1: Using npm (recommended for Node.js projects)
   npm install -g sonarqube-scanner
   
   # Option 2: Download standalone scanner
   # https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
   ```

### Local Setup

1. **Create SonarQube Token**:
   - Login to SonarQube: `http://localhost:9000`
   - Go to: User > My Account > Security
   - Generate a new token (e.g., `jenkins-fullstack-token`)

2. **Configure Environment**:
   ```bash
   cp .sonarqube.env.example .sonarqube.env
   # Edit .sonarqube.env and add your SonarQube URL and token
   ```

3. **Run Analysis Locally**:
   ```bash
   npm run sonar
   # Or directly:
   bash scripts/sonar-scanner.sh
   ```

4. **View Results**:
   - Open SonarQube dashboard: `http://localhost:9000/dashboard?id=jenkins-fullstack`

### Jenkins Integration

The Jenkins pipeline includes a SonarQube analysis stage that runs automatically.

#### Jenkins Configuration

1. **Install SonarQube Plugin**:
   - Go to: Jenkins > Manage Jenkins > Manage Plugins
   - Install: "SonarQube Scanner" plugin

2. **Configure SonarQube Server**:
   - Go to: Jenkins > Manage Jenkins > Configure System
   - Under "SonarQube servers", add your SonarQube instance:
     - Name: `SonarQube`
     - Server URL: `http://your-sonarqube-server:9000`
     - Server authentication token: Add your SonarQube token

3. **Install SonarQube Scanner Tool**:
   - Go to: Jenkins > Manage Jenkins > Global Tool Configuration
   - Under "SonarQube Scanner", add scanner installation
   - Name: `SonarQube Scanner`
   - Install automatically from Maven Central

4. **Configure Pipeline Credentials** (Optional):
   - Add credentials in Jenkins for SonarQube:
     - `sonar-host-url`: Your SonarQube server URL
     - `sonar-token`: Your SonarQube authentication token

#### Pipeline Behavior

- The SonarQube analysis stage runs **after** the Build stage
- Analysis is **optional** - pipeline continues even if SonarQube is not configured
- Results are published to SonarQube dashboard
- Quality gates can be configured in SonarQube to fail builds on quality issues

### SonarQube Configuration Files

- **`sonar-project.properties`**: Main SonarQube configuration
- **`.sonarqube.env.example`**: Environment variables template
- **`scripts/sonar-scanner.sh`**: Local analysis script

### What SonarQube Analyzes

- **Code Quality**: Code smells, maintainability issues
- **Security**: Vulnerabilities, security hotspots
- **Coverage**: Test coverage (if test reports are generated)
- **Duplications**: Code duplication detection
- **Complexity**: Cyclomatic complexity
- **Bugs**: Potential bugs and errors

### Quality Gates

Configure quality gates in SonarQube to enforce code quality standards:
- Go to: Quality Gates in SonarQube dashboard
- Set thresholds for:
  - Code coverage
  - Duplicated lines
  - Maintainability rating
  - Security rating
  - Reliability rating

## 🔧 Troubleshooting

### Jenkins Issues

- Ensure Node.js is installed on Jenkins server
- Check Jenkins workspace permissions
- Verify Git credentials are configured

### SonarQube Issues

- **Scanner not found**: Install SonarQube Scanner or add it to PATH
- **Authentication failed**: Verify SONAR_TOKEN is correct and not expired
- **Connection refused**: Check if SonarQube server is running and accessible
- **Project not found**: Create the project in SonarQube dashboard first, or it will be auto-created
- **Jenkins plugin errors**: Ensure SonarQube Scanner plugin is installed and configured correctly

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

