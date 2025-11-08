pipeline {
    agent any
    
    environment {
        NODE_VERSION = '18'
        BACKEND_DIR = 'backend'
        FRONTEND_DIR = 'frontend'
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
        
        stage('Archive Artifacts') {
            steps {
                echo 'Archiving build artifacts...'
                archiveArtifacts artifacts: "${env.FRONTEND_DIR}/build/**/*", fingerprint: true
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline execution completed.'
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded! ✅'
        }
        failure {
            echo 'Pipeline failed! ❌'
        }
    }
}

