pipeline {
    agent any

    environment {
        SONARQUBE_URL = 'http://192.168.189.138:9000'
        SONARQUBE_TOKEN = '3rINM1HkWDD/nb7HmKbJYMVHZniCbwkC5xGCEp0AZTU=' // Token fourni
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo 'Cloning repository from GitHub...'
                    checkout scm: [
                        $class: 'GitSCM',
                        branches: [[name: 'refs/heads/main']], // Spécification de la branche main
                        userRemoteConfigs: [[url: 'https://github.com/18448-ops/simple-banking.git']]
                    ]
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker build -t manel/simple-banking-api:latest .'
                }
            }
        }

        stage('Trivy Scan') {
            steps {
                script {
                    echo 'Running Trivy scan...'
                    sh 'curl -sfL https://github.com/aquasecurity/trivy/releases/download/v0.33.0/trivy_0.33.0_Linux-64bit.tar.gz -o trivy.tar.gz'
                    sh 'tar -xvzf trivy.tar.gz'
                    sh 'mv trivy /usr/local/bin/'
                    sh 'trivy image --format json --output trivy_report.json manel/simple-banking-api:latest'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    echo 'Running SonarQube analysis...'
                    withSonarQubeEnv('SonarQube') {
                        sh '''
                            mvn clean verify sonar:sonar \
                                -Dsonar.projectKey=simple-banking-api \
                                -Dsonar.host.url=${SONARQUBE_URL} \
                                -Dsonar.login=${SONARQUBE_TOKEN}
                        '''
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Running tests...'
                    sh 'pytest tests/'
                }
            }
        }

        stage('Post Actions') {
            steps {
                script {
                    echo 'Cleaning up workspace...'
                    cleanWs()
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
