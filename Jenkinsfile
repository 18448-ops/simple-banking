pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'manel/simple-banking-api'
        SONAR_PROJECT_KEY = 'your_project_key'
    }

    tools {
        // Utilisation de Maven dans Jenkins (assurez-vous qu'il est installé et configuré dans Jenkins)
        maven 'Maven 3'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo 'Cloning repository from GitHub...'
                    checkout scm
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Trivy Scan') {
            steps {
                script {
                    echo 'Installing Trivy...'
                    sh '''
                        curl -sfL https://github.com/aquasecurity/trivy/releases/download/v0.33.0/trivy_0.33.0_Linux-64bit.tar.gz -o trivy.tar.gz
                        tar -xvzf trivy.tar.gz
                        mv trivy /usr/local/bin/
                        trivy --version
                    '''
                    echo 'Running Trivy scan...'
                    sh "trivy image --format json --output trivy_report.json $DOCKER_IMAGE"
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    echo 'Running SonarQube analysis...'
                    withSonarQubeEnv('SonarQube-Server') {
                        sh "mvn clean install sonar:sonar -Dsonar.projectKey=$SONAR_PROJECT_KEY"
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Running tests...'
                    // Ajoutez ici votre commande pour exécuter des tests unitaires, par exemple :
                    sh 'pytest'
                }
            }
        }

        stage('Post Actions') {
            steps {
                cleanWs() // Nettoie le workspace
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
