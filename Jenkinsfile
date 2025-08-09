pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'manel/simple-banking-api:latest'
        SONARQUBE = 'SonarQube' // Nom de votre configuration SonarQube dans Jenkins
        GIT_REPO = 'https://github.com/18448-ops/simple-banking.git'
        GIT_BRANCH = 'main'
    }

    tools {
        // Définir les outils nécessaires, par exemple, Maven si tu l'utilises
        maven 'Maven 3'
    }

    stages {
        // Checkout code
        stage('Checkout SCM') {
            steps {
                echo 'Cloning repository from GitHub...'
                git branch: "${GIT_BRANCH}", url: "${GIT_REPO}"
            }
        }

        // Build Docker Image
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        // Trivy scan
        stage('Trivy Scan') {
            steps {
                script {
                    echo 'Installing Trivy...'
                    sh '''
                        # Télécharge Trivy et installe-le avec sudo
                        curl -sfL https://github.com/aquasecurity/trivy/releases/download/v0.33.0/trivy_0.33.0_Linux-64bit.tar.gz -o trivy.tar.gz
                        tar -xvzf trivy.tar.gz
                        sudo mv trivy /usr/local/bin/
                        sudo chmod +x /usr/local/bin/trivy
                        trivy --version
                    '''
                    echo 'Running Trivy scan...'
                    sh "trivy image --format json --output trivy_report.json $DOCKER_IMAGE"
                }
            }
        }

        // SonarQube Analysis
        stage('SonarQube Analysis') {
            steps {
                script {
                    echo 'Running SonarQube Analysis...'
                    withSonarQubeEnv(SONARQUBE) {
                        sh '''
                            mvn clean install sonar:sonar -Dsonar.projectKey=simple-banking -Dsonar.host.url=http://localhost:9000
                        '''
                    }
                }
            }
        }

        // Run Tests
        stage('Run Tests') {
            steps {
                echo 'Running Tests...'
                sh 'pytest tests/'
            }
        }

        // Clean workspace
        stage('Post Actions') {
            steps {
                echo 'Cleaning up workspace...'
                cleanWs()
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed!'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
    }
}
