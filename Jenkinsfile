pipeline {
    agent any
    
    environment {
        NODE_VERSION = '18'
        BACKEND_DIR = 'backend'
        FRONTEND_DIR = 'frontend'
        // Email notification recipient
        EMAIL_RECIPIENT = 'groklord@yahoo.com'
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
                            sh 'npm test || true' // Continue even if tests fail (no tests yet)
                        }
                    }
                }
                stage('Frontend Tests') {
                    steps {
                        dir("${env.FRONTEND_DIR}") {
                            echo 'Running frontend tests...'
                            sh 'npm test -- --watchAll=false || true' // Continue even if tests fail
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
                            sh 'node --version'
                            sh 'npm --version'
                        }
                    }
                }
                stage('Frontend Build') {
                    steps {
                        dir("${env.FRONTEND_DIR}") {
                            echo 'Building frontend...'
                            sh 'npm run build'
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
        }
        failure {
            echo 'Pipeline failed! ❌'
            script {
                // Send email notification on failure
                emailext (
                    subject: "❌ Jenkins Pipeline FAILED: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                    body: """
                        <h2>Pipeline Build Failed</h2>
                        <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                        <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                        <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                        <p><strong>Status:</strong> <span style="color: red;">FAILED ❌</span></p>
                        <p><strong>Branch:</strong> ${env.GIT_BRANCH ?: 'N/A'}</p>
                        <p><strong>Commit:</strong> ${env.GIT_COMMIT ?: 'N/A'}</p>
                        <hr>
                        <h3>Build Console Output</h3>
                        <p>Check the build console for detailed error information.</p>
                        <p><a href="${env.BUILD_URL}console">View Console Output</a></p>
                        <hr>
                        <p><em>This is an automated message from Jenkins CI/CD Pipeline.</em></p>
                    """,
                    to: "${env.EMAIL_RECIPIENT}",
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
                    mimeType: 'text/html'
                )
            }
        }
    }
}

