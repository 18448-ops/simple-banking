pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'manel/simple-banking-api'
        SONAR_PROJECT_KEY = 'simple-banking'
        SONAR_HOST_URL = 'http://<YOUR_SONARQUBE_URL>' // Remplace par l'URL de ton serveur SonarQube
        SONAR_TOKEN = credentials('sonar-token') // Utilise le token que tu as dans Jenkins (tu devras configurer cette clé d'authentification)
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo 'Cloning Git repository...'
                checkout scm // Récupère automatiquement le dépôt Git configuré dans Jenkins
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    // Exécute Docker avec sudo pour construire l'image
                    sh 'sudo docker build -t ${DOCKER_IMAGE_NAME}:latest .'
                }
            }
        }

        stage('Trivy Scan') {
            steps {
                script {
                    echo 'Running Trivy scan...'
                    // Exécute Trivy avec sudo pour scanner l'image Docker
                    sh 'sudo trivy image --format json --output trivy_report.json ${DOCKER_IMAGE_NAME}'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    echo 'Running SonarQube analysis...'
                    // Exécution de l'analyse SonarQube avec Maven (assure-toi que Maven est installé et configuré)
                    sh '''
                    mvn clean install
                    mvn sonar:sonar \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.host.url=${SONAR_HOST_URL} \
                        -Dsonar.login=${SONAR_TOKEN}
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Running tests...'
                    // Exécution des tests avec pytest
                    sh 'pytest --maxfail=1 --disable-warnings -q'
                }
            }
        }

        stage('Post Actions') {
            steps {
                script {
                    echo 'Cleaning up workspace...'
                    // Nettoyage du workspace après le build
                    cleanWs()
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
