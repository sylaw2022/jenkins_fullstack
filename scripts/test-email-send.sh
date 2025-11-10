#!/bin/bash
# Script to test email sending from Jenkins
# This creates a simple test pipeline that sends an email

echo "=========================================="
echo "Jenkins Email Test"
echo "=========================================="
echo ""

# Check if Jenkins is running
if ! systemctl is-active --quiet jenkins; then
    echo "❌ Jenkins is not running"
    echo "Start Jenkins with: sudo systemctl start jenkins"
    exit 1
fi

echo "✅ Jenkins is running"
echo ""

# Get Jenkins URL
JENKINS_PORT=$(grep HTTP_PORT /etc/default/jenkins 2>/dev/null | cut -d'=' -f2 || echo "8081")
JENKINS_URL="http://localhost:${JENKINS_PORT}"

echo "Jenkins URL: ${JENKINS_URL}"
echo ""

echo "=========================================="
echo "Email Test Options"
echo "=========================================="
echo ""
echo "Option 1: Test from Jenkins UI (Recommended)"
echo "  1. Open Jenkins: ${JENKINS_URL}"
echo "  2. Go to: Manage Jenkins → Configure System"
echo "  3. Scroll to 'Extended E-mail Notification'"
echo "  4. Click 'Test configuration by sending test e-mail'"
echo "  5. Enter: groklord@yahoo.com"
echo "  6. Click 'Test configuration'"
echo "  7. Check your email inbox (and spam folder)"
echo ""
echo "Option 2: Create a test pipeline job"
echo "  - Create a new pipeline job"
echo "  - Use the test pipeline script below"
echo ""
echo "Option 3: Test from existing pipeline"
echo "  - Trigger a build that will send an email"
echo "  - Or manually fail a stage to trigger email"
echo ""

echo "=========================================="
echo "Test Pipeline Script"
echo "=========================================="
echo ""
echo "Create a new Pipeline job in Jenkins and use this script:"
echo ""
cat << 'TEST_PIPELINE'
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
                    echo 'Sending test email...'
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
                    echo '✅ Test email sent!'
                }
            }
        }
    }
    
    post {
        always {
            echo 'Email test completed. Check your inbox!'
        }
    }
}
TEST_PIPELINE

echo ""
echo "=========================================="
echo "Quick Test Commands"
echo "=========================================="
echo ""
echo "1. Check Jenkins email configuration:"
echo "   curl -s ${JENKINS_URL}/configure | grep -i 'email\|smtp' || echo 'Use Jenkins UI to check configuration'"
echo ""
echo "2. View Jenkins logs for email errors:"
echo "   sudo tail -f /var/log/jenkins/jenkins.log | grep -i email"
echo ""
echo "3. Test SMTP connection:"
echo "   telnet smtp.mail.yahoo.com 587"
echo ""

echo "=========================================="
echo "Expected Results"
echo "=========================================="
echo ""
echo "✅ Success:"
echo "   - Email received in groklord@yahoo.com inbox"
echo "   - 'From' address shows: groklord@yahoo.com"
echo "   - No error messages in Jenkins console"
echo ""
echo "❌ Failure:"
echo "   - Check spam/junk folder"
echo "   - Check Jenkins logs for errors"
echo "   - Verify SMTP configuration in Jenkins"
echo "   - Verify Yahoo App Password is correct"
echo ""

echo "=========================================="
echo "For troubleshooting, see:"
echo "  JENKINS_EMAIL_TROUBLESHOOTING.md"
echo "=========================================="

