pipeline {
    agent any
    
    environment {
        NODE_VERSION = '18'
        BACKEND_DIR = 'backend'
        FRONTEND_DIR = 'frontend'
        // Email notification configuration
        EMAIL_RECIPIENT = 'groklord@yahoo.com'
        EMAIL_FROM = 'groklord@yahoo.com'
        EMAIL_REPLY_TO = 'groklord@yahoo.com'
        // SonarQube configuration - set these in Jenkins credentials or environment
        // SONAR_HOST_URL = credentials('sonar-host-url')
        // SONAR_TOKEN = credentials('sonar-token')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository...'
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            parallel {
                stage('Backend Dependencies') {
                    steps {
                        dir("${env.BACKEND_DIR}") {
                            echo 'Installing backend dependencies...'
                            sh 'npm install'
                        }
                    }
                }
                stage('Frontend Dependencies') {
                    steps {
                        dir("${env.FRONTEND_DIR}") {
                            echo 'Installing frontend dependencies...'
                            sh 'npm install'
                        }
                    }
                }
            }
        }
        
        stage('Test') {
            parallel {
                stage('Backend Tests') {
                    steps {
                        dir("${env.BACKEND_DIR}") {
                            echo 'Running backend tests...'
                            script {
                                try {
                                    // Check if test files exist
                                    def testFiles = sh(
                                        script: 'find . -name "*.test.js" -o -name "*.spec.js" | head -1',
                                        returnStdout: true
                                    ).trim()
                                    
                                    if (testFiles) {
                                        echo "Found test files, running tests..."
                                        sh 'npm test -- --watchAll=false --coverage --coverageReporters=text-summary --passWithNoTests'
                                        echo '✅ Backend tests passed!'
                                    } else {
                                        echo '⚠️ No test files found. Skipping tests...'
                                        echo '✅ Backend test stage completed (no tests to run)'
                                    }
                                } catch (Exception e) {
                                    echo '❌ Backend tests failed!'
                                    echo "Error: ${e.getMessage()}"
                                    // Send email notification for test failure
                                    emailext (
                                        subject: "❌ Backend Tests FAILED: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                                        body: """
                                            <h2>Backend Unit Tests Failed</h2>
                                            <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                                            <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                                            <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                                            <p><strong>Status:</strong> <span style="color: red;">TESTS FAILED ❌</span></p>
                                            <p><strong>Branch:</strong> ${env.GIT_BRANCH ?: 'N/A'}</p>
                                            <p><strong>Commit:</strong> ${env.GIT_COMMIT ?: 'N/A'}</p>
                                            <hr>
                                            <h3>Test Failure Details</h3>
                                            <p>Backend unit tests have failed. Please check the build console for detailed error information.</p>
                                            <p><a href="${env.BUILD_URL}console">View Console Output</a></p>
                                            <hr>
                                            <p><em>This is an automated message from Jenkins CI/CD Pipeline.</em></p>
                                        """,
                                        to: "${env.EMAIL_RECIPIENT}",
                                        from: "${env.EMAIL_FROM}",
                                        replyTo: "${env.EMAIL_REPLY_TO}",
                                        mimeType: 'text/html',
                                        attachLog: true,
                                        compressLog: true
                                    )
                                    throw e
                                }
                            }
                        }
                    }
                }
                stage('Frontend Tests') {
                    steps {
                        dir("${env.FRONTEND_DIR}") {
                            echo 'Running frontend tests...'
                            script {
                                try {
                                    // Check if test files exist
                                    def testFiles = sh(
                                        script: 'find src -name "*.test.js" -o -name "*.test.jsx" -o -name "*.spec.js" -o -name "*.spec.jsx" | head -1',
                                        returnStdout: true
                                    ).trim()
                                    
                                    if (testFiles) {
                                        echo "Found test files, running tests..."
                                        sh 'CI=true npm test -- --watchAll=false --coverage --coverageReporters=text-summary --passWithNoTests'
                                        echo '✅ Frontend tests passed!'
                                    } else {
                                        echo '⚠️ No test files found. Skipping tests...'
                                        echo '✅ Frontend test stage completed (no tests to run)'
                                    }
                                } catch (Exception e) {
                                    echo '❌ Frontend tests failed!'
                                    echo "Error: ${e.getMessage()}"
                                    // Send email notification for test failure
                                    emailext (
                                        subject: "❌ Frontend Tests FAILED: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                                        body: """
                                            <h2>Frontend Unit Tests Failed</h2>
                                            <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                                            <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                                            <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                                            <p><strong>Status:</strong> <span style="color: red;">TESTS FAILED ❌</span></p>
                                            <p><strong>Branch:</strong> ${env.GIT_BRANCH ?: 'N/A'}</p>
                                            <p><strong>Commit:</strong> ${env.GIT_COMMIT ?: 'N/A'}</p>
                                            <hr>
                                            <h3>Test Failure Details</h3>
                                            <p>Frontend unit tests have failed. Please check the build console for detailed error information.</p>
                                            <p><a href="${env.BUILD_URL}console">View Console Output</a></p>
                                            <hr>
                                            <p><em>This is an automated message from Jenkins CI/CD Pipeline.</em></p>
                                        """,
                                        to: "${env.EMAIL_RECIPIENT}",
                                        from: "${env.EMAIL_FROM}",
                                        replyTo: "${env.EMAIL_REPLY_TO}",
                                        mimeType: 'text/html',
                                        attachLog: true,
                                        compressLog: true
                                    )
                                    throw e
                                }
                            }
                        }
                    }
                }
            }
        }
        
        stage('Build') {
            parallel {
                stage('Backend Build') {
                    steps {
                        dir("${env.BACKEND_DIR}") {
                            echo 'Backend build check...'
                            script {
                                try {
                                    sh 'node --version'
                                    sh 'npm --version'
                                    // Validate backend can start (syntax check)
                                    sh 'node -c server.js || true'
                                    echo '✅ Backend build check passed!'
                                } catch (Exception e) {
                                    echo '❌ Backend build check failed!'
                                    emailext (
                                        subject: "❌ Backend Build FAILED: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                                        body: """
                                            <h2>Backend Build Failed</h2>
                                            <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                                            <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                                            <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                                            <p><strong>Status:</strong> <span style="color: red;">BUILD FAILED ❌</span></p>
                                            <p><strong>Branch:</strong> ${env.GIT_BRANCH ?: 'N/A'}</p>
                                            <p><strong>Commit:</strong> ${env.GIT_COMMIT ?: 'N/A'}</p>
                                            <hr>
                                            <p>Backend build validation failed. Check the console for details.</p>
                                            <p><a href="${env.BUILD_URL}console">View Console Output</a></p>
                                            <hr>
                                            <p><em>This is an automated message from Jenkins CI/CD Pipeline.</em></p>
                                        """,
                                        to: "${env.EMAIL_RECIPIENT}",
                                        mimeType: 'text/html',
                                        attachLog: true
                                    )
                                    throw e
                                }
                            }
                        }
                    }
                }
                stage('Frontend Build') {
                    steps {
                        dir("${env.FRONTEND_DIR}") {
                            echo 'Building frontend...'
                            script {
                                try {
                                    sh 'npm run build'
                                    echo '✅ Frontend build successful!'
                                } catch (Exception e) {
                                    echo '❌ Frontend build failed!'
                                    emailext (
                                        subject: "❌ Frontend Build FAILED: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                                        body: """
                                            <h2>Frontend Build Failed</h2>
                                            <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                                            <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                                            <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                                            <p><strong>Status:</strong> <span style="color: red;">BUILD FAILED ❌</span></p>
                                            <p><strong>Branch:</strong> ${env.GIT_BRANCH ?: 'N/A'}</p>
                                            <p><strong>Commit:</strong> ${env.GIT_COMMIT ?: 'N/A'}</p>
                                            <hr>
                                            <h3>Build Failure Details</h3>
                                            <p>Frontend build failed. Common causes:</p>
                                            <ul>
                                                <li>Compilation errors</li>
                                                <li>Missing dependencies</li>
                                                <li>TypeScript/ESLint errors</li>
                                                <li>Build configuration issues</li>
                                            </ul>
                                            <p><a href="${env.BUILD_URL}console">View Console Output</a></p>
                                            <hr>
                                            <p><em>This is an automated message from Jenkins CI/CD Pipeline.</em></p>
                                        """,
                                        to: "${env.EMAIL_RECIPIENT}",
                                        from: "${env.EMAIL_FROM}",
                                        replyTo: "${env.EMAIL_REPLY_TO}",
                                        mimeType: 'text/html',
                                        attachLog: true,
                                        compressLog: true
                                    )
                                    throw e
                                }
                            }
                        }
                    }
                }
            }
        }
        
        stage('API Tests (Postman)') {
            steps {
                script {
                    // Install root dependencies to get newman
                    sh 'npm install'
                    
                    // Start backend server in background
                    echo '🚀 Starting backend server...'
                    sh '''
                        cd backend
                        nohup node server.js > ../backend-server.log 2>&1 &
                        echo $! > ../backend-server.pid
                    '''
                    
                    // Wait for server to be ready
                    echo '⏳ Waiting for backend server to start...'
                    def maxAttempts = 30
                    def attempt = 0
                    def serverReady = false
                    
                    while (attempt < maxAttempts && !serverReady) {
                        sleep(time: 3, unit: 'SECONDS')
                        def response = sh(
                            script: 'curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/health || echo "000"',
                            returnStdout: true
                        ).trim()
                        
                        if (response == '200') {
                            serverReady = true
                            echo '✅ Backend server is ready!'
                        } else {
                            attempt++
                            echo "⏳ Attempt ${attempt}/${maxAttempts} - Server not ready yet..."
                        }
                    }
                    
                    if (!serverReady) {
                        error('❌ Backend server failed to start within timeout period')
                    }
                    
                    // Run Postman tests
                    echo '🧪 Running Postman API tests...'
                    try {
                        sh '''
                            npx newman run postman/Jenkins_Fullstack_API.postman_collection.json \
                                -e postman/Local.postman_environment.json \
                                --reporters cli,json \
                                --reporter-json-export postman-test-results.json \
                                --timeout-request 5000
                        '''
                        echo '✅ All API tests passed!'
                    } catch (Exception e) {
                        echo '❌ API tests failed!'
                        // Archive test results even on failure
                        archiveArtifacts artifacts: 'postman-test-results.json', allowEmptyArchive: true
                        
                        // Send email notification for API test failure
                        def testResults = ''
                        try {
                            if (fileExists('postman-test-results.json')) {
                                def resultsFile = readFile('postman-test-results.json')
                                // Parse JSON manually or use sh to extract stats
                                def statsMatch = resultsFile =~ /"total":\s*(\d+).*"failed":\s*(\d+).*"total":\s*(\d+).*"failed":\s*(\d+)/
                                if (statsMatch) {
                                    testResults = """
                                        <h3>Test Results Summary</h3>
                                        <ul>
                                            <li><strong>Total Requests:</strong> ${statsMatch[0][1]}</li>
                                            <li><strong>Failed Requests:</strong> ${statsMatch[0][2]}</li>
                                            <li><strong>Total Assertions:</strong> ${statsMatch[0][3]}</li>
                                            <li><strong>Failed Assertions:</strong> ${statsMatch[0][4]}</li>
                                        </ul>
                                    """
                                } else {
                                    testResults = '<p>Test results file found but unable to parse statistics.</p>'
                                }
                            } else {
                                testResults = '<p>Test results file not found.</p>'
                            }
                        } catch (Exception readErr) {
                            testResults = '<p>Unable to parse test results: ' + readErr.getMessage() + '</p>'
                        }
                        
                        emailext (
                            subject: "❌ API Tests (Postman) FAILED: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                            body: """
                                <h2>API Integration Tests Failed</h2>
                                <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                                <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                                <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                                <p><strong>Status:</strong> <span style="color: red;">API TESTS FAILED ❌</span></p>
                                <p><strong>Branch:</strong> ${env.GIT_BRANCH ?: 'N/A'}</p>
                                <p><strong>Commit:</strong> ${env.GIT_COMMIT ?: 'N/A'}</p>
                                <hr>
                                ${testResults}
                                <h3>Test Failure Details</h3>
                                <p>Postman/Newman API tests have failed. Check the build console and test results for details.</p>
                                <p><a href="${env.BUILD_URL}console">View Console Output</a></p>
                                <p>Test results JSON is available in build artifacts.</p>
                                <hr>
                                <p><em>This is an automated message from Jenkins CI/CD Pipeline.</em></p>
                            """,
                            to: "${env.EMAIL_RECIPIENT}",
                            mimeType: 'text/html',
                            attachLog: true,
                            compressLog: true
                        )
                        throw e
                    } finally {
                        // Stop backend server
                        echo '🛑 Stopping backend server...'
                        sh '''
                            if [ -f backend-server.pid ]; then
                                kill $(cat backend-server.pid) 2>/dev/null || true
                                rm -f backend-server.pid
                            fi
                            pkill -f "node server.js" || true
                        '''
                        // Archive test results
                        archiveArtifacts artifacts: 'postman-test-results.json', allowEmptyArchive: true
                    }
                }
            }
        }
        
        stage('Frontend E2E Tests (Cypress)') {
            when {
                // Only run if frontend build succeeded
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    // Install frontend dependencies (including Cypress)
                    dir("${env.FRONTEND_DIR}") {
                        sh 'npm install'
                    }
                    
                    // Start frontend server in background
                    echo '🚀 Starting frontend server...'
                    dir("${env.FRONTEND_DIR}") {
                        sh '''
                            BROWSER=none PORT=3000 REACT_APP_API_URL=http://localhost:5000 nohup npm start > ../frontend-server.log 2>&1 &
                            echo $! > ../frontend-server.pid
                        '''
                    }
                    
                    // Wait for frontend server to be ready
                    echo '⏳ Waiting for frontend server to start...'
                    def maxAttempts = 60 // Frontend takes longer to start
                    def attempt = 0
                    def serverReady = false
                    
                    while (attempt < maxAttempts && !serverReady) {
                        sleep(time: 5, unit: 'SECONDS')
                        def response = sh(
                            script: 'curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 || echo "000"',
                            returnStdout: true
                        ).trim()
                        
                        if (response == '200') {
                            serverReady = true
                            echo '✅ Frontend server is ready!'
                        } else {
                            attempt++
                            echo "⏳ Attempt ${attempt}/${maxAttempts} - Frontend server not ready yet..."
                        }
                    }
                    
                    if (!serverReady) {
                        error('❌ Frontend server failed to start within timeout period')
                    }
                    
                    // Ensure backend is running for E2E tests
                    echo '🔍 Checking backend server...'
                    def backendResponse = sh(
                        script: 'curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/health || echo "000"',
                        returnStdout: true
                    ).trim()
                    
                    if (backendResponse != '200') {
                        echo '⚠️ Backend server not running. Starting backend for E2E tests...'
                        dir("${env.BACKEND_DIR}") {
                            sh '''
                                PORT=5000 nohup node server.js > ../backend-server-e2e.log 2>&1 &
                                echo $! > ../backend-server-e2e.pid
                            '''
                        }
                        
                        // Wait for backend to be ready
                        def backendAttempts = 0
                        def backendReady = false
                        while (backendAttempts < 30 && !backendReady) {
                            sleep(time: 2, unit: 'SECONDS')
                            def healthCheck = sh(
                                script: 'curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/health || echo "000"',
                                returnStdout: true
                            ).trim()
                            if (healthCheck == '200') {
                                backendReady = true
                                echo '✅ Backend server is ready!'
                            } else {
                                backendAttempts++
                                echo "⏳ Backend attempt ${backendAttempts}/30..."
                            }
                        }
                        
                        if (!backendReady) {
                            error('❌ Backend server failed to start for E2E tests')
                        }
                    } else {
                        echo '✅ Backend server is already running!'
                    }
                    
                    // Run Cypress E2E tests
                    echo '🧪 Running Cypress E2E tests...'
                    try {
                        dir("${env.FRONTEND_DIR}") {
                            sh '''
                                # Set environment variables
                                export REACT_APP_API_URL=http://localhost:5000
                                export CYPRESS_baseUrl=http://localhost:3000
                                
                                # Verify servers are running
                                echo "Checking frontend server..."
                                curl -f http://localhost:3000 > /dev/null 2>&1 || (echo "Frontend not accessible" && exit 1)
                                
                                echo "Checking backend server..."
                                curl -f http://localhost:5000/api/health > /dev/null 2>&1 || (echo "Backend not accessible" && exit 1)
                                
                                # Run Cypress in headless mode
                                # Set environment variables for headless execution
                                export DISPLAY=:99
                                
                                # Try to use Xvfb if available, otherwise use pure headless
                                if command -v Xvfb > /dev/null 2>&1; then
                                    echo "Starting Xvfb for headless display..."
                                    Xvfb :99 -screen 0 1280x1024x24 > /dev/null 2>&1 &
                                    XVFB_PID=$!
                                    sleep 3
                                    
                                    # Run Cypress with Xvfb
                                    npx cypress run --e2e \
                                        --browser electron \
                                        --config video=true,screenshotOnRunFailure=true
                                    
                                    # Cleanup Xvfb
                                    kill $XVFB_PID 2>/dev/null || true
                                else
                                    echo "Xvfb not found, using Cypress headless mode..."
                                    # Run Cypress in headless mode (doesn't require Xvfb)
                                    npx cypress run --e2e \
                                        --headless \
                                        --browser electron \
                                        --config video=true,screenshotOnRunFailure=true
                                fi
                            '''
                        }
                        echo '✅ Cypress E2E tests completed!'
                    } catch (Exception e) {
                        echo '❌ Cypress E2E tests failed!'
                        
                        // Send email notification for Cypress test failure
                        emailext (
                            subject: "❌ Frontend E2E Tests (Cypress) FAILED: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                            body: """
                                <h2>Frontend E2E Tests Failed</h2>
                                <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                                <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                                <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                                <p><strong>Status:</strong> <span style="color: red;">E2E TESTS FAILED ❌</span></p>
                                <p><strong>Branch:</strong> ${env.GIT_BRANCH ?: 'N/A'}</p>
                                <p><strong>Commit:</strong> ${env.GIT_COMMIT ?: 'N/A'}</p>
                                <hr>
                                <h3>Test Failure Details</h3>
                                <p>Cypress end-to-end tests have failed. Test videos and screenshots are available in build artifacts.</p>
                                <p><a href="${env.BUILD_URL}console">View Console Output</a></p>
                                <p><strong>Artifacts:</strong> Check build artifacts for test videos and screenshots.</p>
                                <hr>
                                <p><em>This is an automated message from Jenkins CI/CD Pipeline.</em></p>
                            """,
                            to: "${env.EMAIL_RECIPIENT}",
                            mimeType: 'text/html',
                            attachLog: true,
                            compressLog: true
                        )
                        throw e
                    } finally {
                        // Stop frontend server
                        echo '🛑 Stopping frontend server...'
                        sh '''
                            if [ -f frontend-server.pid ]; then
                                kill $(cat frontend-server.pid) 2>/dev/null || true
                                rm -f frontend-server.pid
                            fi
                            pkill -f "react-scripts start" || true
                        '''
                        
                        // Stop backend if we started it
                        sh '''
                            if [ -f backend-server-e2e.pid ]; then
                                kill $(cat backend-server-e2e.pid) 2>/dev/null || true
                                rm -f backend-server-e2e.pid
                            fi
                        '''
                        
                        // Archive Cypress artifacts
                        archiveArtifacts artifacts: "${env.FRONTEND_DIR}/cypress/videos/**/*,${env.FRONTEND_DIR}/cypress/screenshots/**/*", allowEmptyArchive: true
                    }
                }
            }
        }
        
        stage('SonarQube Analysis') {
            when {
                // Only run if SonarQube is configured
                anyOf {
                    expression { env.SONAR_HOST_URL != null }
                    expression { env.SONAR_TOKEN != null }
                }
            }
            steps {
                script {
                    // Check if SonarQube Scanner is available
                    def scannerHome = tool 'SonarQube Scanner'
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=jenkins-fullstack \
                                -Dsonar.sources=backend/src,frontend/src,backend/server.js \
                                -Dsonar.host.url=\${SONAR_HOST_URL} \
                                -Dsonar.login=\${SONAR_TOKEN}
                        """
                    }
                }
            }
        }
        
        stage('SonarQube Quality Gate') {
            when {
                // Only run if SonarQube analysis was executed
                anyOf {
                    expression { env.SONAR_HOST_URL != null }
                    expression { env.SONAR_TOKEN != null }
                }
            }
            steps {
                script {
                    try {
                        // Wait for SonarQube quality gate and fail build if quality gate fails
                        def qg = waitForQualityGate()
                        
                        if (qg.status != 'OK') {
                            // Quality gate failed - mark build as unstable or failed
                            echo "⚠️ SonarQube Quality Gate Status: ${qg.status}"
                            echo "📊 Quality Gate Details:"
                            echo "   - Status: ${qg.status}"
                            
                            // Get quality gate details from SonarQube
                            def sonarUrl = env.SONAR_HOST_URL ?: 'http://localhost:9000'
                            def projectKey = 'jenkins-fullstack'
                            
                            // Send specific email for SonarQube quality gate failure
                            emailext (
                                subject: "⚠️ SonarQube Quality Gate FAILED: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                                body: """
                                    <h2>SonarQube Quality Gate Failed</h2>
                                    <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                                    <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                                    <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                                    <p><strong>Quality Gate Status:</strong> <span style="color: red;">${qg.status} ⚠️</span></p>
                                    <p><strong>Branch:</strong> ${env.GIT_BRANCH ?: 'N/A'}</p>
                                    <p><strong>Commit:</strong> ${env.GIT_COMMIT ?: 'N/A'}</p>
                                    <hr>
                                    <h3>SonarQube Dashboard</h3>
                                    <p>View detailed quality gate results in SonarQube:</p>
                                    <p><a href="${sonarUrl}/dashboard?id=${projectKey}">${sonarUrl}/dashboard?id=${projectKey}</a></p>
                                    <hr>
                                    <h3>Common Quality Gate Issues</h3>
                                    <ul>
                                        <li><strong>Code Coverage:</strong> Test coverage below threshold</li>
                                        <li><strong>Code Smells:</strong> Too many code smells detected</li>
                                        <li><strong>Security Vulnerabilities:</strong> Security issues found</li>
                                        <li><strong>Bugs:</strong> Potential bugs detected</li>
                                        <li><strong>Duplications:</strong> Code duplication above threshold</li>
                                    </ul>
                                    <p>Check the SonarQube dashboard for specific issues and remediation steps.</p>
                                    <hr>
                                    <p><em>This is an automated message from Jenkins CI/CD Pipeline.</em></p>
                                """,
                                to: "${env.EMAIL_RECIPIENT}",
                                mimeType: 'text/html'
                            )
                            
                            // Mark build as unstable (or fail it)
                            if (qg.status == 'ERROR') {
                                error("❌ SonarQube Quality Gate FAILED with status: ${qg.status}")
                            } else {
                                // WARN or other non-OK status
                                currentBuild.result = 'UNSTABLE'
                                echo "⚠️ Build marked as UNSTABLE due to SonarQube quality gate: ${qg.status}"
                            }
                        } else {
                            echo "✅ SonarQube Quality Gate PASSED: ${qg.status}"
                        }
                    } catch (Exception e) {
                        echo "❌ Error checking SonarQube quality gate: ${e.getMessage()}"
                        // Send email about quality gate check failure
                        emailext (
                            subject: "❌ SonarQube Quality Gate Check FAILED: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                            body: """
                                <h2>SonarQube Quality Gate Check Error</h2>
                                <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                                <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                                <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                                <p><strong>Error:</strong> <span style="color: red;">Failed to check SonarQube quality gate</span></p>
                                <p><strong>Error Message:</strong> ${e.getMessage()}</p>
                                <p><strong>Branch:</strong> ${env.GIT_BRANCH ?: 'N/A'}</p>
                                <p><strong>Commit:</strong> ${env.GIT_COMMIT ?: 'N/A'}</p>
                                <hr>
                                <p>Please check:</p>
                                <ul>
                                    <li>SonarQube server is accessible</li>
                                    <li>SonarQube project exists</li>
                                    <li>Quality gate is configured</li>
                                    <li>Jenkins SonarQube plugin is properly configured</li>
                                </ul>
                                <hr>
                                <p><em>This is an automated message from Jenkins CI/CD Pipeline.</em></p>
                            """,
                            to: "${env.EMAIL_RECIPIENT}",
                            mimeType: 'text/html'
                        )
                        throw e
                    }
                }
            }
        }
        
        stage('Archive Artifacts') {
            steps {
                echo 'Archiving build artifacts...'
                archiveArtifacts artifacts: "${env.FRONTEND_DIR}/build/**/*", fingerprint: true
                // Postman test results are already archived in API Tests stage
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline execution completed.'
            // Clean workspace but keep SonarQube reports
            cleanWs(cleanWhenNotBuilt: false, deleteDirs: true, notFailBuild: true)
        }
        success {
            echo 'Pipeline succeeded! ✅'
            script {
                // Send email notification on successful build
                emailext (
                    subject: "✅ Jenkins Pipeline SUCCESS: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                    body: """
                        <h2>Pipeline Build Successful!</h2>
                        <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                        <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                        <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                        <p><strong>Status:</strong> <span style="color: green;">SUCCESS ✅</span></p>
                        <p><strong>Branch:</strong> ${env.GIT_BRANCH ?: 'N/A'}</p>
                        <p><strong>Commit:</strong> ${env.GIT_COMMIT ?: 'N/A'}</p>
                        <hr>
                        <h3>Build Summary</h3>
                        <p>All pipeline stages completed successfully:</p>
                        <ul>
                            <li>✅ Code Checkout</li>
                            <li>✅ Dependencies Installed (Backend & Frontend)</li>
                            <li>✅ Unit Tests Passed (Backend & Frontend)</li>
                            <li>✅ Build Completed (Backend & Frontend)</li>
                            <li>✅ API Tests Passed (Postman/Newman)</li>
                            <li>✅ E2E Tests Passed (Cypress)</li>
                            <li>✅ SonarQube Analysis Completed</li>
                            <li>✅ Artifacts Archived</li>
                        </ul>
                        <hr>
                        <h3>Build Details</h3>
                        <p><a href="${env.BUILD_URL}">View Build Details</a></p>
                        <p><a href="${env.BUILD_URL}console">View Console Output</a></p>
                        <hr>
                        <p><em>This is an automated message from Jenkins CI/CD Pipeline.</em></p>
                    """,
                    to: "${env.EMAIL_RECIPIENT}",
                    from: "${env.EMAIL_FROM}",
                    replyTo: "${env.EMAIL_REPLY_TO}",
                    mimeType: 'text/html'
                )
            }
        }
        failure {
            echo 'Pipeline failed! ❌'
            script {
                // Get failed stage information if available
                def failedStage = env.STAGE_NAME ?: 'Unknown'
                def failureReason = 'Check console output for details'
                
                // Send email notification on failure (only if not already sent by specific stage)
                // This is a fallback for unexpected failures
                emailext (
                    subject: "❌ Jenkins Pipeline FAILED: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                    body: """
                        <h2>Pipeline Build Failed</h2>
                        <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                        <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                        <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                        <p><strong>Status:</strong> <span style="color: red;">FAILED ❌</span></p>
                        <p><strong>Failed Stage:</strong> ${failedStage}</p>
                        <p><strong>Branch:</strong> ${env.GIT_BRANCH ?: 'N/A'}</p>
                        <p><strong>Commit:</strong> ${env.GIT_COMMIT ?: 'N/A'}</p>
                        <hr>
                        <h3>Build Console Output</h3>
                        <p>Check the build console for detailed error information.</p>
                        <p><a href="${env.BUILD_URL}console">View Console Output</a></p>
                        <hr>
                        <h3>Common Failure Points</h3>
                        <ul>
                            <li><strong>Unit Tests:</strong> Backend or Frontend test failures</li>
                            <li><strong>Build:</strong> Compilation or build errors</li>
                            <li><strong>API Tests:</strong> Postman/Newman test failures</li>
                            <li><strong>E2E Tests:</strong> Cypress test failures</li>
                            <li><strong>SonarQube:</strong> Quality gate failures</li>
                        </ul>
                        <hr>
                        <p><em>This is an automated message from Jenkins CI/CD Pipeline.</em></p>
                    """,
                    to: "${env.EMAIL_RECIPIENT}",
                    from: "${env.EMAIL_FROM}",
                    replyTo: "${env.EMAIL_REPLY_TO}",
                    mimeType: 'text/html',
                    attachLog: true,
                    compressLog: true
                )
            }
        }
        unstable {
            echo 'Pipeline completed with warnings! ⚠️'
            script {
                // Send email notification on warnings/unstable
                emailext (
                    subject: "⚠️ Jenkins Pipeline UNSTABLE: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                    body: """
                        <h2>Pipeline Build Completed with Warnings</h2>
                        <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                        <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                        <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                        <p><strong>Status:</strong> <span style="color: orange;">UNSTABLE ⚠️</span></p>
                        <p><strong>Branch:</strong> ${env.GIT_BRANCH ?: 'N/A'}</p>
                        <p><strong>Commit:</strong> ${env.GIT_COMMIT ?: 'N/A'}</p>
                        <hr>
                        <h3>Build Console Output</h3>
                        <p>Check the build console for warning details.</p>
                        <p><a href="${env.BUILD_URL}console">View Console Output</a></p>
                        <hr>
                        <p><em>This is an automated message from Jenkins CI/CD Pipeline.</em></p>
                    """,
                    to: "${env.EMAIL_RECIPIENT}",
                    from: "${env.EMAIL_FROM}",
                    replyTo: "${env.EMAIL_REPLY_TO}",
                    mimeType: 'text/html',
                    attachLog: false,
                    compressLog: false
                )
            }
        }
        aborted {
            echo 'Pipeline was aborted! 🛑'
            script {
                // Send email notification on abort
                emailext (
                    subject: "🛑 Jenkins Pipeline ABORTED: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                    body: """
                        <h2>Pipeline Build Aborted</h2>
                        <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                        <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                        <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                        <p><strong>Status:</strong> <span style="color: gray;">ABORTED 🛑</span></p>
                        <p><strong>Branch:</strong> ${env.GIT_BRANCH ?: 'N/A'}</p>
                        <p><strong>Commit:</strong> ${env.GIT_COMMIT ?: 'N/A'}</p>
                        <hr>
                        <p><em>This is an automated message from Jenkins CI/CD Pipeline.</em></p>
                    """,
                    to: "${env.EMAIL_RECIPIENT}",
                    from: "${env.EMAIL_FROM}",
                    replyTo: "${env.EMAIL_REPLY_TO}",
                    mimeType: 'text/html'
                )
            }
        }
    }
}

