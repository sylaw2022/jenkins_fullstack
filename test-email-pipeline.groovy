// Test Email Pipeline Script
// Use this script to create a test pipeline job in Jenkins

pipeline {
    agent any
    
    environment {
        EMAIL_RECIPIENT = 'groklord@yahoo.com'
        EMAIL_FROM = 'groklord@yahoo.com'
        EMAIL_REPLY_TO = 'groklord@yahoo.com'
    }
    
    stages {
        stage('Test Email') {
            steps {
                script {
                    echo '📧 Sending test email...'
                    emailext (
                        subject: "✅ Jenkins Email Test - ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                        body: """
                            <h2>Email Test Successful!</h2>
                            <p>This is a test email from Jenkins CI/CD Pipeline.</p>
                            <p><strong>Job:</strong> ${env.JOB_NAME}</p>
                            <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                            <p><strong>Build URL:</strong> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                            <p><strong>Status:</strong> <span style="color: green;">TEST EMAIL ✅</span></p>
                            <p><strong>Time:</strong> ${new Date()}</p>
                            <hr>
                            <p>If you received this email, your Jenkins email configuration is working correctly!</p>
                            <p><em>This is an automated test message from Jenkins CI/CD Pipeline.</em></p>
                        """,
                        to: "${env.EMAIL_RECIPIENT}",
                        from: "${env.EMAIL_FROM}",
                        replyTo: "${env.EMAIL_REPLY_TO}",
                        mimeType: 'text/html'
                    )
                    echo '✅ Test email sent! Check your inbox at groklord@yahoo.com'
                }
            }
        }
    }
    
    post {
        always {
            echo '📧 Email test completed. Check your inbox (and spam folder)!'
        }
        success {
            echo '✅ Email test pipeline completed successfully!'
        }
    }
}

